"""M24 contract tests: extension API version and callback category registry."""
from __future__ import annotations

from modules import extension_api, script_callbacks


def _categories_from_callback_map():
    keys = script_callbacks.callback_map.keys()
    for k in keys:
        assert k.startswith("callbacks_"), (
            f"unexpected callback_map key: {k!r}"
        )
    return {k.removeprefix("callbacks_") for k in keys}


def test_extension_api_version_is_1_0_string():
    assert extension_api.EXTENSION_API_VERSION == "1.0"
    assert isinstance(extension_api.EXTENSION_API_VERSION, str)


def test_supported_callbacks_exactly_matches_callback_map():
    declared = set(extension_api.SUPPORTED_CALLBACKS)
    derived = _categories_from_callback_map()
    assert declared == derived, (
        f"SUPPORTED_CALLBACKS must exactly match callback_map categories.\n"
        f"only in declared: {declared - derived}\n"
        f"only in callback_map: {derived - declared}"
    )


def test_supported_callbacks_no_duplicates():
    names = extension_api.SUPPORTED_CALLBACKS
    assert len(names) == len(set(names)), (
        "SUPPORTED_CALLBACKS must not contain duplicates"
    )
