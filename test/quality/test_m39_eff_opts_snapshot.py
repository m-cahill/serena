"""M39: _eff_opts routes supported-path reads through opts_snapshot when set."""

from __future__ import annotations

from pathlib import Path


def _read(rel: str) -> str:
    return (Path(__file__).resolve().parents[2] / rel).read_text(encoding="utf-8")


def test_processing_helpers_defines_eff_opts():
    src = _read("modules/processing_helpers.py")
    assert "def _eff_opts(p):" in src
    assert "opts_snapshot" in src
    assert "return shared.opts" in src


def test_processing_types_has_no_direct_shared_opts_reads():
    """Contract: migrated M39 reads use _eff_opts, not shared.opts in processing_types."""
    src = _read("modules/processing_types.py")
    assert "shared.opts" not in src
    assert "_eff_opts" in src


def test_process_images_inner_overlay_uses_eff_opts():
    src = _read("modules/processing.py")
    assert "_eff_opts(p).overlay_inpaint" in src
    assert "shared.opts.overlay_inpaint" not in src


def test_processing_infotext_inpainting_mask_uses_eff_opts():
    src = _read("modules/processing_infotext.py")
    assert "_eff_opts(p).inpainting_mask_weight" in src
    assert "shared.opts.inpainting_mask_weight" not in src


def test_processing_runtime_preview_gate_uses_eff_opts():
    src = _read("modules/runtime/processing_runtime.py")
    assert "_eff_opts(p)" in src
    assert "shared.opts.live_previews_enable" not in src
