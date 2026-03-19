# M16_plan — Runtime Module Extraction

## 1. Intent / Target

**Primary objective:**

Extract **runtime orchestration logic** from `modules/processing.py` into `modules/runtime/` while preserving identical behavior.

> This is the first Phase IV milestone — establishing the runtime module boundary for the inference pipeline.

---

### Why this matters

From M15:

```text
UI/API → process_images → ProcessingRunner → process_images_inner
```

The runner boundary exists, but orchestration logic still lives in `processing.py`. M16 relocates that logic behind the runtime boundary without changing outputs or call paths.

---

### M16 Goal (precise)

* Extract orchestration logic into `modules/runtime/` (new or existing runtime modules)
* Preserve **default synchronous behavior** and **identical outputs**
* Introduce **no user-visible changes**
* Establish **runtime module structure** for M17–M20 (sampler, decode/save, model provider, mockable boundaries)

---

## 2. Detected Surfaces & Constraints

### Surfaces Touched

| Surface | Location | Risk |
|---------|----------|------|
| **Processing pipeline** | `modules/processing.py` | HIGH — core inference path |
| **Runtime boundary** | `modules/runtime/runner.py` | MEDIUM — execute() delegates |
| **Runner execute path** | `ProcessingRunner._execute()` | MEDIUM — calls process_images_inner |

### Constraints

* **process_images_inner** remains the inner loop until extraction is complete
* **process_images(p)** remains the public entrypoint (unchanged signature)
* **ProcessingRunner** remains the execution boundary
* **Extensions** must remain unaffected
* **Coverage** ≥ 40%

### Existing Runtime Modules

* `modules/runtime/runner.py` — ProcessingRunner, ProcessingRequest
* `modules/runtime/execution_queue.py` — ExecutionQueue (pass-through)

---

## 3. Scope Boundaries

### In Scope

* `modules/processing.py` — orchestration extraction
* `modules/runtime/` — new pipeline module(s)
* `ProcessingRunner._execute()` — delegation target (may change from process_images_inner to runtime module)
* Contract tests for execution path

### Out of Scope

* Sampler extraction (M17)
* Decode/save separation (M18)
* Model provider interface (M19)
* Mockable boundaries / runtime tests (M20)
* API/UI changes
* Extension API changes

---

## 4. Invariants (Must Not Change)

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

### Structural

* `process_images(p)` remains public entrypoint
* ProcessingRunner lifecycle order unchanged (prepare → execute → finalize)

---

## 5. Verification Plan

### Tests (Required)

#### 1. Execution Path Contract Test

* Ensure `ProcessingRunner._execute()` delegates to runtime module (not direct process_images_inner)
* Assert execution completes correctly

---

#### 2. Output Identity Test

* Compare outputs (seed-based) before and after extraction
* Ensure identical results for txt2img and img2img paths

---

#### 3. Existing Contract Preservation

* Re-run:
  * `test_txt2img_path_uses_runner`
  * `test_api_runner_contract`
  * `test_runner_lifecycle_order`
  * `test_queue_mode_*`

Ensure:

> Extraction does NOT break routing or lifecycle guarantees

---

### CI Signals

* Linter ✓
* Smoke ✓
* Quality ✓
* Coverage ≥ 40% ✓

---

## 6. Implementation Steps (Small, Reversible)

### Step 1 — Create Runtime Pipeline Module

Create:

```
modules/runtime/pipeline.py
```

Introduce minimal wrapper:

```python
def run_pipeline(processing):
    """Delegates to process_images_inner. Extraction boundary for M17+."""
    from modules.processing import process_images_inner
    return process_images_inner(processing)
```

* No behavior change
* Establishes extraction boundary

---

### Step 2 — Update Runner to Use Pipeline

In `ProcessingRunner._execute()`:

```python
def _execute(self, state):
    from modules.runtime.pipeline import run_pipeline
    return run_pipeline(state.processing)
```

Replace direct `process_images_inner` call with `run_pipeline`.

* Single delegation point change
* process_images_inner remains in processing.py for now

---

### Step 3 — Move process_images_inner to Runtime (Optional / Incremental)

**Option A (minimal):** Keep process_images_inner in processing.py; pipeline.py imports and delegates. Extraction boundary established; no file move.

**Option B (full):** Move process_images_inner body into pipeline.py; processing.py re-exports or delegates. Larger diff; verify all imports.

Recommend **Option A** for M16 to minimize blast radius. Option B can be M16b or folded into M17.

---

### Step 4 — Preserve Lifecycle and Queue Behavior

