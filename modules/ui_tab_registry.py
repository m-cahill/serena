"""
Top-level UI tab registry (M21).

Assembles the ordered list of main tabs for create_ui(). Import-light: no Gradio.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

TabSource = Literal["core", "extension"]


@dataclass(frozen=True)
class TabSpec:
    interface: Any
    label: str
    ifid: str
    source: TabSource


def core_tab_specs(
    txt2img_interface: Any,
    img2img_interface: Any,
    extras_interface: Any,
    pnginfo_interface: Any,
    modelmerger_blocks: Any,
    train_interface: Any,
) -> list[TabSpec]:
    """Ordered built-in tabs (first six top-level entries), before extension callbacks."""
    return [
        TabSpec(txt2img_interface, "txt2img", "txt2img", "core"),
        TabSpec(img2img_interface, "img2img", "img2img", "core"),
        TabSpec(extras_interface, "Extras", "extras", "core"),
        TabSpec(pnginfo_interface, "PNG Info", "pnginfo", "core"),
        TabSpec(modelmerger_blocks, "Checkpoint Merger", "modelmerger", "core"),
        TabSpec(train_interface, "Train", "train", "core"),
    ]


def tab_specs_from_ui_tabs_rows(rows: list) -> list[TabSpec]:
    """Normalize script_callbacks.ui_tabs_callback() rows to TabSpec(extension)."""
    return [TabSpec(interface, label, ifid, "extension") for interface, label, ifid in rows]


def merge_extension_tabs(core: list[TabSpec], extension: list[TabSpec]) -> list[TabSpec]:
    """Concatenate core then extension tabs (historical webui order)."""
    return [*core, *extension]


def append_settings_tab_spec(tabs: list[TabSpec], settings_interface: Any) -> list[TabSpec]:
    return [*tabs, TabSpec(settings_interface, "Settings", "settings", "core")]


def append_extensions_tab_spec(tabs: list[TabSpec], extensions_interface: Any) -> list[TabSpec]:
    return [*tabs, TabSpec(extensions_interface, "Extensions", "extensions", "core")]


def interface_tuples_from_specs(specs: list[TabSpec]) -> list[tuple]:
    return [(s.interface, s.label, s.ifid) for s in specs]


def build_top_level_interface_tuples(
    txt2img_interface: Any,
    img2img_interface: Any,
    extras_interface: Any,
    pnginfo_interface: Any,
    modelmerger_blocks: Any,
    train_interface: Any,
    ui_tabs_rows: list,
    settings_interface: Any,
    extensions_interface: Any,
) -> list[tuple]:
    """
    Full top-level tab list: six core tabs, extension ui_tabs hooks, Settings, Extensions.

    Callers should invoke script_callbacks.ui_tabs_callback() before ui_extensions.create_ui()
    to preserve historical side-effect ordering.
    """
    core = core_tab_specs(
        txt2img_interface,
        img2img_interface,
        extras_interface,
        pnginfo_interface,
        modelmerger_blocks,
        train_interface,
    )
    extension = tab_specs_from_ui_tabs_rows(ui_tabs_rows)
    merged = merge_extension_tabs(core, extension)
    merged = append_settings_tab_spec(merged, settings_interface)
    merged = append_extensions_tab_spec(merged, extensions_interface)
    return interface_tuples_from_specs(merged)
