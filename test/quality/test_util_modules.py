"""Unit tests for modules.util and modules.prompt_parser. Adds coverage without server."""
from modules.util import natural_sort_key, html_path
from modules.prompt_parser import get_learned_conditioning_prompt_schedules


def test_natural_sort_key():
    """natural_sort_key orders strings with numbers correctly."""
    items = ["a10", "a2", "a1"]
    assert sorted(items, key=natural_sort_key) == ["a1", "a2", "a10"]


def test_natural_sort_key_empty():
    """natural_sort_key handles empty string."""
    assert natural_sort_key("") == []


def test_html_path():
    """html_path returns path under script_path/html/."""
    p = html_path("foo")
    assert "html" in p
    assert p.endswith("foo")


def test_get_learned_conditioning_prompt_schedules_simple():
    """Prompt schedule for simple prompt."""
    result = get_learned_conditioning_prompt_schedules(["test"], 10)[0]
    assert result == [[10, "test"]]


def test_get_learned_conditioning_prompt_schedules_scheduled():
    """Prompt schedule for [a:b:0.5] syntax."""
    result = get_learned_conditioning_prompt_schedules(["a [b:.5] c"], 10)[0]
    assert result == [[5, "a  c"], [10, "a b c"]]


def test_get_learned_conditioning_prompt_schedules_alternate():
    """Prompt schedule for [a|b] alternate syntax."""
    result = get_learned_conditioning_prompt_schedules(["[a|b]"], 3)[0]
    assert len(result) == 3
    assert result[0][1] in ("a", "b")
    assert result[1][1] in ("a", "b")
    assert result[2][1] in ("a", "b")
