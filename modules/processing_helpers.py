"""Shared helpers used by processing types and re-exported from processing.py (M38)."""
from __future__ import annotations

import logging
import math

import cv2
import numpy as np
import torch
from PIL import Image
from skimage import exposure
from blendmodes.blend import blendLayers, BlendType

import modules.images as images
import modules.shared as shared
from modules import rng
from modules.sd_samplers_common import images_tensor_to_samples, approximation_indexes
from modules.shared import opts

# some of those options should not be changed at all because they would break the model, so I removed them from options.
opt_C = 4
opt_f = 8


def setup_color_correction(image):
    logging.info("Calibrating color correction.")
    correction_target = cv2.cvtColor(np.asarray(image.copy()), cv2.COLOR_RGB2LAB)
    return correction_target


def apply_color_correction(correction, original_image):
    logging.info("Applying color correction.")
    image = Image.fromarray(cv2.cvtColor(exposure.match_histograms(
        cv2.cvtColor(
            np.asarray(original_image),
            cv2.COLOR_RGB2LAB
        ),
        correction,
        channel_axis=2
    ), cv2.COLOR_LAB2RGB).astype("uint8"))

    image = blendLayers(image, original_image, BlendType.LUMINOSITY)

    return image.convert('RGB')


def uncrop(image, dest_size, paste_loc):
    x, y, w, h = paste_loc
    base_image = Image.new('RGBA', dest_size)
    image = images.resize_image(1, image, w, h)
    base_image.paste(image, (x, y))
    image = base_image

    return image


def apply_overlay(image, paste_loc, overlay):
    if overlay is None:
        return image, image.copy()

    if paste_loc is not None:
        image = uncrop(image, (overlay.width, overlay.height), paste_loc)

    original_denoised_image = image.copy()

    image = image.convert('RGBA')
    image.alpha_composite(overlay)
    image = image.convert('RGB')

    return image, original_denoised_image

def create_binary_mask(image, round=True):
    if image.mode == 'RGBA' and image.getextrema()[-1] != (255, 255):
        if round:
            image = image.split()[-1].convert("L").point(lambda x: 255 if x > 128 else 0)
        else:
            image = image.split()[-1].convert("L")
    else:
        image = image.convert('L')
    return image


def _orchestration_model(p):
    """Live model for supported-path orchestration in this module (M35).

    Uses ``p.model_provider`` when set (``ProcessingRunner.prepare``); otherwise
    ``shared.sd_model``. Runtime modules continue to use ``ModelProvider`` only.
    """
    mp = getattr(p, "model_provider", None)
    if mp is not None:
        return mp.get_model(p)
    return shared.sd_model


def txt2img_image_conditioning(sd_model, x, width, height):
    if sd_model.model.conditioning_key in {'hybrid', 'concat'}: # Inpainting models

        # The "masked-image" in this case will just be all 0.5 since the entire image is masked.
        image_conditioning = torch.ones(x.shape[0], 3, height, width, device=x.device) * 0.5
        image_conditioning = images_tensor_to_samples(image_conditioning, approximation_indexes.get(opts.sd_vae_encode_method))

        # Add the fake full 1s mask to the first dimension.
        image_conditioning = torch.nn.functional.pad(image_conditioning, (0, 0, 0, 0, 1, 0), value=1.0)
        image_conditioning = image_conditioning.to(x.dtype)

        return image_conditioning

    elif sd_model.model.conditioning_key == "crossattn-adm": # UnCLIP models

        return x.new_zeros(x.shape[0], 2*sd_model.noise_augmentor.time_embed.dim, dtype=x.dtype, device=x.device)

    else:
        if sd_model.is_sdxl_inpaint:
            # The "masked-image" in this case will just be all 0.5 since the entire image is masked.
            image_conditioning = torch.ones(x.shape[0], 3, height, width, device=x.device) * 0.5
            image_conditioning = images_tensor_to_samples(image_conditioning,
                                                            approximation_indexes.get(opts.sd_vae_encode_method))

            # Add the fake full 1s mask to the first dimension.
            image_conditioning = torch.nn.functional.pad(image_conditioning, (0, 0, 0, 0, 1, 0), value=1.0)
            image_conditioning = image_conditioning.to(x.dtype)

            return image_conditioning

        # Dummy zero conditioning if we're not using inpainting or unclip models.
        # Still takes up a bit of memory, but no encoder call.
        # Pretty sure we can just make this a 1x1 image since its not going to be used besides its batch size.
        return x.new_zeros(x.shape[0], 5, 1, 1, dtype=x.dtype, device=x.device)



def create_random_tensors(shape, seeds, subseeds=None, subseed_strength=0.0, seed_resize_from_h=0, seed_resize_from_w=0, p=None):
    g = rng.ImageRNG(shape, seeds, subseeds=subseeds, subseed_strength=subseed_strength, seed_resize_from_h=seed_resize_from_h, seed_resize_from_w=seed_resize_from_w)
    return g.next()



def old_hires_fix_first_pass_dimensions(width, height):
    """old algorithm for auto-calculating first pass size"""

    desired_pixel_count = 512 * 512
    actual_pixel_count = width * height
    scale = math.sqrt(desired_pixel_count / actual_pixel_count)
    width = math.ceil(scale * width / 64) * 64
    height = math.ceil(scale * height / 64) * 64

    return width, height
