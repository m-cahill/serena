# M13 Summary — txt2img Path Through Runner

📌 Milestone Summary — M13: txt2img execution via runner
========================================================

**Project:** Serena  
**Phase:** Phase III — Runner & Service Boundary  
**Milestone:** M13 — txt2img path through runner  
**Timeframe:** 2026-03-12 → 2026-03-13  
**Status:** Closed  
**Baseline:** 46cf6d1c (v0.0.12-m12, M12)  
**Refactor Posture:** Behavior-Preserving

---

## 1. Milestone Objective

M13 existed to **verify** that the txt2img execution path flows through `ProcessingRunner`. The runner was introduced in M10–M12; M13 confirmed that the txt2img UI path already uses it via `process_images` and added a contract test to lock that routing.

**What would remain unsafe or ungoverned if this refactor did not occur?** Without explicit verification and a contract test, future changes could accidentally bypass the runner. M13 makes the txt2img → runner flow **provably true** and regression-protected.

---

## 2. Scope Definition

### In Scope

* `modules/txt2img.py` — Verification only; no changes
* `test/quality/test_txt2img_runner_contract.py` — New contract test
* `docs/milestones/M13/*` — Plan, toolcalls, run1, run2, summary, audit

### Out of Scope

* API integration (M14)
* img2img path (covered by process_images; not M13 scope)
* Scripts, extensions
* Queue/background runner (M15)
* Pipeline modification

---

## 3. Refactor Classification

### Change Type

**Boundary refactor (verification)** — No routing changes; added contract test to verify existing flow.

### Observability

* **API responses:** Unchanged  
* **CLI output:** Unchanged  
* **File formats / save paths:** Unchanged  
* **Model outputs:** Unchanged  

---

## 4. Work Executed

* Verified txt2img calls `process_images(p)` only (lines 83, 109); no direct `process_images_inner`
* Verified `process_images` delegates to `ProcessingRunner().run(ProcessingRequest(p))` (M10)
* Added `test_txt2img_path_uses_runner` — monkeypatches runner, calls `process_images`, asserts runner.execute invoked
* Updated M13_plan (implementation steps, risk level, deliverables)
* No functional logic changed in txt2img, processing, or runner

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
| Smoke Tests | run_smoke_tests (PR) | ✓ | Run 1: 23038170275 |
| Linter | Linter workflow | ✓ | Run 2: 23072709504 |
| Quality Tests | run_quality_tests | ✓ | Run 2: 23072709479 |
| Coverage | --fail-under=40 | ✓ | Gate passed |
| Contract test | test_txt2img_path_uses_runner | ✓ | Runner invocation verified |

---

## 7. CI / Automation Impact

* Workflows: Smoke Tests (PR), Linter, Quality Tests (push to main); all passed
* New test: `test_txt2img_runner_contract.py` runs in quality tier
* No checks added/removed/reclassified
* No enforcement changes

---

## 8. Issues, Exceptions, and Guardrails

No new issues were introduced during this milestone.

---

## 9. Deferred Work

* API runner routing — M14
* Queue/background runner — M15
* Node.js 20 actions deprecation — informational; no M13 action
* pip-audit vulnerabilities — deferred to M27 (pre-existing)

---

## 10. Governance Outcomes

**What is now provably true that was not provably true before?**

The txt2img UI path is **contract-tested** to invoke `ProcessingRunner`. The call chain `txt2img → process_images → ProcessingRunner.run → process_images_inner` is locked in by automated test. Future changes that bypass the runner will fail the contract test.

---

## 11. Exit Criteria Evaluation

| Criterion | Status | Evidence |
| --------- | ------ | -------- |
| txt2img path uses ProcessingRunner | Met | Verified; no routing changes needed |
| No direct process_images_inner in txt2img path | Met | txt2img calls process_images only |
| CI green | Met | Smoke, Linter, Quality all pass |
| Coverage ≥40% | Met | Gate passed |
| Behavior identical | Met | No pipeline changes |

---

## 12. Final Verdict

Milestone objectives met. Refactor verified safe. Proceed to M14.

---

## 13. Authorized Next Step

**M14 — API integration:** Route API generation paths through the runner.

---

## 14. Canonical References

* **Commits:** 142f0bbe (M13 impl), 212b6275 (run1 report), 4dd04999 (merge)
* **PR:** [#31](https://github.com/m-cahill/serena/pull/31)
* **CI Runs:** Smoke 23038170275; Linter 23072709504; Quality 23072709479
* **Docs:** docs/milestones/M13/M13_plan.md, M13_run1.md, M13_run2.md
