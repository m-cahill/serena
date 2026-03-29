"""Processing pipeline: orchestration entrypoints and re-exports (M38: classes in processing_types)."""
from __future__ import annotations

import os
import random

from PIL import Image

import modules.sd_hijack
from modules import devices, extra_networks, profiling, scripts, sd_samplers
from modules.sd_hijack import model_hijack
from modules.shared import opts, cmd_opts
import modules.shared as shared
from modules.opts_snapshot import create_opts_snapshot
from modules.runtime_context import RuntimeContext, model_identity_from_model
import modules.prompt_seed_prep as prompt_seed_prep
import modules.runtime_utils as runtime_utils
from modules.runtime import processing_runtime, decode_runtime
import modules.sd_models as sd_models
import modules.sd_vae as sd_vae

from modules.processing_helpers import (
    opt_C,
    opt_f,
    setup_color_correction,
    apply_color_correction,
    uncrop,
    apply_overlay,
    create_binary_mask,
    _orchestration_model,
    txt2img_image_conditioning,
    create_random_tensors,
    old_hires_fix_first_pass_dimensions,
)
from modules.processing_infotext import create_infotext, program_version
from modules.processing_types import (
    StableDiffusionProcessing,
    Processed,
    StableDiffusionProcessingTxt2Img,
    StableDiffusionProcessingImg2Img,
)


def get_fixed_seed(seed):
    if seed == '' or seed is None:
        seed = -1
    elif isinstance(seed, str):
        try:
            seed = int(seed)
        except Exception:
            seed = -1

    if seed == -1:
        return int(random.randrange(4294967294))

    return seed


def fix_seed(p):
    p.seed = get_fixed_seed(p.seed)
    p.subseed = get_fixed_seed(p.subseed)


def process_images(p: StableDiffusionProcessing) -> Processed:
    if p.scripts is not None:
        p.scripts.before_process(p)

    # if no checkpoint override or the override checkpoint can't be found, remove override entry and load opts checkpoint
    # and if after running refiner, the refiner model is not unloaded - webui swaps back to main model here, if model over is present it will be reloaded afterwards
    if sd_models.checkpoint_aliases.get(p.override_settings.get('sd_model_checkpoint')) is None:
        p.override_settings.pop('sd_model_checkpoint', None)
        sd_models.reload_model_weights()

    try:
        with runtime_utils.temporary_opts(p.override_settings, restore_afterwards=p.override_settings_restore_afterwards):
            for k in p.override_settings:
                if k == 'sd_model_checkpoint':
                    sd_models.reload_model_weights()
                if k == 'sd_vae':
                    sd_vae.reload_vae_weights()

            sd_models.apply_token_merging(p.sd_model, p.get_token_merging_ratio())

            # backwards compatibility, fix sampler and scheduler if invalid
            sd_samplers.fix_p_invalid_sampler_and_scheduler(p)

            with profiling.Profiler():
                from modules.runtime.runner import ProcessingRunner, ProcessingRequest
                runner = ProcessingRunner()
                request = ProcessingRequest(p)
                res = runner.run(request)
    finally:
        sd_models.apply_token_merging(p.sd_model, 0)

        if p.override_settings_restore_afterwards and 'sd_vae' in p.override_settings:
            sd_vae.reload_vae_weights()

    return res


