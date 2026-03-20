"""Contract tests for M21 top-level UI tab registry (no Gradio render)."""
from __future__ import annotations

from pathlib import Path

from modules import ui_tab_registry as utr

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _six_placeholders():
    return [object() for _ in range(6)]


def test_core_tab_specs_order_and_ids():
    """Contract A (core segment): fixed labels and ids for the six built-in tabs."""
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
    assert [s.interface for s in specs] == [a, b, c, d, e, f]


def test_merge_inserts_extension_after_core():
    core = [
        utr.TabSpec(object(), "txt2img", "txt2img", "core"),
        utr.TabSpec(object(), "img2img", "img2img", "core"),
    ]
    ext_iface = object()
    extension = [utr.TabSpec(ext_iface, "Ext", "ext", "extension")]
    merged = utr.merge_extension_tabs(core, extension)
    assert [s.label for s in merged] == ["txt2img", "img2img", "Ext"]
    assert merged[2].interface is ext_iface


def test_full_pre_sort_labels_contract_a():
    """Pre-sort tab label sequence: core → extension rows → Settings → Extensions."""
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
    labels = [t[1] for t in tuples]
    assert labels == [
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


def test_create_ui_source_uses_registry_assembly():
    """create_ui must assemble top-level tabs via ui_tab_registry (source contract)."""
    src = (_REPO_ROOT / "modules" / "ui.py").read_text(encoding="utf-8")
    assert "ui_tab_registry.build_top_level_interface_tuples" in src


def test_core_tab_specs_monkeypatch_drives_assembly(monkeypatch):
    """Sentinel core list from patched core_tab_specs appears at start of output."""
    sentinel = object()

    def fake_core(*_a, **_k):
        return [utr.TabSpec(sentinel, "sentinel", "sentinel", "core")]

    monkeypatch.setattr(utr, "core_tab_specs", fake_core)
    s_if, e_if = object(), object()
    out = utr.build_top_level_interface_tuples(
        object(), object(), object(), object(), object(), object(),
        [],
        s_if,
        e_if,
    )
    assert out[0][0] is sentinel
    assert out[0][1] == "sentinel"
    assert [t[1] for t in out] == ["sentinel", "Settings", "Extensions"]
