# M06 Plan — Prompt / Seed Preparation Extraction

Project: Serena  
Phase: Phase II — Runtime Seam Preparation  
Milestone: M06  
Title: Prompt / seed prep extraction  
Posture: Behavior-preserving refactor  
Target: Extract prompt + seed preparation logic from processing.py

---

# 1. Intent / Target

`modules/processing.py` currently performs multiple responsibilities inside
`process_images()` and `process_images_inner()` including:

- prompt parsing
- seed preparation
- subseed logic
- batch seed generation
- variation seed handling
- negative prompt expansion

These steps are mixed with sampling and decoding logic.

The goal of M06 is to **extract prompt and seed preparation into a dedicated module**
while preserving the exact runtime behavior.

This milestone **does NOT change generation semantics**.

It only relocates preparation logic behind a clean function boundary.

This prepares for:

- M07 — opts snapshot introduction
- M08 — process_images_inner snapshot threading
- M09 — execution context/state seam

---

# 2. Scope Boundaries

## In Scope

Extract logic related to:

- prompt parsing
- negative prompt preparation
- seed normalization
- subseed handling
- seed list generation
- batch seed assignment
- seed resizing logic
- variation strength seed mixing

Target location:

```
modules/prompt_seed_prep.py
```

Expose a pure helper function:

```
prepare_prompt_seed_state(p: StableDiffusionProcessing)
```

Return a small structured result object.

---

## Out of Scope

The following must remain unchanged:

- sampler execution
- conditioning generation
- latent creation
- decode pipeline
- model/VAE loading
- token merging logic
- override_settings seam (M05)
- extension hooks

No API/UI behavior changes are allowed.

---

# 3. Invariants

The following behaviors must remain identical.

### Prompt handling

- prompt lists identical
- negative prompt behavior unchanged
- prompt matrix logic preserved
- prompt parser behavior unchanged

### Seed handling

- seed generation identical
- subseed behavior identical
- variation seeds identical
- batch seeds identical
- deterministic runs unchanged

### Extension compatibility

Extensions reading prompt or seed fields must behave identically.

### API compatibility

txt2img / img2img endpoints must return identical responses.

### Generation determinism

Given identical inputs, outputs must remain identical.

---

# 4. Verification Plan

## CI Verification

Existing CI gates remain unchanged.

Required passing checks:

Smoke Tests  
Linter  
Quality Tests  
Coverage ≥ 40%

---

## Runtime verification

Smoke tests already exercise:

```
txt2img
img2img
```

which invoke the full generation pipeline.

If prompt or seed handling breaks, smoke tests will fail.

---

## Local verification (recommended)

Cursor should run:

```
pytest test/smoke
pytest test/quality
```

---

# 5. Implementation Steps

## Step 1 — Identify extraction block

Locate code inside `modules/processing.py` responsible for:

- prompt normalization
- negative prompt handling
- seed initialization
- subseed preparation
- batch seed generation

These sections should be grouped logically.

---

## Step 2 — Create new module

Create:

```
modules/prompt_seed_prep.py
```

Add:

```
prepare_prompt_seed_state(p)
```

This function should:

1. Read prompt + seed values from `p`
2. Perform all current preparation logic
3. Return a structured result

Example structure:

```
PromptSeedState
prompts
negative_prompts
seeds
subseeds
subseed_strength
seed_resize
```

The structure should mirror the values currently produced in `processing.py`.

---

## Step 3 — Replace inline logic

Replace the extracted code in `processing.py` with:

```
state = prepare_prompt_seed_state(p)
```

Then reference fields from `state`.

---

## Step 4 — Maintain identical behavior

Important:

Do NOT change:

- variable names used by extensions
- field assignments on `p`
- order of operations
- default values
- seed calculation logic

This must be a **mechanical extraction only**.

---

## Step 5 — Minimal tests

No new tests are required for M06 unless extraction introduces new seams.

Existing smoke + quality tests should cover behavior.

If helpful, a small unit test can be added:

```
test_prompt_seed_prep.py
```

but this is optional.

---

# 6. Risk & Rollback Plan

Risk: Low (mechanical extraction).

Potential failure modes:

- prompt list mismatch
- seed list mismatch
- extension accessing moved variables

Mitigation:

- Keep assignments on `p`
- Only move internal computation logic

Rollback:

Revert the commit.

Because the change is localized to:

```
modules/processing.py
modules/prompt_seed_prep.py
```

---

# 7. Deliverables

Expected files changed:

```
modules/prompt_seed_prep.py      (new)
modules/processing.py            (modified)
docs/milestones/M06/*            (plan, toolcalls, run reports)
```

No other modules should change.

---

# 8. Expected Outcome

After M06:

- prompt and seed preparation isolated
- `processing.py` becomes smaller
- preparation stage clearly separated from sampling stage

This unlocks:

M07 — Options snapshot introduction
M08 — Snapshot threading into process_images_inner
M09 — Execution context seam
