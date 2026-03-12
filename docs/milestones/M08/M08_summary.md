# M08 Summary — Opts Snapshot Threading

**Project:** Serena  
**Phase:** Phase II — Runtime Seam Preparation  
**Milestone:** M08 — Opts snapshot threading  
**Status:** Closed  
**Branch:** m08-snapshot-threading  
**PR:** #24  
**Commit:** 710a0abd (merge)  
**Quality Run:** 22984445599 ✓

---

## Accomplished

| Item | Status |
|------|--------|
| Migrated save-related opts reads to p.opts_snapshot in process_images_inner | ✓ |
| save_images_before_face_restoration, save_images_before_color_correction | ✓ |
| samples_format, return_mask, save_mask, return_mask_composite, save_mask_composite | ✓ |
| grid_only_if_multiple, return_grid, grid_save, grid_format, grid_extended_filename | ✓ |
| Left save_samples(), sample_hr_pass(), create_infotext(), metadata on shared.opts | ✓ |
| Preserved behavior (same inputs → same outputs) | ✓ |
| Extension compatibility preserved | ✓ |

---

## CI Layout After M08

| Workflow | Trigger | Coverage | Security |
|----------|---------|----------|----------|
| Smoke Tests | pull_request (main) | No gate | None |
| Linter | pull_request | — | — |
| Quality Tests | push to main | ≥40% | pip-audit (informational) |

---

## Invariants Preserved

- Generation behavior unchanged
- File output behavior (save paths, naming) unchanged
- Extension compatibility (shared.opts still exists)
- API compatibility (txt2img/img2img)
- CLI behavior unchanged

---

## Blast Radius

| File | Change |
|------|--------|
| modules/processing.py | Modified — p.opts_snapshot for save-related reads |
| docs/milestones/M08/* | Plan, toolcalls, run reports |

---

## Refactor Result

First deterministic runtime boundary: generation pipeline now reads save-related config from p.opts_snapshot instead of shared.opts within process_images_inner. Fourth Phase II runtime seam; enables M09 execution context and ProcessingRunner architecture (M10+).
