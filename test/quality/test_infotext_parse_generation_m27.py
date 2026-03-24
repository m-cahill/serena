"""M27: parse_generation_parameters coverage (requires initialized shared.opts)."""
from __future__ import annotations

_DOC_SAMPLE = (
    "girl with an artist's beret, determined, blue eyes, desert scene, "
    "computer monitors, heavy makeup, by Alphonse Mucha and Charlie Bowater, "
    "((eyeshadow)), (coquettish), detailed, intricate\n"
    "Negative prompt: ugly, fat, obese, chubby, (((deformed))), [blurry], "
    "bad anatomy, disfigured, poorly drawn face, mutation, mutated, "
    "(extra_limb), (ugly), (poorly drawn hands), messy drawing\n"
    "Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 965400086, "
    "Size: 512x512, Model hash: 45dee52b"
)


def test_parse_generation_parameters_doc_sample(initialize):
    from modules import infotext_utils

    res = infotext_utils.parse_generation_parameters(_DOC_SAMPLE)
    assert "girl with an artist" in res["Prompt"]
    assert "ugly" in res["Negative prompt"]
    assert res.get("Steps") == "20"
    assert res.get("Size-1") == "512"
    assert res.get("Size-2") == "512"
    assert res.get("Clip skip") == "1"


def test_parse_generation_parameters_compact(initialize):
    from modules import infotext_utils

    compact = (
        "one line prompt\n"
        "Steps: 1, Sampler: Euler, CFG scale: 5, Seed: 1, Size: 64x64"
    )
    res = infotext_utils.parse_generation_parameters(compact)
    assert res["Prompt"].strip() == "one line prompt"
    assert res["Steps"] == "1"
    assert res["Size-1"] == "64"
    assert res["Size-2"] == "64"
