# M17_plan — Sampler Runner Extraction

## 1. Intent / Target

### Primary objective

Extract **sampler invocation orchestration** from `modules/processing.py` into the runtime layer (`modules/runtime/`), following the extraction pattern established in M16.

This milestone moves:

> sampler creation + invocation + immediate latent handling

out of `StableDiffusionProcessing*.sample()` and into a dedicated runtime module.

---

### Why this matters

M16 proved:

> orchestration can move safely behind the runner boundary

M17 proves:

> **model execution (sampler) can move safely as well**

This is the **core runtime boundary**:

* before → orchestration extraction (M16)
* now → sampler extraction (M17)
* next → decode/save separation (M18)

---

## 2. Scope Boundaries

### In Scope

* Sampler **creation + invocation orchestration**
* Moving sampler call out of:

  * `StableDiffusionProcessingTxt2Img.sample`
  * `StableDiffusionProcessingTxt2Img.sample_hr_pass`
  * `StableDiffusionProcessingImg2Img.sample`
* New runtime module:

  * `modules/runtime/sampler_runtime.py`

---

### Out of Scope

* Decode logic (M18)
* Save/postprocess logic (M18)
* Model provider abstraction (M19)
* Script hook movement
* API/UI changes
* Runner lifecycle changes

---

## 3. Invariants (Must Not Change)

### Public behavior

* `process_images()` unchanged
* txt2img/img2img outputs identical for same inputs
* API responses unchanged
* file outputs unchanged

---

### Architectural invariants

* `ProcessingRunner` remains execution boundary
* Lifecycle order unchanged:

  ```
  prepare → execute → finalize
  ```
* Queue seam unchanged

---

### Critical runtime invariants

* Sampler selection behavior unchanged
* Seed determinism preserved
* Conditioning / unconditional conditioning unchanged
* Latent outputs identical
* Script hooks remain in `sample()` — do NOT move `process_before_every_sampling`

---

## 4. Extraction Target (Precise)

### Extract THIS:

Inside `sample()` / `sample_hr_pass()` methods:

* `sd_samplers.create_sampler(...)` (Txt2Img.sample, sample_hr_pass only; Img2Img keeps creation in init)
* call to:

  ```python
  sampler.sample(...)
  sampler.sample_img2img(...)
  ```
* handling of:

  * `x`
  * conditioning
  * unconditional conditioning
  * image conditioning (img2img)
* return of latent results

---

### Do NOT extract:

* decode (`decode_first_stage`)
* image save
* metadata construction
* script callbacks
* sampler creation from Img2Img.init()

---

## 5. Target Design

### New module

```
modules/runtime/sampler_runtime.py
```

### Core functions (TWO — mirror existing shapes)

```python
def run_sampler_txt2img(p, x, conditioning, unconditional_conditioning):
    """Txt2Img: create sampler, invoke sample(), return latents."""
    p.sampler = sd_samplers.create_sampler(p.sampler_name, p.sd_model)
    samples = p.sampler.sample(
        p, x, conditioning, unconditional_conditioning,
        image_conditioning=p.txt2img_image_conditioning(x)
    )
    return samples


def run_sampler_img2img(p, x, noise, conditioning, unconditional_conditioning, steps=None, image_conditioning=None, sampler_name=None):
    """Img2Img: invoke sample_img2img. If sampler_name provided (hr pass), create sampler first."""
    if sampler_name is not None:
        p.sampler = sd_samplers.create_sampler(sampler_name, p.sd_model)
    samples = p.sampler.sample_img2img(
        p, x, noise, conditioning, unconditional_conditioning,
        steps=steps, image_conditioning=image_conditioning
    )
    return samples
```

---

### Integration points

**Txt2Img.sample():**
```python
samples = sampler_runtime.run_sampler_txt2img(self, x, conditioning, unconditional_conditioning)
```

**sample_hr_pass():**
```python
samples = sampler_runtime.run_sampler_img2img(
    self, samples, noise, self.hr_c, self.hr_uc,
    steps=self.hr_second_pass_steps or self.steps,
    image_conditioning=image_conditioning,
    sampler_name=self.hr_sampler_name or self.sampler_name
)
```

**Img2Img.sample():**
```python
samples = sampler_runtime.run_sampler_img2img(
    self, self.init_latent, x, conditioning, unconditional_conditioning,
    image_conditioning=self.image_conditioning
)
```

---

## 6. M17 Rules (Condensed)

### What to extract

* Sampler invocation
* Immediate call to `sampler.sample` or `sampler.sample_img2img`
* Sampler creation (Txt2Img, sample_hr_pass only; Img2Img keeps creation in init)

### What must NOT move

* Sampler creation in `init()` (Img2Img)
* Script hooks
* Decode/save
* Metadata
* Lifecycle

### Argument fidelity

Preserve exact argument order, values, and defaults.

---

## 7. Implementation Steps

### Step 1 — Create runtime module

* Add `modules/runtime/sampler_runtime.py`
* Implement `run_sampler_txt2img(...)` and `run_sampler_img2img(...)`

### Step 2 — Extract sampler call

* Replace invocation in `StableDiffusionProcessingTxt2Img.sample`
* Replace invocation in `StableDiffusionProcessingTxt2Img.sample_hr_pass`
* Replace invocation in `StableDiffusionProcessingImg2Img.sample`

### Step 3 — Preserve structure

* Keep method signatures unchanged
* Keep all pre/post logic in place
* Only replace sampler invocation block

### Step 4 — Avoid import cycles

* Use local imports if needed
* Do not introduce circular dependencies

### Step 5 — Add tests

Create `test/quality/test_sampler_runtime.py`:

1. Delegation test: monkeypatch `sampler_runtime.run_sampler_*`, assert sample() calls it
2. Module existence: assert sampler_runtime exposes both functions

---

## 8. Verification Plan

### Required CI signals

* Linter ✓
* Smoke ✓
* Quality ✓
* Coverage ≥40%

---

## 9. Deliverables

### Code

* `modules/runtime/sampler_runtime.py`
* updated `processing.py`

### Tests

* `test_sampler_runtime.py`

### Docs

* `M17_run1.md`
* `M17_summary.md`
* `M17_audit.md`
* `docs/serena.md` updated

---

## 10. Acceptance Criteria

M17 is complete when:

* Sampler invocation lives in runtime module
* `processing.py` no longer directly calls sampler
* All tests pass
* Outputs unchanged
* CI green
* No scope creep

---

## 11. One-Line Summary

> Extract sampler execution into `modules/runtime/sampler_runtime.py`, preserving all behavior and using the M16 runtime pattern.
