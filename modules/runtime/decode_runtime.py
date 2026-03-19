"""M18: Decode, postprocess (face / color / overlay), and save for process_images_inner.

Extracted from modules.processing.process_images_inner. Script hooks remain in
processing.py; this module performs the non-hook output stages only.
"""

from __future__ import annotations

import numpy as np
import torch
from PIL import Image

from modules import devices, errors, lowvram
from modules.sd_samplers_common import decode_first_stage
import modules.shared as shared
from modules.shared import opts


class DecodedSamples(list):
    already_decoded = True


def decode_latent_batch(model, batch, target_device=None, check_for_nans=False):
    samples = DecodedSamples()

    if check_for_nans:
        devices.test_for_nans(batch, "unet")

    for i in range(batch.shape[0]):
        sample = decode_first_stage(model, batch[i:i + 1])[0]

        if check_for_nans:

            try:
                devices.test_for_nans(sample, "vae")
            except devices.NansException as e:
                if shared.opts.auto_vae_precision_bfloat16:
                    autofix_dtype = torch.bfloat16
                    autofix_dtype_text = "bfloat16"
                    autofix_dtype_setting = "Automatically convert VAE to bfloat16"
                    autofix_dtype_comment = ""
                elif shared.opts.auto_vae_precision:
                    autofix_dtype = torch.float32
                    autofix_dtype_text = "32-bit float"
                    autofix_dtype_setting = "Automatically revert VAE to 32-bit floats"
                    autofix_dtype_comment = "\nTo always start with 32-bit VAE, use --no-half-vae commandline flag."
                else:
                    raise e

                if devices.dtype_vae == autofix_dtype:
                    raise e

                errors.print_error_explanation(
                    "A tensor with all NaNs was produced in VAE.\n"
                    f"Web UI will now convert VAE into {autofix_dtype_text} and retry.\n"
                    f"To disable this behavior, disable the '{autofix_dtype_setting}' setting.{autofix_dtype_comment}"
                )

                devices.dtype_vae = autofix_dtype
                model.first_stage_model.to(devices.dtype_vae)
                batch = batch.to(devices.dtype_vae)

                sample = decode_first_stage(model, batch[i:i + 1])[0]

        if target_device is not None:
            sample = sample.to(target_device)

        samples.append(sample)

    return samples


def decode_latents(p, samples_ddim):
    """VAE decode and normalize to [0,1] float batch tensor; mirrors former process_images_inner block."""
    if getattr(samples_ddim, "already_decoded", False):
        x_samples_ddim = samples_ddim
    else:
        devices.test_for_nans(samples_ddim, "unet")

        if opts.sd_vae_decode_method != "Full":
            p.extra_generation_params["VAE Decoder"] = opts.sd_vae_decode_method
        x_samples_ddim = decode_latent_batch(p.sd_model, samples_ddim, target_device=devices.cpu, check_for_nans=True)

    x_samples_ddim = torch.stack(x_samples_ddim).float()
    x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)

    del samples_ddim

    if lowvram.is_enabled(shared.sd_model):
        lowvram.send_everything_to_cpu()

    devices.torch_gc()

    shared.state.nextjob()

    return x_samples_ddim


def postprocess_face_restore_row(p, x_sample_tensor, row_index, save_samples, infotext_fn):
    """Tensor row -> uint8 numpy; optional face restoration and pre-restore save."""
    import modules.face_restoration
    import modules.images as images

    x_sample = 255.0 * np.moveaxis(x_sample_tensor.cpu().numpy(), 0, 2)
    x_sample = x_sample.astype(np.uint8)

    if p.restore_faces:
        if save_samples and p.opts_snapshot.save_images_before_face_restoration:
            images.save_image(
                Image.fromarray(x_sample),
                p.outpath_samples,
                "",
                p.seeds[row_index],
                p.prompts[row_index],
                p.opts_snapshot.samples_format,
                info=infotext_fn(row_index),
                p=p,
                suffix="-before-face-restoration",
            )

        devices.torch_gc()

        x_sample = modules.face_restoration.restore_faces(x_sample)

        devices.torch_gc()

    return x_sample


