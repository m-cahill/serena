# M17 Summary — Sampler Runner Extraction

**Project:** Serena  
**Phase:** Phase IV — Runtime Extraction  
**Milestone:** M17 — Sampler runner extraction  
**Timeframe:** 2026-03-19  
**Status:** Closed  
**Baseline:** M16 (912f33da)  
**Refactor Posture:** Behavior-Preserving

---

## 1. Milestone Objective

M17 extracted **sampler creation and invocation** from `modules/processing.py` into `modules/runtime/sampler_runtime.py`, following the M16 extraction pattern. This is the second major Phase IV slice: **model execution** (sampler) now lives in the runtime layer alongside batch orchestration.

**What would remain ungoverned if this refactor did not occur?** No proof that sampler execution can relocate safely; M18 (decode/save) and M19 (model provider) would lack a clean execution boundary.

---

## 2. Scope Definition

### In Scope

* `modules/runtime/sampler_runtime.py` — `run_sampler_txt2img`, `run_sampler_img2img`
* `StableDiffusionProcessingTxt2Img.sample`, `sample_hr_pass` — delegation
* `StableDiffusionProcessingImg2Img.sample` — invocation only (creation stays in `init()`)
* `test/quality/test_sampler_runtime.py` — delegation contract tests
* M17 plan, toolcalls, run1, run2, summary, audit

### Out of Scope

* Decode/save separation (M18)
* Model provider interface (M19)
* Mockable boundaries / runtime tests (M20)
* Script hook movement
* API/UI changes
* Runner lifecycle changes

---

## 3. Refactor Classification

### Change Type

**Boundary refactor** — Mechanical relocation of `create_sampler` + `sampler.sample` / `sampler.sample_img2img` behind runtime functions; argument fidelity preserved.

### Observability

* API responses: Unchanged  
* CLI output: Unchanged  
* Model outputs: Unchanged  
* File formats / save paths: Unchanged  

---

## 4. Work Executed

* Added `run_sampler_txt2img(p, x, conditioning, unconditional_conditioning)` for txt2img first pass
* Added `run_sampler_img2img(..., steps=..., image_conditioning=..., sampler_name=...)` for img2img and hires pass (`sampler_name` set only when creating hr sampler)
* Replaced inline sampler calls in three sites; `process_before_every_sampling` remains in `sample()` / `sample_hr_pass()` before runtime calls
* Img2Img: `create_sampler` unchanged in `init()` (intentional asymmetry per M17 rules)

---

## 5. Why It Mattered

* Completes the **second** major runtime extraction after M16 (orchestration)
* Establishes **runtime ownership of model execution** (sampler path)
* Pipeline shape: `processing → runtime (orchestration + sampler) → model`
* M18 decode/save and M19 model provider have a clearer seam

---

## 6. What Remains

* **M18** — Decode/save separation  
* **M19** — Model provider interface  
* **M20** — Mockable runtime boundaries  

---

## 7. Validation & Evidence

| Evidence Type | Tool/Workflow | Result | Notes |
|---------------|---------------|--------|-------|
| Linter | ruff, eslint | ✓ | PR + main |
| Smoke Tests | run_smoke_tests | ✓ | PR |
| Quality Tests | run_quality_tests | ✓ | Run 23318593847 |
| Coverage | ≥40% gate | ✓ | Post-merge |
| Delegation tests | test_sampler_runtime | ✓ | Quality tier |

---

## 8. Exit Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Sampler invocation in runtime module | Met | sampler_runtime.py |
| Script hooks / decode / save unchanged | Met | processing.py |
| CI green | Met | Linter, Smoke, Quality |
| Coverage ≥40% | Met | Quality gate |
| No behavior drift | Met | All tests pass |

---

## 9. Final Verdict

Milestone objectives met. Phase IV runtime boundary now includes **orchestration (M16) and sampler execution (M17)**. Proceed to M18.

---

## 10. Canonical References

* **PR:** [#35](https://github.com/m-cahill/serena/pull/35)
* **Merge commit:** 16bd28ce
* **Quality run:** [23318593847](https://github.com/m-cahill/serena/actions/runs/23318593847)
* **Tag:** v0.0.17-m17
