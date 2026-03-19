# M18 Milestone Audit

**Milestone:** M18 — Decode/save separation  
**Mode:** EXTRACTION AUDIT  
**Range:** 5f53d175...84ea94e7 (`main` pre-merge tip → merge commit for PR #36)  
**CI Status:** Green (Linter + Smoke on PR; Linter + Quality on `main`)  
**Refactor Posture:** Behavior-Preserving  
**Audit Verdict:** **5.0 / 5** — Behavior preserved; hook ordering invariant held; no CI weakening; scope discipline maintained (inner-loop output path only)

---

## 1. Executive Summary

**Wins:**

* Inner-loop **decode → postprocess → save** relocated to `modules/runtime/decode_runtime.py` while **script hooks** (`postprocess_batch`, `postprocess_image`, `postprocess_maskoverlay`, `postprocess_image_after_composite`) remain in `processing.py` in the **same order**  
* `decode_latent_batch` / `DecodedSamples` moved to runtime to avoid **import cycles**; HR paths only swap import target  
* **Quality** post-merge run includes **`test_decode_runtime.py`** plus existing runner/sampler contracts; **79 passed**, **40%** coverage gate satisfied  
* No relaxation of coverage threshold, pip-audit policy, or workflow gates  

**Risks:**

* None identified for this extraction. Lazy import of `apply_color_correction` / `apply_overlay` is intentional and matches deferred-import precedent (M16/M17).

**Next action:** Proceed to **M19** — model provider interface.

---

## 2. Delta Map & Blast Radius

**Changed:**

* `modules/runtime/decode_runtime.py` (new)  
* `modules/processing.py` — `process_images_inner` delegation; HR `decode_latent_batch` call sites  
* `modules/runtime/__init__.py`, `modules/runtime/processing_runtime.py` (comments)  
* `test/quality/test_decode_runtime.py` (new)  
* `docs/milestones/M18/*`, `docs/serena.md`  

**Consumer surfaces touched:** None. `process_images`, `ProcessingRunner`, API/UI unchanged.

**Blast radius:** Inner generation output path; failures would appear in generation/smoke/quality — **none observed**.

---

## 3. Architecture & Modularity Review

* **Boundary:** One-direction `processing` → `decode_runtime` for the extracted stages; runtime does **not** own script hooks  
* **Cycles:** Avoided via moved `decode_latent_batch` and lazy import inside `postprocess_images_for_row`  
* **Scope:** No repo-wide normalization of other decode/save sites (per plan)  

**Keep:** Current split. **Fix now:** None. **Defer:** Model injection abstraction (M19).

---

## 4. CI/CD & Workflow Audit

| Gate | Result |
|------|--------|
| Linter (PR + main) | ✓ |
| Smoke (PR #36) | ✓ |
| Quality (`main`, run 23321103961) | ✓ |
| Coverage ≥40% | ✓ (40% reported) |
| pip-audit / Node annotations | Informational only; policy unchanged |

**CI weakening:** None.

---

## 5. Tests, Coverage, and Invariants

* **New tests:** Delegation + textual stage-order + static check for stack/normalize in `decode_latents`  
* **Hook ordering:** Preserved by construction (hooks stay in `processing.py`)  
* **Flake:** None observed  

---

## 6. Refactor Guardrail Compliance

| Guardrail | Status |
|-----------|--------|
| Behavior preservation | PASS |
| Hook ordering / call-site location | PASS |
| Scope = `process_images_inner` output stage | PASS |
| No silent CI weakening | PASS |
| No unrelated decode/save churn | PASS |

---

## 7. Top Issues

None.

---

## 8. Quality Gates

| Gate | Result |
|------|--------|
| Invariants | PASS |
| CI truthfulness | PASS |
| Tests + coverage | PASS |
| Extraction discipline | PASS |

---

## 9. Audit Score

**5.0 / 5** — Mechanical extraction with explicit hook preservation and full post-merge Quality evidence.
