"""M19: Model provider injection and runtime model access.

M36: Behavior tests for ModelProvider / SharedModelProvider and
``processing._orchestration_model`` (M35 seam).
"""

from types import SimpleNamespace

import pytest

from modules.runtime.runner import ProcessingRequest, ProcessingRunner
from modules.runtime import sampler_runtime
from modules.runtime.model_provider import ModelProvider, SharedModelProvider
from modules.runtime_context import ModelIdentity, RuntimeContext, model_identity_from_model
from test.fixtures.fake_model import FakeModel


def test_shared_model_provider_get_model_returns_shared_sd_model():
    import inspect

    src = inspect.getsource(SharedModelProvider.get_model)
    assert "shared.sd_model" in src


def test_model_provider_get_model_not_implemented():
    with pytest.raises(NotImplementedError):
        ModelProvider().get_model(SimpleNamespace())


def test_shared_model_provider_returns_current_shared_sd_model(initialize):
    import modules.shared as shared

    prev = shared.sd_model
    sentinel = object()
    try:
        shared.sd_model = sentinel
        out = SharedModelProvider().get_model(SimpleNamespace())
        assert out is sentinel
    finally:
        shared.sd_model = prev


def test_orchestration_model_falls_back_to_shared_when_no_provider(initialize):
    from modules import processing as proc_mod

    import modules.shared as shared

    prev = shared.sd_model
    sentinel = object()
    try:
        shared.sd_model = sentinel
        p = SimpleNamespace()
        assert proc_mod._orchestration_model(p) is sentinel
    finally:
        shared.sd_model = prev


def test_orchestration_model_uses_provider_when_set(initialize):
    from modules import processing as proc_mod

    fake = FakeModel()

    class MP:
        def get_model(self, p):
            return fake

    p = SimpleNamespace(model_provider=MP())
    assert proc_mod._orchestration_model(p) is fake


def test_model_identity_equality_and_hash():
    a = ModelIdentity(name_for_extra="a", model_hash="h1")
    b = ModelIdentity(name_for_extra="a", model_hash="h1")
    c = ModelIdentity(name_for_extra="b", model_hash="h1")
    assert a == b
    assert hash(a) == hash(b)
    assert a != c


def test_runtime_context_holds_model_identity():
    fake = FakeModel()
    mi = model_identity_from_model(fake)
    snap = object()
    dev = object()
    st = object()
    co = object()
    rc = RuntimeContext(
        model=fake,
        model_identity=mi,
        opts_snapshot=snap,
        device=dev,
        state=st,
        cmd_opts=co,
    )
    assert rc.model is fake
    assert rc.model_identity is mi
    assert rc.opts_snapshot is snap
    assert rc.device is dev
    assert rc.state is st
    assert rc.cmd_opts is co


def test_runner_prepare_attaches_model_provider():
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
