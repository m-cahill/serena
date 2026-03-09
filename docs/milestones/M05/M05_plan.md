# M05 Plan — Override Isolation / Temporary Opts Seam

**Project:** Serena
**Phase:** Phase II — Runtime Seam Preparation
**Milestone:** M05
**Title:** Override Isolation / Temporary Opts Seam
**Branch:** `m05-override-isolation`
**Posture:** Behavior-Preserving Refactor
**Target:** Introduce an isolated mechanism for temporary option overrides during generation.

---

# 1. Intent / Target

Introduce a **temporary options override seam** that prevents direct mutation of `shared.opts` during generation runs.

Currently, `process_images()` temporarily mutates global options when applying `override_settings`, then restores them afterward.

This milestone introduces a **context-managed override mechanism** that:

* isolates temporary option changes
* preserves runtime behavior
* prepares the runtime pipeline for future **opts snapshot injection**

This is the **first runtime seam milestone** in Phase II.

---

# 2. Problem Being Solved

The current implementation inside `modules/processing.py` roughly resembles:

```python
for k, v in p.override_settings.items():
    opts.set(k, v)

process_images_inner(p)

restore_settings()
```

Issues:

* mutates **global state**
* creates potential nondeterminism
* makes testing harder
* couples generation pipeline to `shared.opts`

This milestone **does not change behavior**, but introduces a **structured override mechanism**.

---

# 3. Scope Boundaries

### In scope

* Introduce a **temporary options context manager**
* Replace inline override logic in `process_images()`
* Ensure restoration logic is deterministic
* Preserve identical runtime semantics

### Explicitly out of scope

* Changing how `opts` values are accessed elsewhere
* Introducing `opts_snapshot` (M07)
* Changing processing pipeline structure
* Any modification to API/UI behavior
* Performance changes

---

# 4. Invariants (Must Not Change)

The following runtime surfaces **must remain identical**:

| Surface              | Verification                  |
| -------------------- | ----------------------------- |
| Image outputs        | Smoke tests                   |
| API response schemas | API tests                     |
| CLI behavior         | Smoke tests                   |
| Extension behavior   | Extension loading smoke       |
| Generation semantics | txt2img / img2img smoke tests |

These invariants are part of the Serena invariant registry.

---

# 5. Verification Plan

### CI gates expected to remain green

* Smoke tests
* Quality tests
* Coverage ≥ 40%
* verify_pinned_deps
* pip-audit (informational)

### Evidence artifacts

CI should still produce:

```
coverage.xml
ci_environment.txt
```

as introduced in M04.

### Behavioral verification

* Compare outputs from smoke generation tests
* Ensure override settings behave identically

---

# 6. Implementation Steps

## Step 1 — Add temporary override context manager

Create helper:

```
modules/runtime_utils.py
```

(or similar location appropriate to project structure)

Add:

```python
from contextlib import contextmanager
from modules import shared


@contextmanager
def temporary_opts(overrides: dict):
    if not overrides:
        yield
        return

    original = {}

    try:
        for key, value in overrides.items():
            if hasattr(shared.opts, key):
                original[key] = getattr(shared.opts, key)
                shared.opts.set(key, value)

        yield

    finally:
        for key, value in original.items():
            shared.opts.set(key, value)
```

Purpose:

* isolate override logic
* centralize restore semantics
* enable later replacement with snapshot model

---

## Step 2 — Replace override block in `process_images()`

Locate override logic inside:

```
modules/processing.py
```

Replace pattern similar to:

```python
for k, v in p.override_settings.items():
    opts.set(k, v)

process_images_inner(p)

restore_settings()
```

with:

```python
with temporary_opts(p.override_settings):
    process_images_inner(p)
```

---

## Step 3 — Remove redundant restore logic

Remove manual restore code now handled by context manager.

Ensure behavior remains identical.

---

## Step 4 — Minimal unit test

Add small test under:

```
test/quality/test_opts_override.py
```

Example:

```python
def test_temporary_opts_restores_value():
    from modules import shared
    from modules.runtime_utils import temporary_opts

    original = shared.opts.some_option

    with temporary_opts({"some_option": "test_value"}):
        assert shared.opts.some_option == "test_value"

    assert shared.opts.some_option == original
```

Purpose:

* verify restoration behavior
* protect seam for future milestones

---

## Step 5 — Ensure no behavior drift

Run:

```
pytest
```

Verify:

* generation tests unchanged
* API tests unchanged
* coverage still ≥ 40%

---

# 7. Risk & Rollback Plan

### Risk

Low.

Changes are isolated to override application.

### Potential issue

If extensions rely on exact ordering of override logic.

### Rollback

Revert the commit introducing:

```
temporary_opts
```

and restore original override block.

Because the change is localized, rollback is trivial.

---

# 8. Deliverables

### Code

New helper:

```
modules/runtime_utils.py
```

Modified:

```
modules/processing.py
```

New test:

```
test/quality/test_opts_override.py
```

---

### Documentation

Update milestone artifacts:

```
docs/milestones/M05/M05_summary.md
docs/milestones/M05/M05_audit.md
```

Update ledger:

```
docs/serena.md
```

---

# 9. Acceptance Criteria

M05 is complete when:

* CI passes
* Coverage ≥ 40%
* Override logic replaced with context manager
* Runtime behavior unchanged
* Milestone documentation completed
* Audit score remains **5.0**

---

# 10. Expected Architectural Impact

Before:

```
process_images
 └─ mutate shared.opts
```

After:

```
process_images
 └─ temporary_opts
     └─ process_images_inner
```

This creates the **first runtime seam** required for Phase II.

---

# 11. Next Milestone

```
M06 — Prompt / Seed Preparation Extraction
```

Goal:

Extract prompt + seed preparation logic from `process_images_inner()`.
