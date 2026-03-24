"""M27: pure infotext quote/unquote helpers."""
from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "text,expected",
    [
        ("plain", "plain"),
        ("no special", "no special"),
    ],
)
def test_quote_passthrough(initialize, text, expected):
    from modules import infotext_utils

    assert infotext_utils.quote(text) == expected


def test_quote_escapes_special_chars(initialize):
    from modules import infotext_utils

    q = infotext_utils.quote("has,comma")
    assert q.startswith('"')
    assert infotext_utils.unquote(q) == "has,comma"


def test_quote_escapes_newline(initialize):
    from modules import infotext_utils

    q = infotext_utils.quote("a\nb")
    assert q.startswith('"')
    assert infotext_utils.unquote(q) == "a\nb"


def test_unquote_non_json_passthrough(initialize):
    from modules import infotext_utils

    assert infotext_utils.unquote("bare") == "bare"


def test_unquote_valid_json_string(initialize):
    from modules import infotext_utils

    assert infotext_utils.unquote('"hello"') == "hello"


def test_unquote_invalid_json_returns_original(initialize):
    from modules import infotext_utils

    bad = '"unclosed'
    assert infotext_utils.unquote(bad) == bad
