"""M13 contract test: txt2img path uses ProcessingRunner.

Verifies that the txt2img execution path flows through process_images → runner,
not direct process_images_inner calls.
"""


def test_txt2img_path_uses_runner(monkeypatch, initialize):
    """txt2img path invokes ProcessingRunner when process_images is called."""
    from modules.processing import (
        StableDiffusionProcessingTxt2Img,
        process_images,
    )

    calls = []

    # Avoid real pipeline: patch runner.execute. Record the call here — do not
    # replace ProcessingRunner with a subclass and then patch .execute again;
    # the second patch overwrites the subclass method (M29.2 Quality failure).
    def fake_execute(self, state):
        from modules.processing import Processed

        calls.append("runner_execute")
        return Processed(state.processing, [], seed=-1, info="", comments="")

    monkeypatch.setattr(
        "modules.runtime.runner.ProcessingRunner.execute",
        fake_execute,
    )

    # Minimal processing object matching txt2img path
    p = StableDiffusionProcessingTxt2Img(
        sd_model=None,
        prompt="test",
        override_settings={},
        steps=1,
        width=64,
        height=64,
        extra_generation_params={},
    )
    p.scripts = None
    p.comments = []

    # Mock reload + token merge so None sd_model does not touch device
    import modules.sd_models as sd_models_mod
    monkeypatch.setattr(sd_models_mod, "reload_model_weights", lambda: None)
    monkeypatch.setattr(
        sd_models_mod, "apply_token_merging", lambda m, r: None
    )

    process_images(p)

    assert "runner_execute" in calls
