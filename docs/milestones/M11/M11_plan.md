# M11 — Runner Lifecycle Surface

Phase: **Phase III — Runner & Service Boundary**
Status: Planned

---

# 1. Intent / Target

Introduce lifecycle structure on ProcessingRunner:

```
runner.prepare()
runner.execute()
runner.finalize()
```

This enables:
* cancellation
* instrumentation
* progress reporting
* distributed execution (later milestones)

Behavior-preserving. No runtime changes yet.

---

# 2. Scope Boundaries

### In scope

* Add prepare / execute / finalize structure to ProcessingRunner
* Route existing run() logic through execute()
* Maintain identical behavior
* Add minimal contract tests

### Out of scope

* No cancellation implementation yet
* No async
* No instrumentation hooks (M12)
* No txt2img path through runner (M13)

---

# 3. Invariants

| Surface | Invariant | Verification |
|---------|-----------|--------------|
| CLI behavior | Identical | smoke tests |
| API responses | Unchanged | tests |
| Processing results | Byte-identical | quality tests |
| CI coverage | ≥ 40% | CI gate |

---

# 4. Deliverables

Code: `modules/runtime/runner.py` (lifecycle methods)
Tests: `test/quality/test_processing_runner.py` (lifecycle contract)
Docs: M11_plan.md, M11_toolcalls.md, M11_run1.md, M11_summary.md, M11_audit.md
Ledger: Update `docs/serena.md`
Tag: `v0.0.11-m11`