def postprocess_images_for_row(p, image, row_index, save_samples, infotext_fn, overlay_image):
    """Color correction (if any) and inpaint overlay composite; no script hooks."""
    from modules.processing import apply_color_correction, apply_overlay

    import modules.images as images

    if p.color_corrections is not None and row_index < len(p.color_corrections):
        if save_samples and p.opts_snapshot.save_images_before_color_correction:
            image_without_cc, _ = apply_overlay(image, p.paste_to, overlay_image)
            images.save_image(
                image_without_cc,
                p.outpath_samples,
                "",
                p.seeds[row_index],
                p.prompts[row_index],
                p.opts_snapshot.samples_format,
                info=infotext_fn(row_index),
                p=p,
                suffix="-before-color-correction",
            )
        image = apply_color_correction(p.color_corrections[row_index], image)

    image, original_denoised_image = apply_overlay(image, p.paste_to, overlay_image)
    return image, original_denoised_image


def save_outputs_for_row(
    p,
    row_index,
    image,
    original_denoised_image,
    mask_for_overlay,
    save_samples,
    infotext_fn,
    output_images,
    infotexts,
):
    """Save main sample, append infotexts/output_images, optional mask outputs."""
    import modules.images as images

    if save_samples:
        images.save_image(
            image,
            p.outpath_samples,
            "",
            p.seeds[row_index],
            p.prompts[row_index],
            p.opts_snapshot.samples_format,
            info=infotext_fn(row_index),
            p=p,
        )

    text = infotext_fn(row_index)
    infotexts.append(text)
    if opts.enable_pnginfo:
        image.info["parameters"] = text
    output_images.append(image)

    if mask_for_overlay is not None:
        if p.opts_snapshot.return_mask or p.opts_snapshot.save_mask:
            image_mask = mask_for_overlay.convert("RGB")
            if save_samples and p.opts_snapshot.save_mask:
                images.save_image(
                    image_mask,
                    p.outpath_samples,
                    "",
                    p.seeds[row_index],
                    p.prompts[row_index],
                    p.opts_snapshot.samples_format,
                    info=infotext_fn(row_index),
                    p=p,
                    suffix="-mask",
                )
            if p.opts_snapshot.return_mask:
                output_images.append(image_mask)

        if p.opts_snapshot.return_mask_composite or p.opts_snapshot.save_mask_composite:
            image_mask_composite = Image.composite(
                original_denoised_image.convert("RGBA").convert("RGBa"),
                Image.new("RGBa", image.size),
                images.resize_image(2, mask_for_overlay, image.width, image.height).convert("L"),
            ).convert("RGBA")
            if save_samples and p.opts_snapshot.save_mask_composite:
                images.save_image(
                    image_mask_composite,
                    p.outpath_samples,
                    "",
                    p.seeds[row_index],
                    p.prompts[row_index],
                    p.opts_snapshot.samples_format,
                    info=infotext_fn(row_index),
                    p=p,
                    suffix="-mask-composite",
                )
            if p.opts_snapshot.return_mask_composite:
                output_images.append(image_mask_composite)


def save_outputs_grid(p, output_images, infotexts, infotext_fn):
    """Grid insert and/or grid save; mutates output_images and infotexts like process_images_inner."""
    import modules.images as images

    index_of_first_image = 0
    unwanted_grid_because_of_img_count = len(output_images) < 2 and p.opts_snapshot.grid_only_if_multiple
    if (p.opts_snapshot.return_grid or p.opts_snapshot.grid_save) and not p.do_not_save_grid and not unwanted_grid_because_of_img_count:
        grid = images.image_grid(output_images, p.batch_size)

        if p.opts_snapshot.return_grid:
            text = infotext_fn(use_main_prompt=True)
            infotexts.insert(0, text)
            if opts.enable_pnginfo:
                grid.info["parameters"] = text
            output_images.insert(0, grid)
            index_of_first_image = 1
        if p.opts_snapshot.grid_save:
            images.save_image(
                grid,
                p.outpath_grids,
                "grid",
                p.all_seeds[0],
                p.all_prompts[0],
                p.opts_snapshot.grid_format,
                info=infotext_fn(use_main_prompt=True),
                short_filename=not p.opts_snapshot.grid_extended_filename,
                p=p,
                grid=True,
            )

    return index_of_first_image
