# M12 — Runner Instrumentation Surface

Phase: Phase III — Runner & Service Boundary  
Status: Planned

---

# 1. Intent / Target

Introduce an **instrumentation hook surface** on the ProcessingRunner lifecycle.

The runner currently exposes:

prepare → execute → finalize

This milestone introduces **optional lifecycle hooks** that allow later milestones
to attach progress tracking, tracing, and cancellation signals.

The hooks must default to **no-op behavior** so the processing pipeline remains unchanged.

---

# 2. Scope Boundaries

## In scope

• Add optional instrumentation hooks to ProcessingRunner  
• Keep hooks disabled by default  
• Ensure lifecycle execution order is unchanged  
• Add contract tests verifying hook invocation

## Out of scope

• No runtime behavior change  
• No progress reporting yet  
• No cancellation yet  
• No threading / async  
• No API changes  
• No CLI changes  

Instrumentation is only structural in this milestone.

---

# 3. Invariants

| Surface | Invariant | Verification |
|---------|-----------|--------------|
| CLI behavior | identical outputs | smoke tests |
| API responses | unchanged schemas | smoke tests |
| Processing results | identical images/metadata | quality tests |
| Runner lifecycle | prepare → execute → finalize | contract tests |
| Coverage | ≥ 40% | CI gate |

---

# 4. Verification Plan

CI must remain green.

Expected checks:

| Check | Expected |
|-------|----------|
| Linter | pass |
| Smoke Tests | pass |
| Quality Tests | pass (post-merge) |
| Coverage | ≥ 40% |

Manual verification:

```bash
pytest
```

---

# 5. Implementation Steps

## Step 1 — Add instrumentation hooks

Modify:

```
modules/runtime/runner.py
```

Add hook methods:

```python
class ProcessingRunner:

    def run(self, request):
        state = self.prepare(request)

        self.on_prepare(state)

        result = self.execute(state)

        self.on_execute(state, result)

        result = self.finalize(state, result)

        self.on_finalize(state, result)

        return result

    def on_prepare(self, state):
        pass

    def on_execute(self, state, result):
        pass

    def on_finalize(self, state, result):
        pass
```

Hooks must be **no-op by default**.

---

## Step 2 — Ensure lifecycle remains unchanged

Lifecycle order must still be:

```
prepare → on_prepare → execute → on_execute → finalize → on_finalize
```

And `execute` must still call:

```
process_images_inner(state.processing)
```

---

## Step 3 — Extend contract tests

File:

```
test/quality/test_processing_runner.py
```

Add test verifying hook invocation.

Example:

```python
def test_runner_hooks_called(monkeypatch, initialize):

    calls = []

    class TestRunner(ProcessingRunner):

        def on_prepare(self, state):
            calls.append("prepare_hook")

        def on_execute(self, state, result):
            calls.append("execute_hook")

        def on_finalize(self, state, result):
            calls.append("finalize_hook")

        def execute(self, state):
            return "result"

    runner = TestRunner()
    runner.run(ProcessingRequest(processing="dummy"))

    assert calls == ["prepare_hook", "execute_hook", "finalize_hook"]
```

---

# 6. Risk & Rollback Plan

Risk level: **Low**

Changes are internal to the runner.

Rollback:

1. revert runner instrumentation commit
2. restore previous runner lifecycle
3. re-run CI

No runtime data or external interfaces change.

---

# 7. Deliverables

Code:

```
modules/runtime/runner.py
```

Tests:

```
test/quality/test_processing_runner.py
```

Docs:

```
docs/milestones/M12/M12_plan.md
docs/milestones/M12/M12_toolcalls.md
docs/milestones/M12/M12_run1.md
docs/milestones/M12/M12_summary.md
docs/milestones/M12/M12_audit.md
```

Ledger update:

```
docs/serena.md
```

Tag:

```
v0.0.12-m12
```

---

# 8. Exit Criteria

M12 closes when:

• PR CI passes
• post-merge Quality Tests pass
• instrumentation runner merged
• ledger updated
• tag created
