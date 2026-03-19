"""Sampler invocation orchestration for Serena processing pipeline.

M17: Extracted from StableDiffusionProcessingTxt2Img.sample, sample_hr_pass,
and StableDiffusionProcessingImg2Img.sample. Handles sampler creation (where
applicable) and invocation; returns latent samples. Script hooks, decode,
and save remain in processing.py.
"""

from __future__ import annotations


def run_sampler_txt2img(p, x, conditioning, unconditional_conditioning):
    """Txt2Img: create sampler, invoke sample(), return latents.

    M17 extraction: replaces inline create_sampler + sampler.sample in
    StableDiffusionProcessingTxt2Img.sample. Assigns p.sampler for extension
    compatibility.
    """
    from modules import sd_samplers

    p.sampler = sd_samplers.create_sampler(p.sampler_name, p.sd_model)
    samples = p.sampler.sample(
        p,
        x,
        conditioning,
        unconditional_conditioning,
        image_conditioning=p.txt2img_image_conditioning(x),
    )
    return samples


def run_sampler_img2img(
    p,
    x,
    noise,
    conditioning,
    unconditional_conditioning,
    steps=None,
    image_conditioning=None,
    sampler_name=None,
):
    """Img2Img: invoke sample_img2img. If sampler_name provided (hr pass), create first.

    M17 extraction: replaces inline sampler.sample_img2img in
    StableDiffusionProcessingImg2Img.sample and sample_hr_pass.
    """
    from modules import sd_samplers

    if sampler_name is not None:
        p.sampler = sd_samplers.create_sampler(sampler_name, p.sd_model)
    samples = p.sampler.sample_img2img(
        p,
        x,
        noise,
        conditioning,
        unconditional_conditioning,
        steps=steps,
        image_conditioning=image_conditioning,
    )
    return samples
