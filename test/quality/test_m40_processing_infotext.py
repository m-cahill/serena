"""M40: contract tests for modules/processing_infotext.

Imports are deferred until test body (after ``initialize``) so collection does not
load ``processing_infotext`` while ``shared.opts`` is still None.
"""

from __future__ import annotations


def _pick_sampler_name() -> str:
    from modules import sd_samplers

    names = sd_samplers.visible_sampler_names()
    if names:
        return names[0]
    return sd_samplers.all_samplers[0].name


def test_program_version_none_when_git_tag_is_none(monkeypatch, initialize):
    import launch

    monkeypatch.setattr(launch, "git_tag", lambda: "<none>")
    from modules.processing_infotext import program_version

    assert program_version() is None


def test_program_version_returns_resolved_tag(monkeypatch, initialize):
    import launch

    monkeypatch.setattr(launch, "git_tag", lambda: "v0-test")
    from modules.processing_infotext import program_version

    assert program_version() == "v0-test"


def test_create_infotext_includes_prompt_and_steps(initialize, tmp_path):
    """Smoke: infotext string contains core fields after full stack init."""
    from modules.processing_infotext import create_infotext
    from modules.processing_types import StableDiffusionProcessingTxt2Img

    out_dir = str(tmp_path / "out")
    p = StableDiffusionProcessingTxt2Img(
        outpath_samples=out_dir,
        outpath_grids=out_dir,
        prompt="m40 infotext",
        negative_prompt="",
        styles=[],
        seed=1,
        subseed=-1,
        sampler_name=_pick_sampler_name(),
        batch_size=1,
        n_iter=1,
        steps=5,
        cfg_scale=7.0,
        width=64,
        height=64,
        enable_hr=False,
        disable_extra_networks=True,
        do_not_save_samples=True,
        do_not_save_grid=True,
        restore_faces=False,
        do_not_reload_embeddings=True,
    )
    p.setup_prompts()
    p.all_seeds = [1]
    p.all_subseeds = [1]
    p.sd_model_hash = "abc"
    p.sd_model_name = "test-model"
    p.sd_vae_hash = None
    p.sd_vae_name = None
    p.user = None
    p.extra_generation_params = {}

    text = create_infotext(
        p,
        p.all_prompts,
        p.all_seeds,
        p.all_subseeds,
    )
    assert "m40 infotext" in text
    assert "Steps" in text and "5" in text
    assert p.sampler_name in text
