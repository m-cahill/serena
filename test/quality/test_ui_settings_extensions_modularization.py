"""M23 contract tests: Settings/Extensions modular builders (no full Gradio render)."""
from __future__ import annotations

from pathlib import Path

from modules import ui_extensions_tab
from modules import ui_settings_tab
from modules import ui_tab_registry as utr
from modules.ui_tab_build_result import TabBuildResult

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _six_placeholders():
    return [object() for _ in range(6)]


def test_pre_sort_labels_match_m21_contract_m23():
    """Pre-sort label sequence unchanged (core → extension → Settings → Extensions)."""
    t2, i2, ex, png, mm, tr = _six_placeholders()
    ext_tab = object()
    settings_i = object()
    extensions_i = object()
    rows = [(ext_tab, "Custom", "custom")]
    tuples = utr.build_top_level_interface_tuples(
        t2,
        i2,
        ex,
        png,
        mm,
        tr,
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


def test_create_ui_source_uses_settings_extensions_builders():
    """create_ui must build Settings/Extensions via M23 tab modules (source contract)."""
    src = (_REPO_ROOT / "modules" / "ui.py").read_text(encoding="utf-8")
    assert "ui_settings_tab.create_settings_tab(" in src
    assert "ui_extensions_tab.create_extensions_tab()" in src


def test_loadsave_excludes_settings_and_extensions_in_ui_py():
    """loadsave.add_block must not apply to settings/extensions tabs (guard in ui.py)."""
    src = (_REPO_ROOT / "modules" / "ui.py").read_text(encoding="utf-8")
    assert 'if ifid not in ["extensions", "settings"]:' in src


def test_create_settings_tab_delegates_and_returns_tab_build_result():
    """Settings builder runs UiSettings.create_ui and exposes interface on TabBuildResult."""

    class FakeSettings:
        def __init__(self):
            self.interface = None

        def create_ui(self, loadsave, dummy_component):
            self.interface = object()

    s = FakeSettings()
    ls, dc = object(), object()
    r = ui_settings_tab.create_settings_tab(s, ls, dc)
    assert isinstance(r, TabBuildResult)
    assert r.interface is s.interface
    assert r.label == "Settings"
    assert r.ifid == "settings"


def test_patched_settings_builder_flows_into_registry_slot(monkeypatch):
    """Modular settings interface is what the registry list uses (Settings slot)."""
    sentinel = object()

    def fake_settings_tab(_settings, _loadsave, _dummy_component):
        return TabBuildResult(sentinel, "Settings", "settings")

    monkeypatch.setattr(ui_settings_tab, "create_settings_tab", fake_settings_tab)
    t = ui_settings_tab.create_settings_tab(object(), object(), object())
    t2, i2, ex, png, mm, tr = (object() for _ in range(6))
    out = utr.build_top_level_interface_tuples(
        t2,
        i2,
        ex,
        png,
        mm,
        tr,
        [],
        t.interface,
        object(),
    )
    settings_row = next(row for row in out if row[2] == "settings")
    assert settings_row[0] is sentinel
    assert settings_row[1] == "Settings"


def test_patched_extensions_builder_flows_into_registry_last_slot(monkeypatch):
    """Modular extensions interface is what the registry list uses (last slot)."""
    sentinel = object()

    def fake_extensions():
        return TabBuildResult(sentinel, "Extensions", "extensions")

    monkeypatch.setattr(ui_extensions_tab, "create_extensions_tab", fake_extensions)
    t = ui_extensions_tab.create_extensions_tab()
    t2, i2, ex, png, mm, tr = (object() for _ in range(6))
    out = utr.build_top_level_interface_tuples(
        t2,
        i2,
        ex,
        png,
        mm,
        tr,
        [],
        object(),
        t.interface,
    )
    assert out[-1][0] is sentinel
    assert out[-1][1] == "Extensions"
    assert out[-1][2] == "extensions"
