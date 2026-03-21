"""Settings top-level tab UI assembly (M23).

Delegates to UiSettings.create_ui; lifecycle (register_settings, add_quicksettings, etc.) stays in modules.ui.create_ui.
"""
from __future__ import annotations


def create_settings_tab(settings, loadsave, dummy_component):
    from modules.ui_tab_build_result import TabBuildResult

    settings.create_ui(loadsave, dummy_component)
    return TabBuildResult(
        interface=settings.interface,
        label="Settings",
        ifid="settings",
    )
