# M08 CI Run 1 — Opts Snapshot Threading

**Date:** 2026-03-12  
**Branch:** m08-snapshot-threading  
**PR:** #24  
**Trigger:** pull_request (PR to main)

---

## 1. Workflow Identity

| Workflow | Run ID | Trigger | Branch | Commit | Status |
|----------|--------|---------|--------|--------|--------|
| Linter | 22984306617 | pull_request | m08-snapshot-threading | be214f4e | ✓ success |
| Smoke Tests | 22984306614 | pull_request | m08-snapshot-threading | be214f4e | ✓ success |

**Quality Tests:** Not yet run (triggered on push to main; will run post-merge).

---

## 2. Change Context

| Item | Value |
|------|-------|
| Milestone | M08 — Opts Snapshot Threading |
| Phase | Phase II — Runtime Seam Preparation |
| Posture | Behavior-preserving |
| Refactor target | `modules/processing.py` (process_images_inner save-related opts reads) |
| Run type | First CI verification of M08 implementation |

---

## 3. Step 1 — Workflow Inventory

### Linter (22984306617)

| Job | Required? | Purpose | Pass/Fail |
|-----|-----------|---------|-----------|
| ruff | Yes | Python lint | ✓ |
| eslint | Yes | JS lint | ✓ |

**Duration:** ~22s

### Smoke Tests (22984306614)

| Job / Step | Required? | Purpose | Pass/Fail |
|------------|-----------|---------|-----------|
| Verify repository | Yes | Guardrail: m-cahill/serena only | ✓ |
| Verify base branch | Yes | Guardrail: PR targets main | ✓ |
| Checkout Code | Yes | Fetch PR branch | ✓ |
| Set up Python 3.10 | Yes | Runtime | ✓ |
| Cache models | Yes | Deterministic model path | ✓ |
| Install test dependencies | Yes | pytest, coverage | ✓ |
| Install runtime dependencies | Yes | torch, CLIP, open_clip, requirements_versions | ✓ |
| Create stub repositories | Yes | CI fake inference support | ✓ |
| Setup environment | Yes | launch.py --exit | ✓ |
| Smoke startup | Yes | Verify server can start | ✓ |
| Start test server | Yes | Live server for API tests | ✓ |
| **Run smoke tests** | **Yes** | **pytest test/smoke** | **✓** |
| Kill test server | Yes | Cleanup | ✓ |
| Upload main app output | No (always) | Artifact for debugging | ✓ |

**Duration:** 2m21s

---

## 4. Step 2 — Refactor Signal Integrity

### A) Tests

- **Tier:** Smoke only (test/smoke)
- **Coverage of refactor target:** Smoke tests exercise txt2img and img2img API endpoints, which call `process_images()` → `process_images_inner()`. The migrated opts reads (save_images_before_face_restoration, save_images_before_color_correction, samples_format, return_mask, save_mask, grid_save, grid_format, etc.) are on the critical path for image and grid saving. Smoke tests verify generation and save behavior.
- **Failures:** None
- **Golden/snapshot:** Smoke tests use CI fake inference (deterministic 1×1 PNG); no golden image comparison. API contract (response schema) and save paths exercised.
- **Missing:** Quality tier tests will run on push to main (coverage ≥40%, pip-audit, verify_pinned_deps).

### B) Coverage

- Smoke run does not enforce a coverage gate (Quality Tests do, on push to main).
- Coverage gate: ≥40% (M04 baseline).
- Post-merge Quality run will report coverage.

### C) Static Gates

- Ruff and eslint passed. No new lint issues introduced by M08 changes.
- Pre-existing F811 (sd_model, mask_blur redefinition) in processing.py unchanged.

---

## 5. Step 3 — Delta Analysis

### Change Inventory

| File | Change |
|------|--------|
| modules/processing.py | Replaced opts.foo with p.opts_snapshot.foo for save-related reads in process_images_inner |
| docs/milestones/M08/M08_plan.md | Populated plan |
| docs/milestones/M08/M08_toolcalls.md | Tool call log |

**Migrated options:** save_images_before_face_restoration, save_images_before_color_correction, samples_format, return_mask, save_mask, return_mask_composite, save_mask_composite, grid_only_if_multiple, return_grid, grid_save, grid_format, grid_extended_filename

**Unchanged (per M08 rules):** save_samples(), sample_hr_pass(), create_infotext(), Processed.__init__(), fill_fields_from_opts(), opts.enable_pnginfo, modules/images.py

### Expected vs Observed

- **Expected:** Same inputs → same outputs; save paths and naming identical; no behavior change.
- **Observed:** All smoke tests pass. No regressions.

---

## 6. Step 4 — Invariant Verification

| Invariant | Verification | Status |
|-----------|--------------|--------|
| Generation behavior unchanged | Smoke tests pass; snapshot values match shared.opts at capture time | ✓ |
| File output behavior | Save paths use p.outpath_samples/outpath_grids (unchanged); format from snapshot | ✓ |
| Extension compatibility | shared.opts still exists; extensions unchanged | ✓ |
| API responses | txt2img/img2img smoke tests pass | ✓ |
| CLI behavior | No CLI changes | ✓ |

---

## 7. Blast Radius

**Files changed:**
- `modules/processing.py` (modified)
- `docs/milestones/M08/*`

**No other modules changed.** Invariant registry surfaces (CLI, API, file formats, extension API, generation semantics) preserved.

---

## 8. Verdict

**CI Status:** Green (Linter ✓, Smoke Tests ✓)

**Refactor posture:** Behavior-preserving. First deterministic runtime boundary: generation pipeline now reads save-related config from p.opts_snapshot instead of shared.opts within process_images_inner.

**Next step:** Await merge permission. Post-merge Quality Tests will run (coverage, pip-audit, verify_pinned_deps). M08 run analysis complete; ready for M08 audit and summary generation after closeout.
