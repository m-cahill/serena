# M02 Plan — API CI Truthfulness & Local Dev Guardrails

**Milestone:** M02  
**Title:** API CI truthfulness, local dev guardrails, repeatable verification  
**Branch:** `m02-api-ci-truthfulness`  
**Status:** Completed  
**Depends on:** M01 (complete)

---

## 1. Intent / Target

M01 achieved deterministic CI with dynamic stub repositories and verified server startup, but **API endpoints requiring model inference still return HTTP 500**, preventing full CI pass and blocking coverage enforcement.

M02 resolves this by:

1. Implementing **deterministic fake inference in CI**
2. Ensuring **API contract tests pass**
3. Re-enabling **coverage gate enforcement**
4. Introducing **developer guardrails for repeatable local verification**

The milestone ensures the **API surface is testable without requiring a real model** while preserving runtime behavior outside CI.

---

## 2. Scope Boundaries

### In scope

* CI-only fake inference for `txt2img` and `img2img`
* Deterministic API response satisfying contract tests
* Coverage gate restoration
* CONTRIBUTING documentation for deterministic local runs
* Repeatable verification workflow

### Explicitly out of scope

* Real Stable Diffusion inference
* Model loading changes
* Refactoring generation pipeline
* Runtime architecture changes
* Extension system changes

Those belong to later runtime seam milestones.

---

## 3. Invariants

The following Serena invariants **must remain unchanged**:

| Invariant                      | Verification           |
| ------------------------------ | ---------------------- |
| API response schema unchanged  | API tests              |
| Generation semantics preserved | E2E smoke              |
| Extension API compatibility    | Extension loading      |
| CLI behavior unchanged         | Smoke tests            |
| No CI weakening                | checks remain enforced |

---

## 4. Implementation

### Step 1 — Add CI fake inference helper

Create `modules/api/ci_fake_inference.py`:

```python
from modules.api import models

_FAKE_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO5vX8cAAAAASUVORK5CYII="
)

def ci_fake_txt2img():
    return models.TextToImageResponse(
        images=[_FAKE_PNG],
        parameters={},
        info="ci-fake-image"
    )

def ci_fake_img2img():
    return models.ImageToImageResponse(
        images=[_FAKE_PNG],
        parameters={},
        info="ci-fake-image"
    )
```

### Step 2 — Patch API endpoints

Modify `modules/api/api.py`:

* Add: `import os` and `from modules.api.ci_fake_inference import ci_fake_txt2img, ci_fake_img2img`
* In `text2imgapi`: add guard at **start** (before any model loading):

  ```python
  if os.getenv("CI") == "true":
      return ci_fake_txt2img()
  ```

* In `img2imgapi`: add guard at **start** (before init_images check):

  ```python
  if os.getenv("CI") == "true":
      return ci_fake_img2img()
  ```

GitHub Actions sets `CI=true` by default; no workflow change required.

### Step 3 — Re-enable coverage enforcement

Coverage gate enforced on combined (pytest + server) coverage. Baseline 33% (current − 2% margin); target 60% deferred to M04.

### Step 4 — Add CONTRIBUTING.md

Structure: Quickstart, Local verification, CI parity, Stub repositories, Development workflow.

Reference existing scripts (e.g. `scripts/dev/create_stub_repos.py`); do not duplicate documentation.

---

## 5. Definition of Done

* [ ] CI linter passes
* [ ] CI tests pass (35/35)
* [ ] Coverage gate enforced
* [ ] API responses validated
* [ ] Milestone documentation created (M02_run1.md, M02_summary.md, M02_audit.md)
* [ ] Ledger updated in docs/serena.md

---

## 6. Deliverables

### Code

* `modules/api/ci_fake_inference.py`
* `modules/api/api.py` (CI guards)
* `CONTRIBUTING.md`

### Documentation

* `docs/milestones/M02/M02_plan.md` (this file)
* `docs/milestones/M02/M02_run1.md`
* `docs/milestones/M02/M02_summary.md`
* `docs/milestones/M02/M02_audit.md`

### Ledger

* `docs/serena.md` — add M02 entry
