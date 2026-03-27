"""M20: ProcessingRunner + fake ModelProvider — inner pipeline without real weights."""

from __future__ import annotations

import numpy as np
import pytest

from modules.runtime.model_provider import ModelProvider
from modules.runtime.runner import ProcessingRequest, ProcessingRunner
from modules.runtime_context import ModelIdentity, model_identity_from_model
from test.fixtures.fake_model import FakeModel, FakeModelProvider


class _FakeSampler:
    """Bypass k-diffusion; return DecodedSamples (already_decoded)."""

    def sample(
        self,
        p,
        x,
        conditioning,
        unconditional_conditioning,
        image_conditioning=None,
    ):
        import torch

        from modules.runtime.decode_runtime import DecodedSamples

        b = x.shape[0]
        h, w = p.height, p.width
        tensors = [
            torch.full((3, h, w), 0.0, dtype=torch.float32) for _ in range(b)
        ]
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
    if sampler_config:
        total_steps = sampler_config.total_steps(self.steps)
    else:
        total_steps = self.steps
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
    """CPU-only CI: skip torch.autocast('cuda') contexts."""
    import contextlib

    return contextlib.nullcontext()


def _noop_reload(*a, **k):
    return None


def _fake_create_sampler(name, model):
    return _FakeSampler()


# Minimal opts.data in CI can omit keys decode_runtime reads from p.opts_snapshot.
_OPTS_SNAPSHOT_DEFAULTS = {
    "grid_only_if_multiple": True,
    "return_grid": False,
    "grid_save": False,
    "grid_format": "png",
    "grid_extended_filename": False,
    "save_images_before_face_restoration": False,
    "samples_format": "png",
    "save_images_before_color_correction": False,
    "return_mask": False,
    "save_mask": False,
    "return_mask_composite": False,
    "save_mask_composite": False,
}


def _create_opts_snapshot_patched(opts):
    from modules.opts_snapshot import create_opts_snapshot as _real

    ns = _real(opts)
    for key, val in _OPTS_SNAPSHOT_DEFAULTS.items():
        if not hasattr(ns, key):
            setattr(ns, key, val)
    return ns


@pytest.fixture
def fake_pipeline_env(monkeypatch, tmp_path, initialize):
    """Stub shared.sd_model, reload, conditioning, sampler; CPU-safe."""
    import modules.shared as shared
    from modules import devices as devices_mod
    from modules import processing as proc_mod
    from modules import sd_models, sd_samplers

    prev = shared.sd_model
    fake = FakeModel()
    shared.sd_model = fake

    monkeypatch.setattr(devices_mod, "autocast", _null_autocast)
    monkeypatch.setattr(devices_mod, "without_autocast", _null_autocast)
    monkeypatch.setattr(sd_models, "reload_model_weights", _noop_reload)
    monkeypatch.setattr(sd_samplers, "create_sampler", _fake_create_sampler)
    monkeypatch.setattr(proc_mod, "create_opts_snapshot", _create_opts_snapshot_patched)
    monkeypatch.setattr(
        proc_mod.StableDiffusionProcessing,
        "setup_conds",
        _minimal_setup_conds,
    )
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


def test_model_identity_from_model_matches_checkpoint_fields():
    fake = FakeModel()
    mi = model_identity_from_model(fake)
    assert isinstance(mi, ModelIdentity)
    assert mi.name_for_extra == fake.sd_checkpoint_info.name_for_extra
    assert mi.model_hash == fake.sd_model_hash


def test_full_pipeline_populates_runtime_context_model_identity(fake_pipeline_env):
    fake, out = fake_pipeline_env
    provider = FakeModelProvider(fake)
    p = _make_txt2img(out, sampler_name=_pick_sampler_name())
    runner = ProcessingRunner(model_provider=provider)
    runner.run(ProcessingRequest(p))

    rc = p.runtime_context
    assert rc.model_identity is not None
    assert rc.model_identity.name_for_extra == fake.sd_checkpoint_info.name_for_extra
    assert rc.model_identity.model_hash == fake.sd_model_hash
    assert p.sd_model_name == rc.model_identity.name_for_extra
    assert p.sd_model_hash == rc.model_identity.model_hash
    assert rc.model is fake


def test_model_identity_available_before_script_hooks(fake_pipeline_env):
    """RuntimeContext.model_identity exists before scripts.process and batch hooks."""
    fake, out = fake_pipeline_env
    provider = FakeModelProvider(fake)
    p = _make_txt2img(out, sampler_name=_pick_sampler_name())

    seen = []

    class _Scripts:
        def process(self, p):
            assert p.runtime_context is not None
            assert p.runtime_context.model_identity is not None
            assert p.runtime_context.model_identity.name_for_extra == p.sd_model_name
            seen.append("process")

        def before_process_batch(self, p, **kwargs):
            assert p.runtime_context.model_identity is not None
            seen.append("before_process_batch")

        def process_batch(self, p, **kwargs):
            pass

    p.scripts = _Scripts()
    runner = ProcessingRunner(model_provider=provider)
    runner.run(ProcessingRequest(p))
    assert seen == ["process", "before_process_batch"]
