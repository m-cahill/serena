"""M27: unit coverage for M06/M07 seams (no Gradio, no HTTP)."""
from __future__ import annotations

from types import SimpleNamespace

from modules.opts_snapshot import create_opts_snapshot
from modules.prompt_seed_prep import prepare_prompt_seed_state


def test_create_opts_snapshot_copies_data():
    opts = SimpleNamespace(data={"k": 1, "nested": {"x": 2}})
    snap = create_opts_snapshot(opts)
    assert snap.k == 1
    assert snap.nested == {"x": 2}
    opts.data["k"] = 99
    assert snap.k == 1


def test_prepare_prompt_seed_state_int_seeds():
    p = SimpleNamespace(
        seed=10,
        subseed=20,
        subseed_strength=0.0,
        all_prompts=["a", "b"],
    )
    prepare_prompt_seed_state(p)
    assert p.all_seeds == [10, 11]
    assert p.all_subseeds == [20, 21]


def test_prepare_prompt_seed_state_list_seeds():
    p = SimpleNamespace(
        seed=[1, 2],
        subseed=[3, 4],
        subseed_strength=0.0,
        all_prompts=["x"],
    )
    prepare_prompt_seed_state(p)
    assert p.all_seeds == [1, 2]
    assert p.all_subseeds == [3, 4]


def test_prepare_prompt_seed_state_subseed_strength_nonzero():
    p = SimpleNamespace(
        seed=5,
        subseed=7,
        subseed_strength=0.5,
        all_prompts=["p1", "p2", "p3"],
    )
    prepare_prompt_seed_state(p)
    assert p.all_seeds == [5, 5, 5]
    assert p.all_subseeds == [7, 8, 9]