Ensure:

```text
prepare → (optional queue) → _execute → run_pipeline → process_images_inner → finalize
```

is unchanged. Queue still wraps `_execute`; pipeline is internal to execute path.

---

### Step 5 — Add Contract Tests

Create or extend:

```
test/quality/test_runtime_pipeline.py
```

Test:

* Runner delegates to run_pipeline
* Execution completes correctly
* Output identity (seed-based comparison if feasible)

---

### Step 6 — Validate No Behavior Drift

* Run full smoke and quality suites
* Compare outputs (seed-based) if test infrastructure supports
* Ensure extensions unaffected

---

### Step 7 — Update Documentation

* M16_plan.md (this document)
* M16_run*.md (run logs)
* M16_summary.md (closeout)
* serena.md ledger entry

---

## 7. Detailed Instructions for Phase Summary Documents

### M16_summary.md Structure

Follow Phase I–III summary format:

1. **Why This Milestone Existed** — Runtime logic in processing.py; need extraction boundary for Phase IV
2. **What Changed** — New pipeline.py; runner delegates to run_pipeline; process_images_inner call path updated
3. **Why It Mattered** — First Phase IV extraction; establishes runtime module boundary
4. **Seam Added** — `run_pipeline(processing)` as extraction boundary
5. **Invariant Added** — Execution flows through runtime pipeline module
6. **Key Files** — pipeline.py (new), runner.py (updated)
7. **Deferred to M17+** — Sampler extraction, decode/save, model provider, mockable boundaries

### phaseIV-summary.md (When Phase IV Completes)

Phase IV summary will aggregate M16–M20:

* M16: Runtime module extraction
* M17: Sampler runner extraction
* M18: Decode/save separation
* M19: Model provider interface
* M20: Runtime tests with mockable boundaries

Structure consistent with phaseI-summary.md, phaseII-summary.md, phaseIII-summary.md.

---

## 8. Risk & Rollback Plan

### Risk Level: MEDIUM

Why:

* Touching core execution path (processing.py → runtime)
* Import structure may affect extensions

---

### Risks

| Risk | Mitigation |
|------|------------|
| Import cycles | Keep pipeline.py thin; import process_images_inner inside function if needed |
| Extension breakage | Extensions use process_images; no direct process_images_inner calls expected |
| Behavior drift | Contract tests; output identity checks |
| Coverage drop | Add tests for new pipeline module |

---

### Rollback

* Revert runner to call process_images_inner directly
* Remove pipeline.py
* No API/UI impact
* Single-module rollback

---

## 9. Deliverables

### Code

* `modules/runtime/pipeline.py` (new)
* Updated `modules/runtime/runner.py`

### Tests

* `test/quality/test_runtime_pipeline.py` (or equivalent)

### Docs

* `M16_plan.md` (this document)
* `M16_run1.md`, `M16_run2.md` (as needed)
* `M16_summary.md`
* `M16_audit.md` (if applicable)
* serena.md ledger entry

---

## 10. Acceptance Criteria

### Functional

* Default execution unchanged
* Outputs identical (seed-based)
* All existing contract tests pass

### Structural

* `run_pipeline(processing)` exists in modules/runtime/
* ProcessingRunner._execute() delegates to run_pipeline
* process_images remains public entrypoint

### Verification

* All CI green (linter, smoke, quality)
* Coverage maintained ≥ 40%
* Contract tests still pass

---

## 11. Architectural Outcome

### Before M16

```text
ProcessingRunner._execute(state)
    └── process_images_inner(state.processing)
```

### After M16

```text
ProcessingRunner._execute(state)
    └── run_pipeline(state.processing)
            └── process_images_inner(processing)
```

**Key change:** Execution path flows through `modules/runtime/pipeline.py`. Extraction boundary established for M17+ (sampler, decode/save, model provider).

---

## 12. Strategic Impact

M16 enables:

### Immediate

* Runtime module boundary for inference pipeline
* Clear extraction point for M17–M20

### Next (M17+)

* Sampler runner extraction
* Decode/save separation
* Model provider interface
* Runtime tests with mockable boundaries

---

# 🧠 Key Guidance for Cursor

* This is **NOT a full pipeline refactor**
* This is **extraction boundary establishment**
* Behavior must remain identical
* Prefer Option A (thin pipeline wrapper) over Option B (full move) to minimize risk

---

# ✅ Final Instruction

Proceed with M16:

* Minimal diff
* No behavior change
* Add pipeline module only
* Runner delegates through pipeline
* Prove via contract tests and CI
