"""M40: regression/contract tests for modules/processing_helpers (pure + _eff_opts).

Imports are deferred to each test body after the ``initialize`` fixture so
collection does not load ``processing_helpers`` (and transitively ``sd_models``)
before ``shared.opts`` / full stack init.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock


def test_old_hires_fix_first_pass_dimensions_scales_to_512_area(initialize):
    from modules.processing_helpers import old_hires_fix_first_pass_dimensions

    w, h = old_hires_fix_first_pass_dimensions(256, 256)
    assert w % 64 == 0 and h % 64 == 0
    assert w * h >= 512 * 512 * 0.9


def test_create_binary_mask_rgb_to_l(initialize):
    from PIL import Image

    from modules.processing_helpers import create_binary_mask

    img = Image.new("RGB", (4, 4), color="white")
    m = create_binary_mask(img, round=True)
    assert m.mode == "L"


def test_create_binary_mask_rgba_alpha_round(initialize):
    from PIL import Image

    from modules.processing_helpers import create_binary_mask

    img = Image.new("RGBA", (4, 4), color=(255, 255, 255, 128))
    m = create_binary_mask(img, round=True)
    assert m.mode == "L"


def test_create_binary_mask_rgba_alpha_no_round(initialize):
    from PIL import Image

    from modules.processing_helpers import create_binary_mask

    img = Image.new("RGBA", (4, 4), color=(255, 255, 255, 128))
    m = create_binary_mask(img, round=False)
    assert m.mode == "L"


def test_create_binary_mask_rgba_opaque_skips_threshold(initialize):
    from PIL import Image

    from modules.processing_helpers import create_binary_mask

    img = Image.new("RGBA", (4, 4), color=(0, 0, 0, 255))
    m = create_binary_mask(img, round=True)
    assert m.mode == "L"


def test_apply_overlay_none_returns_tuple(initialize):
    from PIL import Image

    from modules.processing_helpers import apply_overlay

    im = Image.new("RGB", (8, 8), color="blue")
    out, orig = apply_overlay(im, None, None)
    assert out is im
    assert orig.size == im.size


def test_uncrop_resizes_and_pastes(initialize, monkeypatch):
    from PIL import Image

    import modules.processing_helpers as ph

    def fake_resize(resize_mode, img, w, h):
        return img.resize((w, h))

    monkeypatch.setattr(ph.images, "resize_image", fake_resize)

    src = Image.new("RGB", (10, 10), color="red")
    out = ph.uncrop(src, (30, 30), (2, 3, 10, 10))
    assert out.size == (30, 30)
    assert out.mode == "RGBA"


def test_eff_opts_view_prefers_snapshot_attrs(initialize):
    from modules import shared
    from modules.processing_helpers import _EffOptsView

    snap = SimpleNamespace(foo="snap", shared_only=None)
    fb = shared.opts
    v = _EffOptsView(snap, fb)
    assert v.foo == "snap"


def test_eff_opts_view_falls_back_for_missing_keys(initialize):
    from modules import shared
    from modules.processing_helpers import _EffOptsView

    snap = SimpleNamespace()
    fb = shared.opts
    v = _EffOptsView(snap, fb)
    assert v.CLIP_stop_at_last_layers == shared.opts.CLIP_stop_at_last_layers


def test_eff_opts_without_snapshot_is_shared_opts(initialize):
    from modules import shared
    from modules.processing_helpers import _eff_opts

    class P:
        pass

    p = P()
    assert _eff_opts(p) is shared.opts


def test_eff_opts_with_snapshot_returns_eff_opts_view(initialize):
    from modules.processing_helpers import _EffOptsView, _eff_opts

    class P:
        pass

    p = P()
    p.opts_snapshot = SimpleNamespace()
    r = _eff_opts(p)
    assert isinstance(r, _EffOptsView)


def test_orchestration_model_uses_provider_when_present(initialize):
    from modules.processing_helpers import _orchestration_model

    got = object()
    mp = MagicMock()
    mp.get_model = lambda p: got

    class P:
        model_provider = mp

    p = P()
    assert _orchestration_model(p) is got


def test_orchestration_model_falls_back_without_provider(initialize, monkeypatch):
    from modules import shared
    from modules.processing_helpers import _orchestration_model

    sentinel = object()
    monkeypatch.setattr(shared, "sd_model", sentinel)

    class P:
        pass

    p = P()
    assert _orchestration_model(p) is sentinel


def test_create_random_tensors_shape_and_determinism(initialize):
    from modules.processing_helpers import create_random_tensors

    shape = (1, 2, 2)
    t1 = create_random_tensors(shape, [1])
    t2 = create_random_tensors(shape, [1])
    assert t1.shape == t2.shape
    assert tuple(t1.shape[-3:]) == shape
    assert (t1 == t2).all()
