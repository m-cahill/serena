"""Shared UI tab builder result type (M22)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TabBuildResult:
    interface: Any
    label: str
    ifid: str
    dummy_component: Any | None = None
    txt2img_preview_params: list[Any] | None = None
    image_cfg_scale: Any | None = None
