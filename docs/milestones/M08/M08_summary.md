# M08 Summary — Opts Snapshot Threading

📌 Milestone Summary — M08: Opts Snapshot Threading
====================================================

**Project:** Serena  
**Phase:** Phase II — Runtime Seam Preparation  
**Milestone:** M08 — Opts snapshot threading  
**Timeframe:** 2026-03-11 → 2026-03-12  
**Status:** Closed  
**Baseline:** 8ea50d35 (M07 merge)  
**Refactor Posture:** Behavior-Preserving

---

## 1. Milestone Objective

M08 existed to thread `p.opts_snapshot` into the generation runtime for safe read-only option access. M07 introduced the snapshot (write-only); M08 migrates the first set of reads from `shared.opts` to `p.opts_snapshot`.

**What would remain unsafe or ungoverned if this refactor did not occur?** The runtime would continue reading directly from global `shared.opts` during generation, preventing deterministic isolation and blocking the ProcessingRunner architecture (M10+).

---

## 2. Scope Definition

### In Scope

* `modules/processing.py` — process_images_inner() for save-related opts reads
* Migrated options: save_images_before_face_restoration, save_images_before_color_correction, samples_format, return_mask, save_mask, return_mask_composite, save_mask_composite, grid_only_if_multiple, return_grid, grid_save, grid_format, grid_extended_filename
* CI: Linter, Smoke Tests (PR), Quality Tests (post-merge)
* Documentation: M08_plan.md, M08_toolcalls.md, M08_run1.md, M08_run2.md

### Out of Scope

* save_samples(), sample_hr_pass(), create_infotext(), Processed.__init__(), fill_fields_from_opts()
* modules/images.py
* Override logic, UI/API option behavior, extension access to shared.opts
* New runtime abstractions

---

## 3. Refactor Classification

### Change Type

**Mechanical refactor** — Replace `opts.foo` with `p.opts_snapshot.foo` for save-related reads. No logic change; same values at capture time.

### Observability

* **API responses:** Unchanged (txt2img/img2img JSON schema unchanged)
* **CLI output:** Unchanged
* **File formats / save paths:** Unchanged (p.outpath_samples, p.outpath_grids set before process_images_inner; format from snapshot)
* **Model outputs:** Unchanged

---

## 4. Work Executed

* Replaced 12 opts reads with p.opts_snapshot reads in process_images_inner
* No functional logic changed; values identical at snapshot capture time
* No new modules; no migration steps
* Files changed: modules/processing.py, docs/milestones/M08/*

---

## 5. Invariants & Compatibility

### Declared Invariants (must by default Not Change)

* Generation behavior unchanged (same inputs → same outputs)
* File output behavior unchanged (save paths, naming)
* Extension compatibility (shared.opts still exists)
* API compatibility (txt2img/img2img)
* CLI behavior unchanged

### Compatibility Notes

* Backward compatibility preserved: Yes
* Breaking changes introduced: No
* Deprecations introduced: No

---

## 6. Validation & Evidence

| Evidence Type | Tool/Workflow | Result | Notes |
|--------------|---------------|--------|-------|
| Linter | ruff, eslint | ✓ | PR #24 |
| Smoke Tests | pytest test/smoke | ✓ | PR #24, run 22984306614 |
| Quality Tests | pytest test/smoke test/quality | ✓ | Post-merge 22984445599 |
| Coverage | ≥40% gate | ✓ | Quality Tests |
| verify_pinned_deps | scripts/ci/verify_pinned_deps.sh | ✓ | Quality Tests |
| pip-audit | Informational | ⚠ | Deferred M27 |

---

## 7. CI / Automation Impact

* Workflows affected: None (unchanged)
* Checks added/removed: None
* Enforcement: Unchanged
* Signal drift: None observed

CI blocked incorrect changes (would fail if snapshot missing or wrong). CI validated correct changes (smoke + quality pass).

---

## 8. Issues, Exceptions, and Guardrails

No new issues were introduced during this milestone.

---

## 9. Deferred Work

* pip-audit vulnerabilities: Pre-existing from M04; deferred to M27. Status unchanged.

---

## 10. Governance Outcomes

* Runtime seam stack now includes snapshot threading: fourth Phase II seam
* First deterministic runtime boundary: generation pipeline reads save-related config from p.opts_snapshot
* Invariants preserved and verified by CI

**What is now provably true that was not provably true before?** The generation runtime reads save-related options from a deterministic snapshot (p.opts_snapshot) rather than global shared.opts within process_images_inner.

---

## 11. Exit Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Snapshot used in generation runtime | Met | p.opts_snapshot.foo in process_images_inner |
| Safe options migrated | Met | 12 opts migrated |
| CI fully green | Met | Linter, Smoke, Quality ✓ |
| No behavior change | Met | Smoke + quality pass |
| Milestone artifacts generated | Met | Plan, toolcalls, run1, run2, audit, summary |
| Ledger updated | Met | docs/serena.md |
| Tag created | Met | v0.0.08-m08 |

---

## 12. Final Verdict

Milestone objectives met. Refactor verified safe. Proceed to M09.

---

## 13. Authorized Next Step

M09 — Execution context seam. No additional constraints.

---

## 14. Canonical References

* Commit: 710a0abd (merge)
* PR: #24 (https://github.com/m-cahill/serena/pull/24)
* CI Run 1 — Linter: 22984306617; Smoke: 22984306614
* CI Run 2 — Quality: 22984445599
* Tag: v0.0.08-m08
* Documents: docs/milestones/M08/M08_plan.md, M08_run1.md, M08_run2.md, M08_audit.md, M08_summary.md
