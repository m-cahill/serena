"""Execution-phase batch orchestration for Serena processing pipeline.

M16: Extracted from process_images_inner. Handles torch context, batch loop,
sampler invocation, and interruption checks. Yields latent samples per batch;
decode/save/postprocess: M18 decode_runtime (process_images_inner path only).
M19: Model access via p.model_provider.get_model(p) only.
"""

from __future__ import annotations

import os

import torch

from modules import devices, extra_networks, sd_models, sd_vae_approx, sd_unet, rng
from modules.sd_hijack import model_hijack
from modules.shared import cmd_opts
import modules.shared as shared

from modules.processing_helpers import _eff_opts
import modules.paths as paths
# Latent dimensions (matches processing.py opt_C, opt_f)
_OPT_C = 4
_OPT_F = 8


def run_generation_batches(p):
    """Execute generation batches: torch context, init, batch loop, sampler call.

    Yields (batch_index, samples_ddim) for each batch. Caller is responsible for
    post_sample, decode, postprocess_batch, and save/decode logic.

    M16 extraction: orchestration moved from process_images_inner.
    """
    state = shared.state

    with torch.no_grad(), p.model_provider.get_model(p).ema_scope():
        with devices.autocast():
            p.init(p.all_prompts, p.all_seeds, p.all_subseeds)

            eff = _eff_opts(p)
            if eff.live_previews_enable and eff.show_progress_type == "Approx NN":
                sd_vae_approx.model()

            sd_unet.apply_unet()

        if state.job_count == -1:
            state.job_count = p.n_iter

        for n in range(p.n_iter):
            p.iteration = n

            if state.skipped:
                state.skipped = False

            if state.interrupted or state.stopping_generation:
                break

            sd_models.reload_model_weights()

            p.prompts = p.all_prompts[n * p.batch_size:(n + 1) * p.batch_size]
            p.negative_prompts = p.all_negative_prompts[n * p.batch_size:(n + 1) * p.batch_size]
            p.seeds = p.all_seeds[n * p.batch_size:(n + 1) * p.batch_size]
            p.subseeds = p.all_subseeds[n * p.batch_size:(n + 1) * p.batch_size]

            latent_channels = getattr(p.model_provider.get_model(p), 'latent_channels', _OPT_C)
            p.rng = rng.ImageRNG(
                (latent_channels, p.height // _OPT_F, p.width // _OPT_F),
                p.seeds,
                subseeds=p.subseeds,
                subseed_strength=p.subseed_strength,
                seed_resize_from_h=p.seed_resize_from_h,
                seed_resize_from_w=p.seed_resize_from_w,
            )

            if p.scripts is not None:
                p.scripts.before_process_batch(p, batch_number=n, prompts=p.prompts, seeds=p.seeds, subseeds=p.subseeds)

            if len(p.prompts) == 0:
                break

            p.parse_extra_network_prompts()

            if not p.disable_extra_networks:
                with devices.autocast():
                    extra_networks.activate(p, p.extra_network_data)

            if p.scripts is not None:
                p.scripts.process_batch(p, batch_number=n, prompts=p.prompts, seeds=p.seeds, subseeds=p.subseeds)

            p.setup_conds()

            p.extra_generation_params.update(model_hijack.extra_generation_params)

            if n == 0 and not cmd_opts.no_prompt_history:
                from modules.processing import Processed
                with open(os.path.join(paths.data_path, "params.txt"), "w", encoding="utf8") as file:
                    processed = Processed(p, [])
                    file.write(processed.infotext(p, 0))

            for comment in model_hijack.comments:
                p.comment(comment)

            if p.n_iter > 1:
                shared.state.job = f"Batch {n+1} out of {p.n_iter}"

            sd_models.apply_alpha_schedule_override(p.model_provider.get_model(p), p)

            with devices.without_autocast() if devices.unet_needs_upcast else devices.autocast():
                samples_ddim = p.sample(
                    conditioning=p.c,
                    unconditional_conditioning=p.uc,
                    seeds=p.seeds,
                    subseeds=p.subseeds,
                    subseed_strength=p.subseed_strength,
                    prompts=p.prompts,
                )

            yield (n, samples_ddim)
