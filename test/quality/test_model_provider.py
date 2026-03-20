"""M19: Model provider injection and runtime model access."""

from modules.runtime.runner import ProcessingRequest, ProcessingRunner
from modules.runtime import sampler_runtime


def test_shared_model_provider_get_model_returns_shared_sd_model():
    import inspect

    from modules.runtime.model_provider import SharedModelProvider

    src = inspect.getsource(SharedModelProvider.get_model)
    assert "shared.sd_model" in src


def test_runner_prepare_attaches_model_provider():
    from modules.runtime.model_provider import SharedModelProvider

    proc = type("Proc", (), {})()
    runner = ProcessingRunner()
    state = runner.prepare(ProcessingRequest(proc))
    assert state.processing.model_provider is runner.model_provider
    assert isinstance(runner.model_provider, SharedModelProvider)


def test_sampler_runtime_uses_model_provider(monkeypatch):
    captured = {}
    sentinel = object()

    class MockSampler:
        def sample(self, p, x, c, uc, image_conditioning=None):
            return []

    def fake_create_sampler(name, model):
        captured["model"] = model
        return MockSampler()

    monkeypatch.setattr("modules.sd_samplers.create_sampler", fake_create_sampler)

    class MP:
        def get_model(self, p):
            return sentinel

    class P:
        sampler_name = "Euler"
        model_provider = MP()

        def txt2img_image_conditioning(self, x):
            return None

    p = P()
    sampler_runtime.run_sampler_txt2img(p, None, None, None)
    assert captured["model"] is sentinel


def test_sampler_img2img_hr_path_uses_model_provider(monkeypatch):
    captured = {}
    sentinel = object()

    class MockSampler:
        def sample_img2img(self, p, x, noise, c, uc, steps=None, image_conditioning=None):
            return []

    def fake_create_sampler(name, model):
        captured["model"] = model
        return MockSampler()

    monkeypatch.setattr("modules.sd_samplers.create_sampler", fake_create_sampler)

    class MP:
        def get_model(self, p):
            return sentinel

    class P:
        sampler_name = "Euler"
        model_provider = MP()
        sampler = None

    p = P()
    sampler_runtime.run_sampler_img2img(p, None, None, None, None, sampler_name="Euler")
    assert captured["model"] is sentinel
