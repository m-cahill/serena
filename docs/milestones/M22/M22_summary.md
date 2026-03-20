# M22 Summary — txt2img / img2img tab modularization

**Milestone:** M22  
**Phase:** Phase V — UI & Extension Stabilization  
**Audit score:** 5.0 / 5  
**Closed:** 2026-03-20 (UTC)

---

## What changed

- **`modules/ui_tab_build_result.py`:** `TabBuildResult` dataclass carrying `interface`, `label`, `ifid`, optional `dummy_component`, `txt2img_preview_params`, `image_cfg_scale` for remaining `create_ui()` wiring.
- **`modules/ui_txt2img_tab.py`:** `create_txt2img_tab()` — txt2img top-level `gr.Blocks` body moved from `ui.py`; lazy `import modules.ui as ui` inside the builder.
- **`modules/ui_img2img_tab.py`:** `create_img2img_tab()` and module-level `img2img_dummy_component` bridge so img2img reuses txt2img’s dummy label wiring; lazy imports inside builder.
- **`modules/ui.py`:** Orchestrates txt2img/img2img via tab modules; sets `ui_img2img_tab.img2img_dummy_component` before img2img build and clears after; registry call unchanged (six interface objects into `build_top_level_interface_tuples`).
- **`.github/workflows/run_smoke_tests.yaml`:** `push` on non-`main` branches plus PR to `main`; “Verify base branch” only on `pull_request` — fixes Smoke not firing for PR #41.
- **`test/quality/test_ui_tab_modularization.py`:** Contracts for frozen registry labels/ifids, pre-sort label sequence, `create_ui` source wiring, patched builder flowing into registry tuples.
- **`docs/milestones/M22/`:** Plan, toolcalls, CI run notes (`M22_run1.md`), summary, audit.

**Not changed:** `ui_tab_registry` public API (`core_tab_specs`, `build_top_level_interface_tuples` arity and semantics), `shared.tab_names` pre-sort derivation, `sorted_interfaces` / `hidden_tabs` rendering, nested tab structure inside txt2img/img2img, runtime modules, M21 registry tests.

---

## Why it mattered

- **`ui.py` shrinks toward orchestration** while preserving M21 tab-order and registry contracts.
- **Dummy bridge is explicit and test-backed** so cross-tab wiring stays behavior-identical.
- **CI delivery gap documented and repaired** so Smoke is a reliable pre-merge gate on feature branches.

---

## What remains

- **M23:** Settings and Extensions UI modularization behind the registry seam.
- **M24 / M25:** Extension API versioning and deprecation scaffolding.

---

## Evidence

- PR [#41](https://github.com/m-cahill/serena/pull/41) — squash-merged to `main`.
- Merge commit: **`99b5f0c43806c3b521cbb6d8ef561fa87ef2c75d`** (`99b5f0c4`).
- Pre-merge: Smoke [23365701378](https://github.com/m-cahill/serena/actions/runs/23365701378); Linter [23365701379](https://github.com/m-cahill/serena/actions/runs/23365701379) (push-triggered after workflow fix).
- Post-merge Quality: [23365924953](https://github.com/m-cahill/serena/actions/runs/23365924953) @ merge commit — success, **coverage ≥ 40%** (gate).
- Tag **`v0.0.22-m22`** (annotated) on merge commit **`99b5f0c43806c3b521cbb6d8ef561fa87ef2c75d`**. Closeout docs may land on `main` after the merge; tag remains on the squash merge commit per program convention.
