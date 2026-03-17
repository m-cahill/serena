# M14 Summary — API Runner Contract

📌 Milestone Summary — M14: API integration (runner contract enforcement)
========================================================================

**Project:** Serena  
**Phase:** Phase III — Runner & Service Boundary  
**Milestone:** M14 — API runner contract  
**Timeframe:** 2026-03-17  
**Status:** Closed  
**Baseline:** a12028b1 (M13)  
**Refactor Posture:** Behavior-Preserving

---

## 1. Milestone Objective

M14 existed to **verify** that the API execution path flows through `ProcessingRunner`. M13 proved the UI path; M14 proved the API path. No routing changes were required — the API already calls `process_images`, which delegates to the runner.

**What would remain unsafe or ungoverned if this refactor did not occur?** Without explicit verification and a contract test, future changes could accidentally bypass the runner for API requests. M14 makes the API → process_images → runner flow **provably true** and regression-protected.

---

## 2. Scope Definition

### In Scope

* `test/quality/test_api_runner_contract.py` — New contract test
* `docs/milestones/M14/*` — Plan, toolcalls, run1, run2, summary, audit
* `CODEOWNERS` — @AUTOMATIC1111 → @m-cahill (fork owner; unblocks merge)

### Out of Scope

* API routing changes
* Runner or processing logic changes
* Queue/background runner (M15)
* Runtime extraction (M16+)

---

## 3. Refactor Classification

### Change Type

**Boundary refactor (verification)** — No routing changes; added contract test to verify existing API flow.

### Observability

* **API responses:** Unchanged  
* **CLI output:** Unchanged  
* **File formats / save paths:** Unchanged  
* **Model outputs:** Unchanged  

---

## 4. Work Executed

* Verified API calls `process_images(p)` only (text2imgapi, img2imgapi)
* Added `test_api_txt2img_uses_runner` — monkeypatches CI env + runner, calls API method directly, asserts runner invoked
* Updated CODEOWNERS for fork (unblocks code owner review)
* No functional logic changed in api/api.py, processing.py, or runner.py

---

## 5. Invariants & Compatibility

### Declared Invariants (must Not Change)

* CLI behavior identical
* API responses unchanged
* Output images identical
* Extensions unaffected
* Coverage ≥40%

### Compatibility Notes

* Backward compatibility preserved: Yes  
* Breaking changes: None  
* Deprecations: None  

---

## 6. Validation & Evidence

| Evidence Type | Tool/Workflow | Result | Notes |
| ------------- | ------------- | ------ | ----- |
| Smoke Tests | run_smoke_tests (PR) | ✓ | Run 1: 23182483297 |
| Linter | Linter workflow | ✓ | Run 1: 23182483282; Run 2: 23182849899 |
| Quality Tests | run_quality_tests | ✓ | Run 2: 23182849888 |
| Coverage | --fail-under=40 | ✓ | Gate passed |
| Contract test | test_api_txt2img_uses_runner | ✓ | API → runner verified |

---

## 7. CI / Automation Impact

* Workflows: Smoke Tests (PR), Linter, Quality Tests (push to main); all passed
* New test: `test_api_runner_contract.py` runs in quality tier
* No checks added/removed/reclassified
* No enforcement changes

---

## 8. Governance Outcomes

**What is now provably true that was not provably true before?**

The API txt2img path is **contract-tested** to invoke `ProcessingRunner`. The call chain `API → process_images → ProcessingRunner.run → process_images_inner` is locked in by automated test. Together with M13 (UI), **all execution entrypoints** now flow through the runner.

---

## 9. Exit Criteria Evaluation

| Criterion | Status | Evidence |
| --------- | ------ | -------- |
| API path uses ProcessingRunner | Met | Contract test added |
| No routing changes | Met | API continues to call process_images |
| CI green | Met | Smoke, Linter, Quality all pass |
| Coverage ≥40% | Met | Gate passed |
| Behavior identical | Met | No pipeline changes |

---

## 10. Canonical References

* **Commits:** 961297f (M14 impl), 46914eb (run1 report), 5b7de065 (merge)
* **PR:** [#32](https://github.com/m-cahill/serena/pull/32)
* **CI Runs:** Smoke 23182483297; Linter 23182483282, 23182849899; Quality 23182849888
* **Docs:** docs/milestones/M14/M14_plan.md, M14_run1.md, M14_run2.md

---

## 11. Authorized Next Step

**M15 — Queue / background runner preparation:** Insert queueing at the runner layer without touching API, UI, or extensions.
