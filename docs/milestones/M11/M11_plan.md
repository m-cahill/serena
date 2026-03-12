# M11 — Runner Lifecycle Surface

Phase: **Phase III — Runner & Service Boundary**
Status: Completed

---

# 1. Intent / Target

Introduce a **lifecycle structure** for the ProcessingRunner.

The runner currently exposes a single method: `ProcessingRunner.run(request)`.

This milestone refactors the internal implementation into three lifecycle stages:

```
prepare → execute → finalize
```

This creates a **stable execution surface** that later milestones can instrument
(progress tracking, cancellation, API runners, queue workers).

Behavior must remain identical.

---

# 2. Scope Boundaries

## In scope

* Add lifecycle methods to ProcessingRunner
* Refactor run() to delegate to lifecycle stages
* Add minimal lifecycle contract test
* Preserve all current execution behavior

## Out of scope

* No API changes
* No CLI changes
* No runtime behavior changes
* No async / threading
* No cancellation yet
* No instrumentation yet

Those come in later Phase III milestones.

---

# 3. Invariants

| Surface | Invariant | Verification |
|---------|-----------|--------------|
| CLI behavior | identical outputs | smoke tests |
| API responses | unchanged schemas | smoke tests |
| Processing results | identical images / metadata | golden outputs |
| Runtime context | still created inside process_images_inner | code review |
| Coverage | ≥ 40% | CI gate |

---

# 4. Verification Plan

CI must remain green.

Expected CI checks:

| Check | Expected |
|-------|----------|
| Linter | pass |
| Smoke Tests | pass |
| Quality Tests | pass (post-merge) |
| Coverage | ≥ 40% |

Manual verification: `pytest`

Runner contract tests must pass.

---

# 5. Implementation Steps

## Step 1 — Extend ProcessingRunner

File: `modules/runtime/runner.py`

Refactor runner:

```python
class ProcessingRunner:

    def run(self, request):
        state = self.prepare(request)
        result = self.execute(state)
        return self.finalize(state, result)

    def prepare(self, request):
        return request

    def execute(self, state):
        from modules.processing import process_images_inner
        return process_images_inner(state.processing)

    def finalize(self, state, result):
        return result
```

Important: prepare/execute/finalize must remain **pass-through behavior**.

## Step 2 — Preserve delegation

Call graph must remain:

```
process_images(p)
      │
      ▼
ProcessingRunner.run(request)
      │
      ▼
prepare
      │
execute
      │
finalize
      │
      ▼
process_images_inner(p)
```

## Step 3 — Update contract tests

Add lifecycle verification.

File: `test/quality/test_processing_runner.py`

Add test verifying lifecycle order. Keep existing `test_processing_runner_delegates`.

---

# 6. Risk & Rollback Plan

Risk level: **Low**

Changes are mechanical and internal.

Rollback: revert runner lifecycle commit, restore single run(), re-run CI.

No runtime data or external API surfaces change.

---

# 7. Deliverables

Code: `modules/runtime/runner.py` lifecycle implementation

Tests: updated `test_processing_runner.py`

Docs: M11_plan.md, M11_toolcalls.md, M11_run1.md, M11_summary.md, M11_audit.md

Ledger update: `docs/serena.md`

Tag: `v0.0.11-m11`

---

# 8. Exit Criteria

M11 closes when:

* PR CI passes
* post-merge Quality Tests pass
* lifecycle runner merged
* ledger updated
* tag created
