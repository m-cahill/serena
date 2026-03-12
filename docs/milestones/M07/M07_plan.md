# M07 Plan — Opts Snapshot Introduction

Project: Serena
Phase: Phase II — Runtime Seam Preparation
Milestone: M07
Title: **Opts snapshot introduction**
Posture: Behavior-preserving refactor
Target: Introduce a stable **options snapshot mechanism** for generation runs.

Context: M06 isolated prompt/seed preparation into `prepare_prompt_seed_state(p)`, establishing a second runtime seam.

M07 introduces the **third seam**: a deterministic snapshot of `shared.opts` used for the duration of a generation run.

This prepares the runtime pipeline for dependency injection and removal of global option mutation in later milestones.

The milestone map defines this sequence explicitly:

* M05 — override isolation
* M06 — prompt/seed prep extraction
* **M07 — opts snapshot introduction**
* M08 — snapshot threading into `process_images_inner`
* M09 — execution context/state seam

---

# 1. Intent / Target

The current pipeline mutates `shared.opts` during generation via:

```
override_settings
```

This occurs in `process_images()` where overrides are temporarily applied and later restored.

This creates problems:

* hidden global mutation
* non-deterministic runtime state
* difficult testing

The goal of **M07** is to introduce an **immutable snapshot of opts** for generation runs without changing runtime behavior.

The snapshot is **not yet threaded through the runtime** (that happens in M08).

Instead, this milestone:

1. Creates a function that builds an **opts snapshot object**
2. Captures it once at the start of `process_images()`
3. Stores it on the processing object (`p.opts_snapshot`)

The runtime will continue to read from `shared.opts` for now.

This is purely **infrastructure preparation**.

---

# 2. Scope Boundaries

## In Scope

Introduce a new helper module:

```
modules/opts_snapshot.py
```

Add:

```
create_opts_snapshot(opts)
```

Responsibilities:

* Copy relevant values from `shared.opts`
* Return an immutable snapshot structure
* Attach snapshot to `StableDiffusionProcessing`

Example:

```
p.opts_snapshot = create_opts_snapshot(shared.opts)
```

Snapshot should include frequently accessed generation settings such as:

* outdir configuration
* sampler defaults
* VAE settings
* precision settings
* clip skip
* model settings

Exact contents may initially mirror `opts.data`.

---

## Out of Scope

This milestone **does NOT**:

* replace reads of `shared.opts`
* remove override logic
* change how options are applied
* modify extension access patterns
* alter UI/API option behavior

Those changes happen later (M08–M09).

---

# 3. Invariants

The following must remain identical.

### Generation behavior

Identical inputs must produce identical outputs.

### Options behavior

* override_settings logic unchanged
* UI settings unchanged
* CLI flags unchanged

### Extension compatibility

Extensions accessing:

```
shared.opts
```

must continue working.

### API compatibility

txt2img and img2img responses remain unchanged.

### Runtime state

No behavioral change to model loading or VAE logic.

---

# 4. Verification Plan

## CI Gates

All existing CI checks must pass:

* Smoke Tests
* Linter
* Quality Tests
* Coverage ≥ 40%

The CI suite already executes the generation path via API smoke tests.

If option behavior breaks, smoke tests will fail.

---

## Local verification

Recommended commands:

```
pytest test/smoke
pytest test/quality
```

---

# 5. Implementation Steps

## Step 1 — Create snapshot module

Create file:

```
modules/opts_snapshot.py
```

Add:

```
create_opts_snapshot(opts)
```

Example structure:

```python
from types import SimpleNamespace

def create_opts_snapshot(opts):
    return SimpleNamespace(**opts.data.copy())
```

Important properties:

* shallow copy of `opts.data`
* no mutation allowed

---

## Step 2 — Capture snapshot

Inside:

```
process_images_inner(p)
```

Add:

```
p.opts_snapshot = create_opts_snapshot(shared.opts)
```

Placement:

Immediately after prompt/seed preparation.

---

## Step 3 — Preserve override behavior

The snapshot must capture **post-override settings**.

Therefore ensure the snapshot is created **after override_settings are applied**.

Current order:

```
apply override_settings
prepare prompts/seeds
```

New order:

```
apply override_settings
prepare prompts/seeds
capture opts snapshot
```

---

## Step 4 — Avoid runtime behavior change

The snapshot should **not yet replace any option reads**.

Example:

Keep existing code:

```
opts.outdir_samples
```

Do NOT change to:

```
p.opts_snapshot.outdir_samples
```

That change occurs in **M08**.

---

## Step 5 — Minimal structural validation

Optionally add a small test:

```
test_opts_snapshot.py
```

Validate:

* snapshot contains expected attributes
* snapshot does not mutate when opts change afterward

This is optional.

---

# 6. Risk & Rollback Plan

Risk: **Very low**

Changes:

```
modules/opts_snapshot.py
modules/processing.py
```

Failure scenarios:

* snapshot created before overrides
* extension code accidentally reading snapshot

Mitigation:

* ensure snapshot is write-only in M07
* snapshot stored only on `p`

Rollback:

Revert the commit.

---

# 7. Deliverables

Expected files:

```
modules/opts_snapshot.py        (new)
modules/processing.py           (modified)
docs/milestones/M07/*           (plan, toolcalls, CI reports)
```

No other modules should change.

---

# 8. Expected Outcome

After M07:

* generation runs capture a **deterministic opts snapshot**
* runtime seams now include:

```
temporary_opts()           (M05)
prepare_prompt_seed_state  (M06)
opts snapshot              (M07)
```

These seams prepare the system for:

```
M08 — snapshot threading into process_images_inner
M09 — execution context/state seam
```

Together they begin removing the **global state dependency** identified in the pre-refactor audit.

---

# 9. Success Criteria

M07 is complete when:

* opts snapshot helper exists
* snapshot attached to `StableDiffusionProcessing`
* no runtime behavior change
* CI fully green
* milestone artifacts generated
* ledger updated
