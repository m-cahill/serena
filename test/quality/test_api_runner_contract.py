"""M14 contract test: API txt2img path uses ProcessingRunner.

Verifies that the API execution path flows through process_images → runner,
not direct process_images_inner calls. No routing changes; verification only.
"""
from threading import Lock


def test_api_txt2img_uses_runner(monkeypatch, initialize):
    """API txt2img path invokes ProcessingRunner when process_images is called."""
    from fastapi import FastAPI

    from modules.api.api import Api
    from modules.api import models
    from modules.processing import Processed
    from modules.runtime.runner import ProcessingRunner

    called = {"run": False}

    # Force real execution path (bypass CI early return)
    monkeypatch.setenv("CI", "false")

    # Patch runner to track invocation
    original_run = ProcessingRunner.run

    def tracking_run(self, request):
        called["run"] = True
        return original_run(self, request)

    monkeypatch.setattr(ProcessingRunner, "run", tracking_run)

    # Mock process_images_inner to avoid full pipeline
    def fake_inner(proc):
        return Processed(proc, [], seed=-1, info="", comments="")

    import modules.processing as proc_mod

    monkeypatch.setattr(proc_mod, "process_images_inner", fake_inner)

    # Mock model reload and token merging to avoid model/device ops
    import modules.sd_models as sd_models_mod

    monkeypatch.setattr(sd_models_mod, "reload_model_weights", lambda: None)
    monkeypatch.setattr(sd_models_mod, "apply_token_merging", lambda m, r: None)

    # Call API method directly (no HTTP)
    app = FastAPI()
    api = Api(app, Lock())

    req = models.StableDiffusionTxt2ImgProcessingAPI(
        prompt="test",
        steps=1,
        width=64,
        height=64,
    )

    result = api.text2imgapi(req)

    assert called["run"] is True
    assert result is not None
    assert hasattr(result, "images")
    assert hasattr(result, "info")
