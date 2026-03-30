"""Opts snapshot for generation runs.

M07: Deterministic snapshot of shared.opts for the duration of a run.
Behavior-preserving: shallow copy of opts.data.
Threaded on `p.opts_snapshot` (M07–M08); snapshot-first reads use `_eff_opts` / helpers (M39).
"""
from types import SimpleNamespace


def create_opts_snapshot(opts):
    """
    Create an immutable snapshot of shared.opts for a generation run.
    Behavior-preserving: shallow copy of opts.data.
    """
    return SimpleNamespace(**opts.data.copy())
