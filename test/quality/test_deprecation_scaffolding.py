"""M25: deprecation helpers and callback channel (warnings only)."""
from __future__ import annotations

import pytest

from modules import deprecation, extension_api, script_callbacks


def _categories_from_callback_map():
    keys = script_callbacks.callback_map.keys()
    for k in keys:
        assert k.startswith("callbacks_"), (
            f"unexpected callback_map key: {k!r}"
        )
    return {k.removeprefix("callbacks_") for k in keys}


def test_warn_deprecated_emits_deprecation_warning():
    with pytest.warns(DeprecationWarning) as record:
        deprecation.warn_deprecated("test reason")
    assert len(record) == 1
    msg = str(record[0].message)
    assert "Serena extension API:" in msg
    assert "test reason" in msg
    assert "(since" not in msg


def test_warn_deprecated_includes_version_when_set():
    with pytest.warns(DeprecationWarning) as record:
        deprecation.warn_deprecated("old hook", version="1.1")
    msg = str(record[0].message)
    assert "Serena extension API:" in msg
    assert "old hook" in msg
    assert "(since 1.1)" in msg


def test_deprecate_callback_emits_with_category_and_prefix():
    with pytest.warns(DeprecationWarning) as record:
        script_callbacks.deprecate_callback("ui_tabs", "use ui_tabs_v2")
    msg = str(record[0].message)
    assert "Serena extension API:" in msg
    assert "callback 'ui_tabs' is deprecated." in msg
    assert "use ui_tabs_v2" in msg


def test_deprecate_callback_empty_message():
    with pytest.warns(DeprecationWarning) as record:
        script_callbacks.deprecate_callback("model_loaded", "")
    msg = str(record[0].message)
    assert "Serena extension API:" in msg
    assert "callback 'model_loaded' is deprecated." in msg


def test_deprecated_decorator_warns_on_function_call():
    @deprecation.deprecated("frobnicate is legacy", version="9.9")
    def frobnicate():
        return 1

    with pytest.warns(DeprecationWarning) as record:
        assert frobnicate() == 1
    msg = str(record[0].message)
    assert "Serena extension API:" in msg
    assert "frobnicate is legacy" in msg
    assert "(since 9.9)" in msg


def test_supported_callbacks_exactly_matches_callback_map():
    declared = set(extension_api.SUPPORTED_CALLBACKS)
    derived = _categories_from_callback_map()
    assert declared == derived


def test_callback_map_key_count_unchanged():
    assert len(script_callbacks.callback_map) == len(
        extension_api.SUPPORTED_CALLBACKS
    )
