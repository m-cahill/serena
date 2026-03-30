"""M40: targeted tests for StableDiffusionProcessing helpers in processing_types.

Imports are deferred until test body (after ``initialize``) so collection does not
load ``processing_types`` while ``shared.opts`` is still None.
"""

from __future__ import annotations


def _pick_sampler_name() -> str:
    from modules import sd_samplers

    names = sd_samplers.visible_sampler_names()
    if names:
        return names[0]
    return sd_samplers.all_samplers[0].name


def test_get_token_merging_ratio_non_hr_uses_instance_value(initialize, tmp_path):
    from modules.processing_types import StableDiffusionProcessingTxt2Img

    out = str(tmp_path / "o")
    p = StableDiffusionProcessingTxt2Img(
        outpath_samples=out,
        outpath_grids=out,
        prompt="",
        negative_prompt="",
        styles=[],
        seed=1,
        subseed=-1,
        sampler_name=_pick_sampler_name(),
        batch_size=1,
        n_iter=1,
        steps=1,
        cfg_scale=1.0,
        width=64,
        height=64,
        enable_hr=False,
        disable_extra_networks=True,
        do_not_save_samples=True,
        do_not_save_grid=True,
        restore_faces=False,
        do_not_reload_embeddings=True,
    )
    p.token_merging_ratio = 0.37
    assert p.get_token_merging_ratio() == 0.37


def test_get_token_merging_ratio_hr_prefers_hr_field(initialize, tmp_path):
    from modules.processing_types import StableDiffusionProcessingTxt2Img

    out = str(tmp_path / "o")
    p = StableDiffusionProcessingTxt2Img(
        outpath_samples=out,
        outpath_grids=out,
        prompt="",
        negative_prompt="",
        styles=[],
        seed=1,
        subseed=-1,
        sampler_name=_pick_sampler_name(),
        batch_size=1,
        n_iter=1,
        steps=1,
        cfg_scale=1.0,
        width=64,
        height=64,
        enable_hr=False,
        disable_extra_networks=True,
        do_not_save_samples=True,
        do_not_save_grid=True,
        restore_faces=False,
        do_not_reload_embeddings=True,
    )
    p.token_merging_ratio = 0.1
    p.token_merging_ratio_hr = 0.55
    assert p.get_token_merging_ratio(for_hr=True) == 0.55
