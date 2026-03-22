"""
Declarative extension API contract (M24).

Import-light: do not import ``script_callbacks`` here (avoids cycles;
runtime unchanged). Quality tests compare this module to
``script_callbacks.callback_map``.
"""
from __future__ import annotations

EXTENSION_API_VERSION = "1.0"

# Canonical identifiers = category strings (``callbacks_<category>`` keys with
# ``callbacks_`` removed). Alphabetical order for stable review.
# MUST match ``{k.removeprefix("callbacks_") for k in callback_map}`` exactly.
SUPPORTED_CALLBACKS = (
    "after_component",
    "app_started",
    "before_component",
    "before_image_saved",
    "before_token_counter",
    "before_ui",
    "cfg_after_cfg",
    "cfg_denoised",
    "cfg_denoiser",
    "extra_noise",
    "image_grid",
    "image_saved",
    "infotext_pasted",
    "list_optimizers",
    "list_unets",
    "model_loaded",
    "on_reload",
    "script_unloaded",
    "ui_settings",
    "ui_tabs",
    "ui_train_tabs",
)
