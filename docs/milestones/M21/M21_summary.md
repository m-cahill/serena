# M21 Summary — UI tab registry

**Milestone:** M21  
**Phase:** Phase V — UI & Extension Stabilization  
**Audit score:** 5.0 / 5  
**Closed:** 2026-03-20 (UTC)

---

## What changed

- **`modules/ui_tab_registry.py`:** Import-light registry — `TabSpec` (frozen dataclass: `interface`, `label`, `ifid`, `source`), `core_tab_specs()` for the six built-in top-level tabs, `tab_specs_from_ui_tabs_rows()`, `merge_extension_tabs()`, `append_settings_tab_spec()` / `append_extensions_tab_spec()`, `build_top_level_interface_tuples()`.
- **`modules/ui.py`:** `create_ui()` builds the top-level `interfaces` list via `ui_tab_registry.build_top_level_interface_tuples(...)` after `script_callbacks.ui_tabs_callback()` and `ui_extensions.create_ui()` in the same order as before; `shared.tab_names` derived from that list (pre-sort). No change to `sorted_interfaces` / `opts.hidden_tabs` rendering loop.
- **`test/quality/test_ui_tab_registry.py`:** Five contract tests (core order/ids, extension merge position, full pre-sort label sequence, source reference to registry call, monkeypatch on `core_tab_specs`).
- **`docs/milestones/M21/`:** Plan, toolcalls, PR CI run notes (`M21_run1.md`).

**Not changed:** Nested txt2img/img2img `gr.Tab` trees, runtime modules, extension callback registration API, `elem_id`s, `loadsave.add_block` exclusions.

---

## Why it mattered

- Establishes a **single, testable seam** for top-level tab enumeration before M22+ moves tab bodies into modules.
- Locks **pre-sort tab label order** (core → extension hooks → Settings → Extensions) with automated contracts.

---

## What remains

- **M22 / M23:** Move tab implementations and settings/extensions UI into focused modules behind the registry.
- **M24 / M25:** Extension API versioning and deprecation scaffolding.

---

## Evidence

- PR [#40](https://github.com/m-cahill/serena/pull/40) — squash-merged to `main`.
- Merge commit: **`081de7e71ea3307a750c16ddd0f8a35d4f44efdb`** (`081de7e7`).
- PR checks: Linter [23360537402](https://github.com/m-cahill/serena/actions/runs/23360537402); Smoke [23360545341](https://github.com/m-cahill/serena/actions/runs/23360545341).
- Post-merge Quality: [23361011739](https://github.com/m-cahill/serena/actions/runs/23361011739) @ `081de7e7` — **92** passed, **40%** coverage (gate).
- Tag **`v0.0.21-m21`** (annotated) on merge commit **`081de7e7`**. Closeout documentation was committed on `main` after the merge (tag remains on the squash merge commit per program convention).
