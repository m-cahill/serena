# Extension API contract v1.0

**Program:** Serena (fork)  
**Code:** `EXTENSION_API_VERSION = "1.0"` in `modules/extension_api.py`  
**Registry:** `modules/script_callbacks.py` — `callback_map` (authoritative)

---

## Versioning

- **v1.0** formalizes the existing callback **categories** as shipped in `callback_map`.
- **Non-breaking (v1.x) expectation:** new categories may be added with ledger + contract update; existing category names remain.
- **Breaking:** removing or renaming a category, or intentionally changing what the runner passes into user callbacks, requires a new **major** API version and explicit milestone approval.

---

## Stability guarantees (documentation)

- **Category names** listed below are locked by `test/quality/test_extension_api_contract.py` against `callback_map`.
- **Callable signatures** are described here for extension authors; they are **not** enforced by automated signature tests (M24 scope).
- **Fields** on parameter objects may gain new attributes in minor releases; documented positional/conventional usage should remain compatible within v1.x unless a release note says otherwise.

---

## Deprecation policy

1. Prefer **additive** changes (new categories, new optional fields) within v1.x.
2. If a category must be retired, announce in milestone docs, keep registration no-op or shim for at least one release where feasible, then bump `EXTENSION_API_VERSION` major/minor per program governance.
3. `script_callbacks` invocation order and `ordered_callbacks` behavior are out of scope for silent change; any change is a versioned milestone.

---

## Canonical category identifiers

Derived from `callback_map` keys by stripping the prefix `callbacks_`.  
Example: `callbacks_on_reload` → **`on_reload`**.

Authoritative tuple: `modules.extension_api.SUPPORTED_CALLBACKS` (must match the derived set **exactly**).

---

## Callback categories and parameter shapes (v1.0)

Summaries align with how `script_callbacks` **invokes** registered functions (see `*_callback` runners in `script_callbacks.py`).

| Category | Invoked as (conceptual) | Notes |
|----------|-------------------------|--------|
| `app_started` | `(demo: Blocks, app: FastAPI)` | After web UI startup. |
| `on_reload` | `()` | Before server reload. |
| `model_loaded` | `(sd_model)` | Model created or script reloaded. |
| `ui_tabs` | `()` → list of `(component, title, elem_id)` or None | Contributes main tabs. |
| `ui_train_tabs` | `(params: UiTrainTabParams)` | Train tab UI. |
| `ui_settings` | `()` | Before settings UI populated; register options via `shared.opts`. |
| `before_image_saved` | `(params: ImageSaveParams)` | May mutate save params. |
| `image_saved` | `(params: ImageSaveParams)` | After save; mutating params has no effect. |
| `extra_noise` | `(params: ExtraNoiseParams)` | Img2img / hires extra noise. |
| `cfg_denoiser` | `(params: CFGDenoiserParams)` | Inside CFG denoiser path. |
| `cfg_denoised` | `(params: CFGDenoisedParams)` | After inner denoise step. |
| `cfg_after_cfg` | `(params: AfterCFGCallbackParams)` | After CFG computation. |
| `before_component` | `(component, **kwargs)` | Before Gradio component construct. |
| `after_component` | `(component, **kwargs)` | After Gradio component construct. |
| `image_grid` | `(params: ImageGridLoopParams)` | Before grid build; params mutable. |
| `infotext_pasted` | `(infotext: str, params: dict[str, Any])` | Before applying infotext. |
| `script_unloaded` | `()` | Reversed order vs registration. |
| `before_ui` | `()` | Reversed order vs registration. |
| `list_optimizers` | `(list)` | Append `SdOptimization` items. |
| `list_unets` | `(list)` | Append `SdUnetOption` items. |
| `before_token_counter` | `(params: BeforeTokenCounterParams)` | May mutate dataclass fields. |

Parameter types (`ImageSaveParams`, `CFGDenoiserParams`, etc.) are defined in `script_callbacks.py`.

---

## Related tests

- `test/quality/test_extension_api_contract.py`
