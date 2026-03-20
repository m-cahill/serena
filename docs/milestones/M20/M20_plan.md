# M20 Plan — Runtime tests with mockable boundaries

**Milestone:** M20 — Runtime tests with mockable boundaries  
**Phase:** Phase IV — Runtime Extraction  
**Status:** Canonical plan (locked 2026-03-19)

---

## 1. Intent / Target

### Primary objective

Introduce **mockable runtime boundaries** and **deterministic runtime tests** that allow:

```text
full pipeline execution WITHOUT real model / GPU
```

This milestone proves:

> The runtime (orchestration + sampler + decode/save + model access) is fully testable via dependency injection.

### Why this matters

After M19:

```text
runtime → model_provider → model
```

M20 proves:

```text
runtime → fake_model_provider → fake model → deterministic output
```

This is the first **end-to-end validation of architectural decoupling**.

---

## 2. Scope Boundaries

### In Scope

* Introduce **FakeModelProvider**
* Introduce **FakeModel / stubbed model behavior**
* Add deterministic runtime tests using fake provider
* Validate full pipeline execution without real model (via **ProcessingRunner** → `process_images_inner`)

### Out of Scope

* Changing real model behavior
* Refactoring sampler logic
* Performance improvements
* UI/API changes
* Extension API changes

---

## 3. Invariants (Must Not Change)

### Public behavior

* Real execution path unchanged
* API/UI behavior unchanged
* No change to real model outputs

### Architectural invariants

* `ProcessingRunner` unchanged
* `ModelProvider` contract unchanged
* Runtime modules unchanged (`processing_runtime`, `sampler_runtime`, `decode_runtime`, `model_provider`)

---

## 4. Test entry (locked)

**Runner-first ONLY:**

```python
runner = ProcessingRunner(model_provider=FakeModelProvider())
runner.run(ProcessingRequest(p))
```

Do **not** call `process_images` or UI/API explicitly; the runner still delegates to `process_images_inner` (expected).

---

## 5. Failure test contract (locked)

When the fake model / provider raises, the exception **propagates unchanged** (`pytest.raises`).

---

## 6. Fake surface (locked)

**Minimal — runtime-only:** satisfy sampler + decode expectations reachable from the stubbed path. No extension/script/UI coupling in the fake.

---

## 7. Determinism (locked)

Structural equivalence (counts, shapes, repeatable outputs) — not pixel-perfect diffusion output.

---

## 8. Deliverables

### Code

* `test/fixtures/fake_model.py`

### Tests

* `test/quality/test_runtime_mock.py` (full pipeline, determinism, failure propagation, provider `get_model` called)

### Docs (after CI green)

* `M20_run1.md`, `M20_summary.md`, `M20_audit.md`
* Ledger update in `docs/serena.md`

---

## 9. Acceptance Criteria

* Runtime path executes without GPU / real weights
* Fake provider works end-to-end through **ProcessingRunner**
* CI green (linter, smoke, quality, coverage ≥ 40%)
* No runtime module diffs

---

## 10. One-Line Summary

> Prove that the runtime is fully mockable and executable without a real model using a fake model provider.
