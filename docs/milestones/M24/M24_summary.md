# M24 Summary — Extension API v1 contract stabilization

**Milestone:** M24  
**Phase:** Phase V — UI & Extension Stabilization  
**Audit score:** 5.0 / 5  
**Closed:** 2026-03-22 (UTC)

---

## What changed

- **`modules/extension_api.py`:** `EXTENSION_API_VERSION = "1.0"` and `SUPPORTED_CALLBACKS` tuple (canonical category strings, alphabetical). **No** import of `script_callbacks`.
- **`modules/script_callbacks.py`:** Comment block `# === Extension API Contract (v1.0) ===` and deprecation/stability policy **above** `callback_map` only.
- **`docs/architecture/extension_api_contract_v1.md`:** v1.0 contract — versioning, stability, deprecation, category table with invocation summaries.
- **`test/quality/test_extension_api_contract.py`:** Version type checks; `set(SUPPORTED_CALLBACKS) ==` categories derived from `callback_map` via `removeprefix("callbacks_")`; all keys prefixed `callbacks_`; no duplicates in tuple.
- **`docs/milestones/M24/`:** Plan, toolcalls, `M24_run1.md`, summary, audit.

**Not changed:** Callback invocation order, `ordered_callbacks`, extension loading, `Script` API, UI registry, runtime modules, CI thresholds.

---

## Why it mattered

- **Explicit, versioned extension surface** before Phase VI hardening.
- **Tests prevent silent drift** between declared categories and `callback_map`.
- **Documentation** gives extension authors and maintainers a single contract reference.

---

## What remains

- **M25:** Deprecation and compatibility scaffolding.

---

## Evidence

- PR [#43](https://github.com/m-cahill/serena/pull/43) — squash-merged to `main`.
- Merge commit: **`2c8bc5b7b5f504597a41a00604f3e7119c22aba6`** (`2c8bc5b7`).
- Pre-merge (PR wave): Linter [23395414702](https://github.com/m-cahill/serena/actions/runs/23395414702); Smoke [23395414700](https://github.com/m-cahill/serena/actions/runs/23395414700); see `M24_run1.md`.
- Post-merge Quality: [23395515966](https://github.com/m-cahill/serena/actions/runs/23395515966) — **success**, **105 passed**, **40%** combined coverage (gate).
- Tag **`v0.0.24-m24`** (annotated) on merge commit **`2c8bc5b7b5f504597a41a00604f3e7119c22aba6`**.
