# M15_plan — Queue / Background Runner Preparation

## 1. Intent / Target

**Primary objective:**

Introduce a **queue-capable execution path at the runner layer** while preserving the current synchronous behavior.

> This is the first step toward async execution, cancellation, and multi-request orchestration.

---

### Why this matters

From M14:

```text
API → process_images → ProcessingRunner
UI  → process_images → ProcessingRunner
```

Now:

> We can insert queueing **inside the runner** without touching API/UI.

---

### M15 Goal (precise)

* Add **optional queued execution capability**
* Maintain **default synchronous behavior**
* Introduce **no user-visible changes**

---

## 2. Scope Boundaries

### In Scope

* `modules/runtime/runner.py`
* New queue abstraction (e.g. `execution_queue.py`)
* Minimal supporting structures

### Out of Scope

* API changes (no new endpoints)
* UI changes
* True async execution (just preparation)
* Distributed execution
* Persistence layer
* Cancellation UI/API (only internal prep)

---

## 3. Invariants (Must Not Change)

From invariant registry:

### Runtime

* Output images identical
* Seeds produce identical outputs
* Execution order unchanged (single request)

### API / UI

* Response format unchanged
* Blocking behavior unchanged (still synchronous)

### System

* Extensions unaffected
* CLI unchanged
* Coverage ≥ 40%

---

## 4. Verification Plan

### Tests (Required)

#### 1. Runner Default Path Test

* Ensure `ProcessingRunner.run()` behaves exactly as before
* No queue usage unless explicitly enabled

---

#### 2. Queue Invocation Test (NEW)

* Enable queue mode (internal flag)
* Assert:

  * request enters queue
  * execution still completes correctly

---

#### 3. Contract Preservation

* Re-run:

  * `test_txt2img_path_uses_runner`
  * `test_api_runner_contract`

Ensure:

> Queue introduction does NOT break routing guarantees

---

### CI Signals

* Linter ✓
* Smoke ✓
* Quality ✓
* Coverage ≥ 40% ✓

---

## 5. Implementation Steps (Small, Reversible)

### Step 1 — Introduce ExecutionQueue (Minimal)

Create:

```
modules/runtime/execution_queue.py
```

Minimal structure:

```python
class ExecutionQueue:
    def submit(self, request, fn):
        return fn(request)  # pass-through for now
```

⚠️ Important:

* No threading
* No async
* No behavior change

---

### Step 2 — Integrate into Runner (Behind Flag)

In `ProcessingRunner.run()`:

```python
if self.use_queue:
    return self.queue.submit(request, self._execute)
else:
    return self._execute(request)
```

Default:

```python
self.use_queue = False
```

---

### Step 3 — Preserve Lifecycle

Ensure:

```text
prepare → execute → finalize
```

is unchanged.

Queue wraps only the **execution call**, not lifecycle ordering.

---

### Step 4 — Add Internal Hook Point

Introduce:

```python
def _execute(self, request):
    return existing_execution_logic
```

This becomes:

> Future insertion point for:

* async
* retries
* cancellation
* batching

---

### Step 5 — Add Tests

Create:

```
test/quality/test_runner_queue_mode.py
```

Test:

* queue enabled
* execution still completes
* runner lifecycle preserved

---

### Step 6 — Validate No Behavior Drift

* Compare outputs (seed-based)
* Ensure identical results

---

## 6. Risk & Rollback Plan

### Risk Level: LOW–MEDIUM

Why:

* Touching execution path (runner)
* But behind a flag

---

### Risks

| Risk                   | Mitigation                   |
| ---------------------- | ---------------------------- |
| Lifecycle disruption   | Preserve call order strictly |
| Hidden async behavior  | No async allowed             |
| Extension interference | Keep queue internal only     |

---

### Rollback

* Remove queue integration block
* No API/UI impact
* Single-module rollback

---

## 7. Deliverables

### Code

* `execution_queue.py`
* Updated `runner.py`

### Tests

* `test_runner_queue_mode.py`

### Docs

* `M15_plan.md`
* `M15_run1.md`, `M15_run2.md`
* `M15_summary.md`
* `M15_audit.md`

### Ledger

* Add M15 entry

---

## 8. Acceptance Criteria

### Functional

* Default execution unchanged
* Outputs identical

### Structural

* Runner supports queue mode (disabled by default)
* Execution path isolated in `_execute`

### Verification

* All CI green
* Coverage maintained
* Contract tests still pass

---

## 9. Architectural Outcome

### Before

```text
runner.run → execute
```

### After

```text
runner.run → (optional queue) → execute
```

---

## 10. Strategic Impact

M15 enables:

### Immediate

* Controlled execution layer
* Hook point for orchestration

### Next (M16+)

* Runtime extraction
* Async execution
* Cancellation
* Multi-request batching

---

# 🧠 Key Guidance for Cursor

* This is **NOT a queue system**
* This is a **queue insertion seam**
* Behavior must remain identical

---

# ✅ Final Instruction

Proceed with M15:

* Minimal diff
* No async
* No behavior change
* Add seam only
* Prove via tests
