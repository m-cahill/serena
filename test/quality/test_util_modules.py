"""Unit tests for modules.prompt_parser. Adds coverage without triggering circular imports.

Note: modules.util (natural_sort_key, html_path) is not tested here due to circular
import chain (util -> shared -> scripts -> util). Coverage for util comes from API/smoke tests.
"""
from modules.prompt_parser import (
    get_learned_conditioning_prompt_schedules,
    get_multicond_prompt_list,
    SdConditioning,
)


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


def test_get_multicond_prompt_list_simple():
    """get_multicond_prompt_list splits AND and extracts weights."""
    indexes, flat_list, _ = get_multicond_prompt_list(["a AND b"])
    assert len(indexes) == 1
    assert len(indexes[0]) == 2
    assert len(flat_list) == 2
    assert flat_list[0] == "a" and flat_list[1].strip() == "b"


def test_get_multicond_prompt_list_weight():
    """get_multicond_prompt_list handles weight syntax."""
    indexes, flat_list, _ = get_multicond_prompt_list(["a:1.2"])
    assert len(indexes) == 1
    assert indexes[0][0][1] == 1.2


def test_sd_conditioning():
    """SdConditioning stores prompts and optional dimensions."""
    c = SdConditioning(["prompt1", "prompt2"], is_negative_prompt=True, width=512, height=768)
    assert list(c) == ["prompt1", "prompt2"]
    assert c.is_negative_prompt is True
    assert c.width == 512
    assert c.height == 768
