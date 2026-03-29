"""M40: narrow runtime tests for modules/runtime/processing_runtime.py."""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

try:
    import modules.runtime.processing_runtime as _m40_prt_import_check  # noqa: F401
except ImportError:
    pytest.skip(
        "Quality CI dependency tree required for modules.runtime.processing_runtime",
        allow_module_level=True,
    )


def test_run_generation_batches_yields_nothing_when_prompt_slice_empty(monkeypatch):
    """First batch with empty prompt slice exits before yield (regression guard)."""
    import modules.runtime.processing_runtime as pr
    import modules.shared as shared

    st = SimpleNamespace(job_count=-1, skipped=False, interrupted=False, stopping_generation=False)
    monkeypatch.setattr(shared, "state", st)

    monkeypatch.setattr(
        pr,
        "_eff_opts",
        lambda p: SimpleNamespace(live_previews_enable=False, show_progress_type=""),
    )
    monkeypatch.setattr(pr, "sd_vae_approx", MagicMock())
    monkeypatch.setattr(pr, "sd_unet", MagicMock())
    monkeypatch.setattr(pr, "sd_models", MagicMock(reload_model_weights=lambda: None))

    monkeypatch.setattr(
        pr.devices,
        "autocast",
        lambda *a, **k: contextlib.nullcontext(),
    )

    @contextlib.contextmanager
    def ema_cm():
        yield None

    mock_model = MagicMock()
    mock_model.ema_scope = lambda: ema_cm()
    mp = MagicMock()
    mp.get_model = lambda p: mock_model

    p = MagicMock()
    p.model_provider = mp
    p.n_iter = 1
    p.batch_size = 1
    p.all_prompts = []
    p.all_negative_prompts = []
    p.all_seeds = []
    p.all_subseeds = []
    p.subseed_strength = 0
    p.seed_resize_from_h = -1
    p.seed_resize_from_w = -1
    p.init = MagicMock()
    p.scripts = None
    p.disable_extra_networks = True
    p.extra_generation_params = {}
    p.parse_extra_network_prompts = MagicMock()

    gen = pr.run_generation_batches(p)
    assert list(gen) == []


def test_preview_approx_nn_branch_calls_sd_vae_approx(monkeypatch):
    """When live previews + Approx NN, sd_vae_approx.model() is invoked once."""
    import modules.runtime.processing_runtime as pr
    import modules.shared as shared

    st = SimpleNamespace(job_count=-1, skipped=False, interrupted=False, stopping_generation=False)
    monkeypatch.setattr(shared, "state", st)

    vae_calls = []

    def record_vae():
        vae_calls.append(1)

    fake_eff = SimpleNamespace(live_previews_enable=True, show_progress_type="Approx NN")
    monkeypatch.setattr(pr, "_eff_opts", lambda p: fake_eff)
    monkeypatch.setattr(pr, "sd_vae_approx", MagicMock(model=record_vae))
    monkeypatch.setattr(pr, "sd_unet", MagicMock())
    monkeypatch.setattr(pr, "sd_models", MagicMock(reload_model_weights=lambda: None))

    monkeypatch.setattr(
        pr.devices,
        "autocast",
        lambda *a, **k: contextlib.nullcontext(),
    )

    @contextlib.contextmanager
    def ema_cm():
        yield None

    mock_model = MagicMock()
    mock_model.ema_scope = lambda: ema_cm()
    mp = MagicMock()
    mp.get_model = lambda p: mock_model

    p = MagicMock()
    p.model_provider = mp
    p.n_iter = 1
    p.batch_size = 1
    p.all_prompts = []
    p.all_negative_prompts = []
    p.all_seeds = []
    p.all_subseeds = []
    p.subseed_strength = 0
    p.seed_resize_from_h = -1
    p.seed_resize_from_w = -1
    p.init = MagicMock()
    p.scripts = None
    p.disable_extra_networks = True
    p.extra_generation_params = {}
    p.parse_extra_network_prompts = MagicMock()

    list(pr.run_generation_batches(p))
    assert len(vae_calls) == 1
