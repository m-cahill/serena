# M18 Summary — Decode / Save Separation

**Project:** Serena  
**Phase:** Phase IV — Runtime Extraction  
**Milestone:** M18 — Decode/save separation  
**Timeframe:** 2026-03-19  
**Status:** Closed  
**Baseline:** M17 (16bd28ce); `main` pre-merge 5f53d175  
**Refactor Posture:** Behavior-Preserving

---

## 1. Milestone Objective

M18 moved **VAE decode (stack + normalize), face restoration, color correction + overlay, per-row saves (including masks), and grid save** from `process_images_inner` in `modules/processing.py` into `modules/runtime/decode_runtime.py`, keeping **all script hook call sites** in `processing.py` with **unchanged order**.

**What would remain ungoverned without this milestone?** The inner loop would still mix runtime output work with hook orchestration, blocking a clean **model provider** boundary (M19) and **mockable runtime** (M20).

---

## 2. Scope Definition

### In Scope

* `modules/runtime/decode_runtime.py` — `decode_latents`, `postprocess_face_restore_row`, `postprocess_images_for_row`, `save_outputs_for_row`, `save_outputs_grid`; `decode_latent_batch` + `DecodedSamples` relocated to avoid cycles  
* `process_images_inner` — delegation only; hooks remain  
* HR / auxiliary paths — import `decode_runtime.decode_latent_batch` only (no wider normalization)  
* `test/quality/test_decode_runtime.py` — delegation, stage order, static normalize check  
* Governance: plan, toolcalls, run1, run2, summary, audit  

### Out of Scope

* Sampler (M17), model provider (M19), mock runtime (M20)  
* Moving script hooks  
* Other `decode_first_stage` / `save_image` call sites outside the inner output path  

---

## 3. Refactor Classification

**Boundary refactor** — mechanical relocation; lazy import of `apply_color_correction` / `apply_overlay` from `processing` inside `postprocess_images_for_row` preserves layering without load-time cycles.

**Observability:** API, CLI, saved filenames/metadata, and generation semantics unchanged by design.

---

## 4. Work Executed

* Added decode/postprocess/save runtime functions; wired `process_images_inner` after `post_sample` and around existing script blocks  
* Moved `decode_latent_batch` / `DecodedSamples` into runtime module  
* Added quality-tier contract tests (source + ordering + decode normalize string check)  

---

## 5. Why It Mattered

* Completes **runtime ownership of the full inner-loop pipeline**: orchestration (M16) + sampler (M17) + **decode / postprocess / save** (M18)  
* Shape: `processing → runtime (orchestration + sampler + decode/save)` with hooks still in `processing.py`  
* Unblocks **M19** (model provider injection at a single boundary) and **M20** (fully mockable runtime)  

---

## 6. What Remains

* **M19** — Model provider interface  
* **M20** — Runtime tests with mockable boundaries  

---

## 7. Validation & Evidence

| Evidence Type | Tool / Workflow | Result | Notes |
|---------------|-----------------|--------|-------|
| Linter | ruff, eslint | ✓ | PR + `main` |
| Smoke Tests | PR #36 | ✓ | Run 1 |
| Quality Tests | `main` push | ✓ | Run [23321103961](https://github.com/m-cahill/serena/actions/runs/23321103961) |
| Coverage | ≥40% gate | ✓ | 40% combined |
| New tests | `test_decode_runtime` | ✓ | 4 tests in Quality |

---

## 8. Exit Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Decode/save in runtime module | Met | `decode_runtime.py` |
| Hook order / call sites in `processing.py` | Met | Code review + CI |
| No CI weakening | Met | Same gates |
| Scope limited to `process_images_inner` output path | Met | Plan + diff |

---

## 9. References

* PR [#36](https://github.com/m-cahill/serena/pull/36)  
* Merge commit `84ea94e7`  
* `docs/milestones/M18/M18_run1.md`, `M18_run2.md`  
