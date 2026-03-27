"""Runtime execution context for generation runs.

M09: Lightweight context grouping model, opts_snapshot, device, state,
cmd_opts. Attached to processing object as p.runtime_context.
Write-only in M09; not yet consumed by runtime.

M34: Explicit model_identity (checkpoint name/hash) for orchestration/metadata
migration; descriptive only — model access remains via ModelProvider in runtime modules.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelIdentity:
    """Checkpoint identity for orchestration and metadata (M34).

    Mirrors the fields historically taken from ``shared.sd_model`` for
    ``p.sd_model_name`` / ``p.sd_model_hash`` in ``process_images_inner``.
    """

    name_for_extra: str
    model_hash: str


def model_identity_from_model(model: object) -> ModelIdentity:
    """Build identity from the active model object (authoritative generation model)."""
    return ModelIdentity(
        name_for_extra=model.sd_checkpoint_info.name_for_extra,
        model_hash=model.sd_model_hash,
    )


@dataclass
class RuntimeContext:
    """Groups runtime dependencies for the generation pipeline."""

    model: object
    model_identity: ModelIdentity
    opts_snapshot: object
    device: object
    state: object
    cmd_opts: object
