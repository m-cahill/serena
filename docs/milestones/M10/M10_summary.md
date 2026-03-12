# M10 Summary — ProcessingRunner Skeleton

📌 Milestone Summary — M10: ProcessingRunner Skeleton
==========================================================

**Project:** Serena  
**Phase:** Phase III — Runner & Service Boundary  
**Milestone:** M10 — ProcessingRunner skeleton  
**Timeframe:** 2026-03-11 → 2026-03-12  
**Status:** Closed  
**Baseline:** 2c6a2510 (M09 merge)  
**Refactor Posture:** Behavior-Preserving

---

## 1. Milestone Objective

M10 existed to introduce the **ProcessingRunner** abstraction as the unified execution entrypoint for Serena. The runner acts as a thin adapter around `process_images_inner`, creating the first true execution boundary between callers (UI/API/scripts) and the processing pipeline.

**What would remain unsafe or ungoverned if this refactor did not occur?** The pipeline would remain directly invoked with no abstraction layer. Phase III goals (CLI runner, queue runner, service mode, distributed execution) would be blocked. No single seam would exist for instrumentation, cancellation, or lifecycle control.

---

## 2. Scope Definition

### In Scope

* `modules/runtime/runner.py` — ProcessingRunner, ProcessingRequest
* `modules/processing.py` — Delegate to runner inside process_images
* `test/quality/test_processing_runner.py` — Contract test
* `docs/serena.md` — Phase III roadmap update (M11–M15)
* CI: Linter, Smoke Tests (PR), Quality Tests (post-merge)

### Out of Scope

* RuntimeContext in runner (deferred)
* txt2img/img2img path through runner (M13)
* API integration (M14)
* Async, threading, multiprocessing

---

## 3. Refactor Classification

### Change Type

**Boundary refactor** — Introduced adapter layer (ProcessingRunner) between process_images and process_images_inner. Mechanical delegation; no logic change.

### Observability

* **API responses:** Unchanged
* **CLI output:** Unchanged
* **File formats / save paths:** Unchanged
* **Model outputs:** Unchanged

---

## 4. Work Executed

* Created `modules/runtime/runner.py` with ProcessingRunner and ProcessingRequest
* ProcessingRequest wraps `StableDiffusionProcessing`
* ProcessingRunner.run(request) delegates to process_images_inner(request.processing)
* Modified process_images to instantiate runner and delegate (import inside function to avoid circular import)
* Added contract test with monkeypatch
* Updated Phase III roadmap in serena.md (M11 lifecycle, M12 instrumentation, M13 txt2img, M14 API, M15 queue)
* Fixed test_processing_runner collection error (PR #28): defer modules.processing import, add initialize fixture

---

## 5. Invariants & Compatibility

### Declared Invariants (must by default Not Change)

* CLI behavior unchanged
* API responses unchanged
* Processing results byte-identical
* Runtime state unchanged
* CI coverage ≥40%

### Compatibility Notes

* Backward compatibility preserved: Yes
* Breaking changes introduced: No
* Deprecations introduced: No

---

## 6. Validation & Evidence

| Evidence Type | Tool/Workflow | Result | Notes |
|--------------|---------------|--------|-------|
| Linter | ruff, eslint | ✓ | PR #27, 22987245316 (rerun); fix PR #28 |
| Smoke Tests | pytest test/smoke | ✓ | PR #27, 22987245317 |
| Quality Tests | pytest test/smoke test/quality | ✓ | Post-merge 22988627838 (after fix) |
| Coverage | ≥40% gate | ✓ | Quality Tests |
| verify_pinned_deps | scripts/ci/verify_pinned_deps.sh | ✓ | Quality Tests |
| pip-audit | Informational | ⚠ | Deferred M27 |

---

## 7. CI / Automation Impact

* Workflows affected: None (unchanged)
* Checks added/removed: None
* Enforcement: Unchanged
* Signal drift: None observed

---

## 8. Issues, Exceptions, and Guardrails

**Issue:** Quality Tests failed on initial merge (22988456117). `test_processing_runner.py` imported `modules.processing` at module level, triggering `sd_samplers.set_samplers()` before `shared.opts` was initialized.

**Resolution:** PR #28 — Defer import to inside test; add `initialize` fixture. Quality Tests passed on rerun (22988627838).

**Guardrail:** Quality tests that import heavy modules (processing, sd_samplers chain) must use `initialize` fixture and defer imports to test body.

---

## 9. Deferred Work

* pip-audit vulnerabilities: Pre-existing from M04; deferred to M27. Status unchanged.

---

## 10. Governance Outcomes

* First Phase III execution boundary established
* Call graph: UI/API/scripts → process_images → ProcessingRunner → process_images_inner
* Phase III roadmap corrected (M11 lifecycle before feature routing)

**What is now provably true that was not provably true before?** Serena has a single execution surface (ProcessingRunner) between callers and the pipeline. This enables future milestones: lifecycle (M11), instrumentation (M12), feature routing (M13–M14), queue/worker mode (M15).

---

## 11. Exit Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| ProcessingRunner skeleton | Met | modules/runtime/runner.py |
| process_images delegates through runner | Met | modules/processing.py |
| Contract test | Met | test/quality/test_processing_runner.py |
| CI fully green | Met | Linter, Smoke, Quality ✓ |
| No behavior change | Met | Smoke + quality pass |
| Milestone artifacts | Met | Plan, toolcalls, run1, run2, summary, audit |
| Ledger updated | Met | docs/serena.md |
| Tag created | Met | v0.0.10-m10 |

---

## 12. Final Verdict

Milestone objectives met. Refactor verified safe. Phase III execution boundary established. Proceed to M11 (Runner lifecycle surface).

---

## 13. Authorized Next Step

M11 — Runner lifecycle surface (prepare / execute / finalize). No additional constraints.

---

## 14. Canonical References

* PR #27: https://github.com/m-cahill/serena/pull/27
* PR #28: https://github.com/m-cahill/serena/pull/28 (Quality test fix)
* Merge commit: 0d11b587
* Quality Tests: 22988627838
* Linter: 22988627802
