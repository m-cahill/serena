"""
Prompt and seed preparation for Stable Diffusion processing.

Extracted from processing.py (M06) to isolate preparation logic from sampling.
Behavior-preserving: writes directly to p; assumes setup_prompts() already ran.
"""

from __future__ import annotations


def prepare_prompt_seed_state(p):
    """
    Populate p.all_seeds and p.all_subseeds from p.seed and p.subseed.

    Assumes:
    - p.seed and p.subseed have already been normalized via get_fixed_seed()
    - p.setup_prompts() has already run (p.all_prompts exists)
    """
    if isinstance(p.seed, list):
        p.all_seeds = p.seed
    else:
        p.all_seeds = [
            int(p.seed) + (x if p.subseed_strength == 0 else 0)
            for x in range(len(p.all_prompts))
        ]

    if isinstance(p.subseed, list):
        p.all_subseeds = p.subseed
    else:
        p.all_subseeds = [int(p.subseed) + x for x in range(len(p.all_prompts))]
