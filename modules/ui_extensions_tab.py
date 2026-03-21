"""Extensions top-level tab UI (M23)."""
from __future__ import annotations


def create_extensions_tab():
    import modules.ui_extensions as ui_extensions

    from modules.ui_tab_build_result import TabBuildResult

    interface = ui_extensions.create_ui()
    return TabBuildResult(interface, "Extensions", "extensions")
