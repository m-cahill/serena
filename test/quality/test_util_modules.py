"""Unit tests for modules.prompt_parser. Adds coverage without triggering circular imports.

Note: modules.util (natural_sort_key, html_path) is not tested here due to circular
import chain (util -> shared -> scripts -> util). Coverage for util comes from API/smoke tests.
"""
from modules.prompt_parser import get_learned_conditioning_prompt_schedules


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


def test_get_learned_conditioning_prompt_schedules_int_step():
    """Prompt schedule with integer step [b:3]."""
    result = get_learned_conditioning_prompt_schedules(["a [b:3]"], 10)[0]
    assert result == [[3, "a "], [10, "a b"]]


def test_get_learned_conditioning_prompt_schedules_unbalanced():
    """Unbalanced bracket falls through to single step."""
    result = get_learned_conditioning_prompt_schedules(["a [unbalanced"], 10)[0]
    assert result == [[10, "a [unbalanced"]]
