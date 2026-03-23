# M25 Summary — Deprecation & compatibility scaffolding

**Milestone:** M25  
**Phase:** Phase V — UI & Extension Stabilization  
**Audit score:** 5.0 / 5  
**Closed:** 2026-03-23 (UTC)

---

## What changed

- **`modules/deprecation.py`:** `warn_deprecated`, `@deprecated`, `format_extension_api_deprecation`; stdlib-only imports.
- **`modules/script_callbacks.py`:** `deprecate_callback(category, message="")` (structured `DeprecationWarning`, correct `stacklevel`); M25 comment block **below** `callback_map` (shim pattern + policy pointer).
- **`docs/architecture/extension_api_deprecation_policy.md`:** Additive v1.x policy, soft vs hard deprecation, milestone documentation, shim reference.
- **`test/quality/test_deprecation_scaffolding.py`:** Warning content, decorator, `deprecate_callback`, `SUPPORTED_CALLBACKS` vs `callback_map` equality, key count.
- **`docs/milestones/M25/`:** Plan, toolcalls, `M25_run1.md`, summary, audit.

**Not changed:** `callback_map` contents, `ordered_callbacks` / invocation order, `SUPPORTED_CALLBACKS`, extension loading, runtime modules, CI thresholds (`fail-under=40`).

---

## Why it mattered

- **Standardized deprecation channel** for future v1.x evolution without silent callback drift.
- **Policy + tests** complement M24 contract; scaffolding is inert until explicitly invoked.

---

## What remains

- **Phase VI:** **M26** — locked manifests / npm ci / CI environment stabilization.

---

## Evidence

- PR [#44](https://github.com/m-cahill/serena/pull/44) — squash-merged to `main`.
- Merge commit: **`468917974f9379ec1c514f995ab703c821078e45`** (`46891797`).
- Pre-merge (PR wave): see `M25_run1.md` — Linter [23417606838](https://github.com/m-cahill/serena/actions/runs/23417606838); Smoke [23417606843](https://github.com/m-cahill/serena/actions/runs/23417606843).
- Post-merge Quality: [23421440167](https://github.com/m-cahill/serena/actions/runs/23421440167) — **success**, **112 passed**, **40%** combined coverage (gate).
- Tag **`v0.0.25-m25`** (annotated) on merge commit **`468917974f9379ec1c514f995ab703c821078e45`**.
