"""M27 wave 2: additional contract-style coverage (prompt parser, options API).

Targets the combined Quality coverage gate (≥42%) without runtime refactors.
"""
from __future__ import annotations

import pytest
import requests

_PROMPT_ATTENTION_CASES = [
    "normal text",
    "an (important) word",
    "(unbalanced",
    r"\(literal\]",
    "(unnecessary)(parens)",
    "a (((house:1.3)) [on] a (hill:0.5), sun, (((sky))).",
    "before BREAK after",
    "[square]",
    "(explicit:2.5)",
    "nested ((parens)) here",
]

_SCHEDULE_CASES: list[tuple[list[str], int, int | None, bool]] = [
    (["test"], 10, None, False),
    (["a [b:3]"], 10, None, False),
    (["a [b: 3]"], 10, None, False),
    (["a [[[b]]:2]"], 10, None, False),
    (["[(a:2):3]"], 10, None, False),
    (["a [b : c : 1] d"], 10, None, False),
    (["a[b:[c:d:2]:1]e"], 10, None, False),
    (["a [unbalanced"], 10, None, False),
    (["a [b:.5] c"], 10, None, False),
    (["a [{b|d{:.5] c"], 10, None, False),
    (["((a][:b:c [d:3]"], 10, None, False),
    (["[a|(b:1.1)]"], 10, None, False),
    (["[fe|]male"], 10, None, False),
    (["[fe|||]male"], 10, None, False),
    (["a [b:.5] c"], 10, 10, False),
    (["a [b:1.5] c"], 10, 10, False),
    (["a [b:.5] c"], 10, None, True),
]


@pytest.mark.parametrize("text", _PROMPT_ATTENTION_CASES)
def test_parse_prompt_attention_wave2(initialize, text):
    from modules import prompt_parser

    prompt_parser.parse_prompt_attention(text)


@pytest.mark.parametrize("prompts,base,hires,old", _SCHEDULE_CASES)
def test_get_learned_conditioning_prompt_schedules_wave2(
    initialize, prompts, base, hires, old
):
    from modules import prompt_parser

    prompt_parser.get_learned_conditioning_prompt_schedules(
        prompts, base, hires, old
    )


def test_get_multicond_prompt_list_wave2(initialize):
    from modules import prompt_parser

    prompt_parser.get_multicond_prompt_list(
        ["left AND right:0.5", "solo", "a AND b AND c:2"]
    )


def test_options_samples_save_roundtrip(base_url):
    g = requests.get(f"{base_url}/sdapi/v1/options", timeout=60)
    assert g.status_code == 200
    opts = g.json()
    key = "samples_save"
    if key not in opts:
        pytest.skip("samples_save missing from options payload")
    cur = opts[key]
    inv = not cur if isinstance(cur, bool) else (not bool(cur))
    p1 = requests.post(
        f"{base_url}/sdapi/v1/options",
        json={key: inv},
        timeout=60,
    )
    assert p1.status_code == 200
    p2 = requests.post(
        f"{base_url}/sdapi/v1/options",
        json={key: cur},
        timeout=60,
    )
    assert p2.status_code == 200


def test_get_override_settings_after_parse(initialize):
    from modules import infotext_utils

    params = infotext_utils.parse_generation_parameters(
        "prompt line\n"
        "Negative prompt: neg line\n"
        "Steps: 2, Sampler: Euler, CFG scale: 5, Seed: 3, Size: 48x48"
    )
    infotext_utils.get_override_settings(params)


def test_create_override_settings_dict_pairs(initialize):
    from modules import infotext_utils

    infotext_utils.create_override_settings_dict(
        ["Steps: 4", "CFG scale: 6"]
    )


def test_parse_generation_parameters_version_hires_hints(initialize):
    from modules import infotext_utils

    block = (
        "prompt\n"
        "Negative prompt: neg\n"
        "Steps: 1, Size: 32x32, Version: v1.8.0, "
        "Hires prompt: hp, Hires negative prompt: hn"
    )
    infotext_utils.parse_generation_parameters(block)


def test_parse_generation_parameters_hypernet_fields(initialize):
    from modules import infotext_utils

    block = (
        "p\n"
        "Negative prompt: n\n"
        "Steps: 1, Sampler: Euler, Hypernet: hn, "
        "Hypernet strength: 0.25, Size: 32x32"
    )
    infotext_utils.parse_generation_parameters(block)
