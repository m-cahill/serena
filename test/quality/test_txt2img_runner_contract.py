"""M13 contract test: txt2img path uses ProcessingRunner.

Verifies that the txt2img execution path flows through process_images → runner,
not direct process_images_inner calls.
"""
from modules.runtime.runner import ProcessingRunner


def test_txt2img_path_uses_runner(monkeypatch, initialize):
    """txt2img path invokes ProcessingRunner when process_images is called."""
    from modules.processing import (
        StableDiffusionProcessingTxt2Img,
        process_images,
        Processed,
    )

    calls = []

    class TestRunner(ProcessingRunner):
        def execute(self, state):
            calls.append("runner_execute")
            return super().execute(state)

    monkeypatch.setattr(
        "modules.runtime.runner.ProcessingRunner",
        TestRunner,
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

    # Mock process_images_inner to avoid full pipeline (model, device, etc.)
    def fake_inner(proc):
        return Processed(proc, [], seed=-1, info="", comments="")

    import modules.processing as proc_mod
    monkeypatch.setattr(proc_mod, "process_images_inner", fake_inner)

    # Mock model reload to avoid loading weights
    import modules.sd_models as sd_models_mod
    monkeypatch.setattr(sd_models_mod, "reload_model_weights", lambda: None)

    process_images(p)

    assert "runner_execute" in calls