def process_images_inner(p: StableDiffusionProcessing) -> Processed:
    """this is the main loop that both txt2img and img2img use; it calls func_init once inside all the scopes and func_sample once per batch"""

    if isinstance(p.prompt, list):
        assert(len(p.prompt) > 0)
    else:
        assert p.prompt is not None

    devices.torch_gc()

    p.seed = get_fixed_seed(p.seed)
    p.subseed = get_fixed_seed(p.subseed)

    if p.restore_faces is None:
        p.restore_faces = opts.face_restoration

    if p.tiling is None:
        p.tiling = opts.tiling

    if p.refiner_checkpoint not in (None, "", "None", "none"):
        p.refiner_checkpoint_info = sd_models.get_closet_checkpoint_match(p.refiner_checkpoint)
        if p.refiner_checkpoint_info is None:
            raise Exception(f'Could not find checkpoint with name {p.refiner_checkpoint}')

    m = _orchestration_model(p)
    if hasattr(m, 'fix_dimensions'):
        p.width, p.height = m.fix_dimensions(p.width, p.height)

    # M34: explicit model identity for runtime-owned seam (same source as pre-M34 lines below)
    model_identity = model_identity_from_model(m)
    p.sd_model_name = model_identity.name_for_extra
    p.sd_model_hash = model_identity.model_hash
    p.sd_vae_name = sd_vae.get_loaded_vae_name()
    p.sd_vae_hash = sd_vae.get_loaded_vae_hash()

    modules.sd_hijack.model_hijack.apply_circular(p.tiling)
    modules.sd_hijack.model_hijack.clear_comments()

    p.fill_fields_from_opts()
    p.setup_prompts()

    prompt_seed_prep.prepare_prompt_seed_state(p)
    p.opts_snapshot = create_opts_snapshot(shared.opts)
    p.runtime_context = RuntimeContext(
        model=m,
        model_identity=model_identity,
        opts_snapshot=p.opts_snapshot,
        device=shared.device,
        state=shared.state,
        cmd_opts=shared.cmd_opts,
    )

    if os.path.exists(cmd_opts.embeddings_dir) and not p.do_not_reload_embeddings:
        model_hijack.embedding_db.load_textual_inversion_embeddings()

    if p.scripts is not None:
        p.scripts.process(p)

    infotexts = []
    output_images = []
    for n, samples_ddim in processing_runtime.run_generation_batches(p):
        if p.scripts is not None:
            ps = scripts.PostSampleArgs(samples_ddim)
            p.scripts.post_sample(p, ps)
            samples_ddim = ps.samples

        x_samples_ddim = decode_runtime.decode_latents(p, samples_ddim)

        if p.scripts is not None:
            p.scripts.postprocess_batch(p, x_samples_ddim, batch_number=n)

            p.prompts = p.all_prompts[n * p.batch_size:(n + 1) * p.batch_size]
            p.negative_prompts = p.all_negative_prompts[n * p.batch_size:(n + 1) * p.batch_size]

            batch_params = scripts.PostprocessBatchListArgs(list(x_samples_ddim))
            p.scripts.postprocess_batch_list(p, batch_params, batch_number=n)
            x_samples_ddim = batch_params.images

        def infotext(index=0, use_main_prompt=False):
            return create_infotext(p, p.prompts, p.seeds, p.subseeds, use_main_prompt=use_main_prompt, index=index, all_negative_prompts=p.negative_prompts)

        save_samples = p.save_samples()

        for i, x_sample in enumerate(x_samples_ddim):
            p.batch_index = i

            x_sample = decode_runtime.postprocess_face_restore_row(p, x_sample, i, save_samples, infotext)

            image = Image.fromarray(x_sample)

            if p.scripts is not None:
                pp = scripts.PostprocessImageArgs(image)
                p.scripts.postprocess_image(p, pp)
                image = pp.image

            mask_for_overlay = getattr(p, "mask_for_overlay", None)

            if not shared.opts.overlay_inpaint:
                overlay_image = None
            elif getattr(p, "overlay_images", None) is not None and i < len(p.overlay_images):
                overlay_image = p.overlay_images[i]
            else:
                overlay_image = None

            if p.scripts is not None:
                ppmo = scripts.PostProcessMaskOverlayArgs(i, mask_for_overlay, overlay_image)
                p.scripts.postprocess_maskoverlay(p, ppmo)
                mask_for_overlay, overlay_image = ppmo.mask_for_overlay, ppmo.overlay_image

            # If the intention is to show the output from the model
            # that is being composited over the original image,
            # we need to keep the original image around
            # and use it in the composite step.
            image, original_denoised_image = decode_runtime.postprocess_images_for_row(p, image, i, save_samples, infotext, overlay_image)

            if p.scripts is not None:
                pp = scripts.PostprocessImageArgs(image)
                p.scripts.postprocess_image_after_composite(p, pp)
                image = pp.image

            decode_runtime.save_outputs_for_row(
                p,
                i,
                image,
                original_denoised_image,
                mask_for_overlay,
                save_samples,
                infotext,
                output_images,
                infotexts,
            )

        del x_samples_ddim

        devices.torch_gc()

    if not infotexts:
        infotexts.append(Processed(p, []).infotext(p, 0))

    p.color_corrections = None

    index_of_first_image = decode_runtime.save_outputs_grid(p, output_images, infotexts, infotext)

    if not p.disable_extra_networks and p.extra_network_data:
        extra_networks.deactivate(p, p.extra_network_data)

    devices.torch_gc()

    res = Processed(
        p,
        images_list=output_images,
        seed=p.all_seeds[0],
        info=infotexts[0],
        subseed=p.all_subseeds[0],
        index_of_first_image=index_of_first_image,
        infotexts=infotexts,
    )

    if p.scripts is not None:
        p.scripts.postprocess(p, res)

    return res
