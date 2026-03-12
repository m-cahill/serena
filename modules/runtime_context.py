"""Runtime execution context for generation runs.

M09: Lightweight context grouping model, opts_snapshot, device, state,
cmd_opts. Attached to processing object as p.runtime_context.
Write-only in M09; not yet consumed by runtime.
"""
from dataclasses import dataclass


@dataclass
class RuntimeContext:
    """Groups runtime dependencies for the generation pipeline."""

    model: object
    opts_snapshot: object
    device: object
    state: object
    cmd_opts: object
