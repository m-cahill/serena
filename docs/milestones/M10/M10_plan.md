# M10 — ProcessingRunner Skeleton

Phase: **Phase III — Runner & Service Boundary**
Status: Planned

---

# 1. Intent / Target

Introduce the **ProcessingRunner** abstraction that will become the unified execution surface for Serena.

Currently the pipeline is invoked directly through internal orchestration code.
This milestone introduces a **runner boundary** that:

- encapsulates pipeline execution
- standardizes runtime entrypoints
- prepares Serena for CLI / API / service mode

The runner initially acts as a **thin adapter** around existing behavior.

No behavior changes are permitted.

---

# 2. Scope Boundaries

### In scope

- Create `ProcessingRunner` skeleton at `modules/runtime/runner.py`
- Define `ProcessingRequest` wrapping `StableDiffusionProcessing`
- Wire `process_images` to delegate through runner (internal only)
- Maintain existing CLI/UI/API/scripts behavior
- Add minimal contract test at `test/quality/test_processing_runner.py`

### Out of scope

- No runtime behavior changes
- No async processing yet
- No service layer
- No multiprocessing
- No new configuration surfaces
- No performance changes
- No RuntimeContext in runner (M10)

---

# 3. Clarifications (Authoritative)

| Decision | Choice |
|----------|--------|
| Module path | `modules/runtime/runner.py` |
| ProcessingRequest | Wraps `p`: `ProcessingRequest(processing=p)` |
| RuntimeContext | Not passed to runner; omit from constructor |
| Wiring | Inside `process_images` only; all callers unchanged |
| Test location | `test/quality/test_processing_runner.py` |

---

# 4. Invariants

| Surface | Invariant | Verification |
|---------|-----------|--------------|
| CLI behavior | Identical outputs and execution path | smoke tests |
| API responses | No schema changes | tests |
| Processing results | Byte-identical outputs | golden comparison |
| Runtime state | No side effects introduced | test suite |
| CI coverage | ≥ 40% | CI gate |

---

# 5. Implementation Steps

## Step 1 — Create runner module

Create `modules/runtime/runner.py`:

```python
class ProcessingRequest:
    def __init__(self, processing):
        self.processing = processing

class ProcessingRunner:
    def run(self, request):
        from modules.processing import process_images_inner
        return process_images_inner(request.processing)
```

## Step 2 — Wire process_images

Inside `process_images`, replace:

```python
res = process_images_inner(p)
```

With:

```python
from modules.runtime.runner import ProcessingRunner, ProcessingRequest
runner = ProcessingRunner()
request = ProcessingRequest(p)
res = runner.run(request)
```

## Step 3 — Add contract test

Add `test/quality/test_processing_runner.py` with delegation test.

---

# 6. Risk & Rollback Plan

Risk level: **Low**

Mechanical refactor. Rollback: revert wiring commit.

---

# 7. Deliverables

Code: `modules/runtime/runner.py`, wiring in `process_images`
Tests: `test/quality/test_processing_runner.py`
Docs: M10_toolcalls.md, M10_run1.md, M10_summary.md, M10_audit.md
Ledger: Update `docs/serena.md`
Tag: `v0.0.10-m10`
