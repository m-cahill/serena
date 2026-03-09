"""Runtime utilities for the generation pipeline.

M05: Temporary opts override seam — isolates option mutation during generation.
"""
from contextlib import contextmanager

from modules import shared


@contextmanager
def temporary_opts(overrides: dict, restore_afterwards: bool = True):
    """Context manager for temporary option overrides during generation.

    Applies overrides via opts.set(..., is_api=True, run_callbacks=False).
    Restores original values on exit via setattr (no callbacks).
    Only mutates keys present in opts.data.

    Args:
        overrides: Dict of option key -> value to apply.
        restore_afterwards: If True, restore original values on exit.
    """
    opts = shared.opts
    if not overrides:
        yield
        return

    original = {
        k: opts.data[k] if k in opts.data else opts.get_default(k)
        for k in overrides.keys()
        if k in opts.data
    }

    try:
        for k, v in overrides.items():
            if k in opts.data:
                opts.set(k, v, is_api=True, run_callbacks=False)
        yield
    finally:
        if restore_afterwards:
            for k, v in original.items():
                setattr(opts, k, v)
