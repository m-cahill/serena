"""M22 contract tests: txt2img/img2img modular builders (no full Gradio render)."""
from __future__ import annotations

from pathlib import Path

from modules import ui_tab_registry as utr
from modules import ui_txt2img_tab
from modules.ui_tab_build_result import TabBuildResult

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _six_placeholders():
    return [object() for _ in range(6)]


def test_core_tab_specs_labels_unchanged_m22():
    """Core segment labels/ifids still match M21 baseline (registry shape frozen)."""
    a, b, c, d, e, f = _six_placeholders()
    specs = utr.core_tab_specs(a, b, c, d, e, f)
    assert [(s.label, s.ifid, s.source) for s in specs] == [
        ("txt2img", "txt2img", "core"),
        ("img2img", "img2img", "core"),
        ("Extras", "extras", "core"),
        ("PNG Info", "pnginfo", "core"),
        ("Checkpoint Merger", "modelmerger", "core"),
        ("Train", "train", "core"),
    ]


def test_pre_sort_labels_match_m21_contract():
    """Pre-sort label sequence unchanged (core → extension → Settings → Extensions)."""
    t2, i2, ex, png, mm, tr = _six_placeholders()
    ext_tab = object()
    settings_i = object()
    extensions_i = object()
    rows = [(ext_tab, "Custom", "custom")]
    tuples = utr.build_top_level_interface_tuples(
        t2, i2, ex, png, mm, tr,
        rows,
        settings_i,
        extensions_i,
    )
    assert [t[1] for t in tuples] == [
        "txt2img",
        "img2img",
        "Extras",
        "PNG Info",
        "Checkpoint Merger",
        "Train",
        "Custom",
        "Settings",
        "Extensions",
    ]


def test_create_ui_source_uses_modular_tab_builders():
    """create_ui must build txt2img/img2img via tab modules (source contract)."""
    src = (_REPO_ROOT / "modules" / "ui.py").read_text(encoding="utf-8")
    assert "ui_txt2img_tab.create_txt2img_tab()" in src
    assert "ui_img2img_tab.create_img2img_tab()" in src
    assert "ui_img2img_tab.img2img_dummy_component" in src


def test_patched_txt2img_builder_flows_into_registry_tuples(monkeypatch):
    """Modular txt2img interface object is what the registry list uses (first slot)."""
    sentinel = object()
    dummy = object()

    def fake_txt2img():
        return TabBuildResult(sentinel, "txt2img", "txt2img", dummy)

    monkeypatch.setattr(ui_txt2img_tab, "create_txt2img_tab", fake_txt2img)
    t = ui_txt2img_tab.create_txt2img_tab()
    i2, ex, png, mm, tr = (object() for _ in range(5))
    out = utr.build_top_level_interface_tuples(
        t.interface, i2, ex, png, mm, tr,
        [],
        object(),
        object(),
    )
    assert out[0][0] is sentinel
    assert out[0][1] == "txt2img"

