# M14_plan — API Integration Through ProcessingRunner

## 1. Intent / Target

**Primary objective:**
Ensure API generation paths (`/sdapi/v1/txt2img`, `/sdapi/v1/img2img`) **continue to route through** `process_images` → `ProcessingRunner`, and **lock that behavior with a contract test**.

This is a **governance milestone** — verification + contract expansion, **not** a routing change.

### Why this matters

* M10–M13 established the runner as a **safe execution boundary**
* M13 proved txt2img UI already flows through it and is contract-protected
* API is the next highest-value surface (external contract)
* M14 proves API uses the same boundary and protects it from regression

**Outcome:**
API → runner routing is **provable and protected** by contract test.

---

## 2. Scope Boundaries

### In Scope

* `modules/api/api.py`

  * `text2imgapi`
  * `img2imgapi`
* `modules/runtime/runner.py`
* `modules/processing.py` (only if minimal adapter needed)
* New contract tests

### Out of Scope

* Queue/background execution (M15)
* Runtime extraction (M16+)
* UI refactor (Phase V)
* Extension behavior changes
* Any change to request/response schemas

---

## 3. Invariants (Must Not Change)

From Serena invariant registry:

### API Contract Invariants

* JSON request/response schemas unchanged
* Status codes unchanged
* Error behavior unchanged

### Runtime Invariants

* Output images identical (same seed → same result)
* Metadata / infotext unchanged
* File save paths unchanged

### System Invariants

* Extensions behave identically
* CLI/UI unaffected
* Coverage ≥ 40% maintained

---

## 4. Verification Plan

### Tests (Required)

#### 1. API → Runner Contract Test (NEW)

* Monkeypatch `ProcessingRunner.execute`
* Call `/sdapi/v1/txt2img`
* Assert runner is invoked

#### 2. Existing API Tests

* Must pass unchanged
* Ensures no schema drift

#### 3. Smoke Tests

* Full API roundtrip
* Ensures server boot + endpoint works

---

### CI Signals (Required)

* Linter ✓
* Smoke Tests ✓
* Quality Tests ✓
* Coverage gate ≥ 40% ✓

---

### Evidence

* `M14_run1.md` (PR CI)
* `M14_run2.md` (post-merge CI)
* Contract test proves routing

---

## 5. Implementation Steps (Small, Reversible)

### Step 1 — No Routing Changes

**KEEP existing API code:**

```python
processed = process_images(p)  # ✅ DO NOT CHANGE
```

**DO NOT** replace with `runner.run()`. `process_images` is the orchestration boundary; bypassing it would break override_settings, model reload, script callbacks, and extension behavior.

---

### Step 2 — Add Contract Test

Create:

```
test/quality/test_api_runner_contract.py
```

Test:

* Monkeypatch `os.getenv("CI")` to `"false"` so real execution path runs
* Monkeypatch `ProcessingRunner.run` to track invocation
* Call API method directly (not HTTP) to avoid server startup
* Assert runner is invoked when API executes

---

### Step 3 — Validate Both Paths

Confirm:

* `text2imgapi` → `process_images` → runner ✓
* `img2imgapi` → `process_images` → runner ✓

Both already flow through `process_images`; contract test locks txt2img; img2img uses identical pattern.

---

### Step 4 — Run CI + Verify

* All tests pass
* No diff in outputs
* Coverage unchanged or improved

---

## 6. Risk & Rollback Plan

### Risk Level: LOW

Why:

* `process_images` already delegates to runner (M10)
* This is a **routing normalization**, not new logic

---

### Potential Risks

| Risk                              | Mitigation         |
| --------------------------------- | ------------------ |
| API bypasses runner accidentally  | Contract test      |
| Subtle response formatting change | Existing API tests |
| Extension interaction edge case   | Smoke tests        |

---

### Rollback Plan

* Revert API call site change only
* No data/model changes required
* Single-file rollback (`api/api.py`)

---

## 7. Deliverables

### Code

* No API routing changes
* New contract test only

### Tests

* `test_api_runner_contract.py`

### Docs

* `docs/milestones/M14/M14_plan.md`
* `M14_run1.md`, `M14_run2.md`
* `M14_summary.md`
* `M14_audit.md`

### Ledger

* Add M14 row to `docs/serena.md` with:

  * commit SHA
  * CI run IDs
  * audit score

---

## 8. Acceptance Criteria

### Functional

* API endpoints produce identical outputs
* No schema or contract changes

### Structural

* API continues to call `process_images` (orchestration boundary)
* All generation flows through process_images → runner
* Contract test proves API path invokes runner

### Verification

* Contract test passes
* CI fully green
* Coverage ≥ 40%

---

## 9. Architectural Outcome

After M14:

### Unchanged (Verified)

```
API → process_images → ProcessingRunner → process_images_inner
UI  → process_images → ProcessingRunner → process_images_inner
```

**Result:**

* API → runner flow **provably true** and regression-protected
* Contract test locks API path
* No behavior change; governance milestone only

---

## 10. Next Milestone Preview

### M15 — Background / Queue Runner Preparation

Will build on M14 by:

* Introducing async/queued execution
* Adding cancellation + lifecycle control
* Enabling multi-request orchestration

---

# ✅ Final Instruction for Cursor

Implement M14 exactly as specified:

* Minimal diff
* No behavior change
* Add contract test
* Verify CI
* Produce run, summary, audit, and ledger update
