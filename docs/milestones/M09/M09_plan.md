# M09 Plan — Execution Context Introduction

Project: **Serena**
Phase: **Phase II — Runtime Seam Preparation**
Milestone: **M09**
Title: **Execution Context Introduction**

Branch: `m09-execution-context`

---

## 1. Intent / Target

M08 migrated runtime reads from `shared.opts` to `p.opts_snapshot` inside the generation pipeline.

However the runtime still depends heavily on **global shared state**:

- `shared.sd_model`
- `shared.device`
- `shared.state`
- `shared.cmd_opts`

These globals prevent the generation pipeline from becoming a **testable runtime component**.

The goal of **M09** is to introduce a **lightweight runtime execution context** that groups these runtime dependencies together.

Example concept:

```python
RuntimeContext(
    model,
    opts_snapshot,
    device,
    state,
    cmd_opts
)
```

The context will be **attached to the processing object** but will **not yet replace global state everywhere**.

This milestone introduces the seam without changing behavior.

---

## 2. Scope Boundaries

### In Scope

Create a new runtime structure:

```
modules/runtime_context.py
```

Define `RuntimeContext` with fields:

- `model`
- `opts_snapshot`
- `device`
- `state`
- `cmd_opts`

Attach it during generation:

```
p.runtime_context
```

Initial wiring occurs in `process_images_inner()`:

```python
p.runtime_context = RuntimeContext(
    model=shared.sd_model,
    opts_snapshot=p.opts_snapshot,
    device=shared.device,
    state=shared.state,
    cmd_opts=shared.cmd_opts,
)
```

Place this **after snapshot creation**.

### Out of Scope

M09 must **NOT**:

- remove `shared.sd_model`
- remove `shared.device`
- modify extension interfaces
- change sampling behavior
- change API responses
- refactor the sampler pipeline

The context exists **in parallel with shared state** for now.

---

## 3. Invariants

The following must remain identical.

| Invariant | Description |
|-----------|-------------|
| Generation determinism | Same inputs → same outputs |
| Sampling math | No changes to samplers or conditioning |
| File outputs | Paths and naming unchanged |
| Extension compatibility | Extensions must still use `shared.*` |
| API behavior | txt2img/img2img responses unchanged |
| CLI behavior | No change to CLI flags |

---

## 4. Verification Plan

CI gates must remain green.

| Check | Requirement |
|-------|-------------|
| Linter | Pass |
| Smoke tests | Pass |
| Quality tests | Pass |
| Coverage | ≥ 40% |

Local verification:

```
pytest test/smoke
pytest test/quality
```

Manual checks:

- txt2img generation
- img2img generation
- highres fix
- image saving
- grid saving

---

## 5. Implementation Steps

### Step 1 — Create runtime context module

Create file: `modules/runtime_context.py`

```python
from dataclasses import dataclass

@dataclass
class RuntimeContext:
    model: object
    opts_snapshot: object
    device: object
    state: object
    cmd_opts: object
```

### Step 2 — Attach context to processing object

Modify: `modules/processing.py`

Inside `process_images_inner()`, after snapshot creation:

```python
from modules.runtime_context import RuntimeContext

p.runtime_context = RuntimeContext(
    model=shared.sd_model,
    opts_snapshot=p.opts_snapshot,
    device=shared.device,
    state=shared.state,
    cmd_opts=shared.cmd_opts,
)
```

### Step 3 — No migration yet

Do **NOT** change runtime reads yet.

For example this must remain:

```python
shared.sd_model
shared.device
```

The context is introduced but **not yet consumed**.

---

## 6. Risk & Rollback Plan

Risk level: **Very low**

Changes introduce a new object but do not change runtime behavior.

| Risk | Mitigation |
|------|------------|
| Missing import | CI smoke tests |
| Attribute collision | Use `runtime_context` name |

Rollback: `git revert milestone commit`

---

## 7. Deliverables

Expected code changes:

- `modules/runtime_context.py` (new)
- `modules/processing.py` (modified)

Documentation artifacts:

- `docs/milestones/M09/M09_plan.md`
- `docs/milestones/M09/M09_toolcalls.md`

---

## 8. Expected Outcome

After M09 the generation runtime will expose `p.runtime_context` which groups:

- `model`
- `opts_snapshot`
- `device`
- `state`
- `cmd_opts`

The runtime seam stack becomes:

```
temporary_opts()             M05
prepare_prompt_seed_state()  M06
opts snapshot                M07
snapshot threading           M08
execution context            M09
```

This completes **Phase II runtime seam preparation**.

---

## 9. Success Criteria

M09 is complete when:

- [ ] Runtime context introduced
- [ ] Context attached to processing object
- [ ] CI fully green
- [ ] No behavior change
- [ ] Milestone artifacts generated
- [ ] Ledger updated
- [ ] Tag created: `v0.0.09-m09`
