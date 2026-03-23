# M25 Plan — Deprecation & Compatibility Scaffolding

**Milestone:** M25  
**Phase:** Phase V — UI & Extension Stabilization  
**Branch:** `m25-deprecation-compat-scaffolding`  
**Status:** Completed (2026-03-23)

---

## Objective

Add **non-breaking** deprecation and compatibility scaffolding: structured `DeprecationWarning`s, optional future shims, and documentation. **No** `callback_map` / `SUPPORTED_CALLBACKS` changes, **no** invocation wiring.

---

## Deliverables

| Item | Path |
|------|------|
| Deprecation utilities | `modules/deprecation.py` — `warn_deprecated`, `@deprecated`, `format_extension_api_deprecation` (message builder for consistent prefix) |
| Callback channel | `script_callbacks.deprecate_callback` — warns only when called |
| Comment block | Below `callback_map`: `# === M25 Deprecation & Compatibility Scaffolding ===` + commented shim example + doc pointer |
| Architecture doc | `docs/architecture/extension_api_deprecation_policy.md` |
| Quality tests | `test/quality/test_deprecation_scaffolding.py` |
| Ledger | `docs/serena.md` — M25 row in progress / completed per closeout |

---

## Locked behavior

- Prefix: `Serena extension API: `; optional ` (since <version>)` when `version` is set.
- `warnings.warn(..., DeprecationWarning, stacklevel=…)` — `warn_deprecated` uses `stacklevel=2`; decorator uses `stacklevel=3` so the caller of the wrapped callable is attributed.
- `deprecate_callback(category, message="")` message format per M25 lock; `stacklevel=2` (defined in `script_callbacks`).

---

## Definition of done

- PR green (ruff, eslint, smoke, quality, coverage ≥ 40%).
- Audit / summary / tag per program workflow.
