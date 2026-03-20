"""M20: ProcessingRunner + fake ModelProvider — full inner pipeline without real weights/GPU."""

from __future__ import annotations

import numpy as np
import pytest

from modules.runtime.model_provider import ModelProvider
from modules.runtime.runner import ProcessingRequest, ProcessingRunner
from test.fixtures.fake_model import FakeModel, FakeModelProvider


class _FakeSampler:
    """Bypasses k-diffusion; returns pre-decoded RGB tensors (DecodedSamples / already_decoded)."""

    def sample(self, p, x, conditioning, unconditional_conditioning, image_conditioning=None):
        import torch

        from modules.runtime.decode_runtime import DecodedSamples

        b = x.shape[0]
        h, w = p.height, p.width
        tensors = [torch.full((3, h, w), 0.0, dtype=torch.float32) for _ in range(b)]
        return DecodedSamples(tensors)


def _pick_sampler_name() -> str:
    from modules import sd_samplers

    names = sd_samplers.visible_sampler_names()
    if names:
        return names[0]
    return sd_samplers.all_samplers[0].name


def _minimal_setup_conds(self):
    import torch

    from modules import devices, sd_samplers

    sampler_config = sd_samplers.find_sampler_config(self.sampler_name)
    total_steps = sampler_config.total_steps(self.steps) if sampler_config else self.steps
    steps = max(self.steps, 1)
    self.step_multiplier = max(total_steps // steps, 1)
    self.firstpass_steps = total_steps
    z = torch.zeros(1, device=devices.device, dtype=devices.dtype)
    self.uc = (z,)
    self.c = (z,)


def _make_txt2img(out_samples: str, *, sampler_name: str):
    from modules import processing as proc_mod

    p = proc_mod.StableDiffusionProcessingTxt2Img(
        outpath_samples=out_samples,
        outpath_grids=out_samples,
        prompt="m20 fake runtime",
        negative_prompt="",
        styles=[],
        seed=42,
        subseed=-1,
        sampler_name=sampler_name,
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
    p.scripts = None
    return p


def _null_autocast(disable=False):
    """CPU-only CI: avoid torch.autocast('cuda') / without_autocast cuda contexts."""
    import contextlib

    return contextlib.nullcontext()


@pytest.fixture
def fake_pipeline_env(monkeypatch, tmp_path, initialize):
    """Stubs shared.sd_model, reload, CLIP conditioning, and sampler creation for a CPU-only path."""
    import modules.shared as shared
    from modules import devices as devices_mod
    from modules import processing as proc_mod
    from modules import sd_models, sd_samplers

    prev = shared.sd_model
    fake = FakeModel()
    shared.sd_model = fake

    monkeypatch.setattr(devices_mod, "autocast", _null_autocast)
    monkeypatch.setattr(devices_mod, "without_autocast", _null_autocast)
    monkeypatch.setattr(sd_models, "reload_model_weights", lambda *a, **k: None)
    monkeypatch.setattr(sd_samplers, "create_sampler", lambda name, model: _FakeSampler())
    monkeypatch.setattr(proc_mod.StableDiffusionProcessing, "setup_conds", _minimal_setup_conds)
    if hasattr(shared.cmd_opts, "no_prompt_history"):
        monkeypatch.setattr(shared.cmd_opts, "no_prompt_history", True)
    if hasattr(shared.opts, "randn_source"):
        monkeypatch.setattr(shared.opts, "randn_source", "CPU")

    try:
        yield fake, str(tmp_path)
    finally:
        shared.sd_model = prev


def _assert_processed_equivalent(a, b):
    assert len(a.images) == len(b.images)
    assert a.seed == b.seed
    for img_a, img_b in zip(a.images, b.images):
        assert img_a.size == img_b.size
        assert np.array_equal(np.array(img_a), np.array(img_b))


def test_full_pipeline_runner_fake_model(fake_pipeline_env):
    fake, out = fake_pipeline_env
    provider = FakeModelProvider(fake)
    p = _make_txt2img(out, sampler_name=_pick_sampler_name())
    runner = ProcessingRunner(model_provider=provider)
    result = runner.run(ProcessingRequest(p))
    assert result is not None
    assert len(result.images) >= 1
    assert all(hasattr(im, "size") for im in result.images)


def test_runner_deterministic_structural_output(fake_pipeline_env):
    fake, out = fake_pipeline_env
    provider = FakeModelProvider(fake)
    sampler = _pick_sampler_name()

    runner = ProcessingRunner(model_provider=provider)
    p1 = _make_txt2img(out, sampler_name=sampler)
    p2 = _make_txt2img(out, sampler_name=sampler)
    r1 = runner.run(ProcessingRequest(p1))
    r2 = runner.run(ProcessingRequest(p2))
    _assert_processed_equivalent(r1, r2)


def test_runner_propagates_provider_error(fake_pipeline_env):
    _, out = fake_pipeline_env

    class Boom(Exception):
        pass

    class BadProvider(ModelProvider):
        def get_model(self, p):
            raise Boom("expected")

    p = _make_txt2img(out, sampler_name=_pick_sampler_name())
    runner = ProcessingRunner(model_provider=BadProvider())
    with pytest.raises(Boom, match="expected"):
        runner.run(ProcessingRequest(p))


def test_fake_model_provider_get_model_called(fake_pipeline_env):
    fake, out = fake_pipeline_env
    provider = FakeModelProvider(fake, track_calls=True)
    p = _make_txt2img(out, sampler_name=_pick_sampler_name())
    runner = ProcessingRunner(model_provider=provider)
    runner.run(ProcessingRequest(p))
    assert len(provider.get_model_calls) >= 1
