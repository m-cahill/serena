# Phase III Summary — Runner & Service Boundary

**Phase:** Phase III — Runner & Service Boundary  
**Milestone Range:** M10–M15  
**Timeframe:** 2026-03-12 → 2026-03-18  
**Overall Outcome:** ProcessingRunner execution boundary established; lifecycle surface introduced; instrumentation hooks added; txt2img/API routing verified; queue insertion seam created

---

## 1. Why This Phase Existed

Phase III addressed the **execution boundary problem**:

* No abstraction layer between callers (UI/API/scripts) and processing pipeline
* No lifecycle structure for instrumentation, progress tracking, or cancellation
* No seam for queue insertion, background execution, or distributed processing
* txt2img/API paths call `process_images_inner` via `process_images`, but no explicit contract enforcement
* No execution surface for future runtime extraction (Phase IV)

**Architectural pressure relieved:** Created unified execution boundary (ProcessingRunner) with lifecycle surface, instrumentation hooks, and queue seam, enabling Phase IV runtime extraction and future service-mode or queued execution patterns.

---

## 2. Milestone-by-Milestone Progression

### M10 — ProcessingRunner Skeleton

**What changed:**
* Introduced `ProcessingRunner` in `modules/runtime/runner.py`
* Introduced `ProcessingRequest` wrapper around `StableDiffusionProcessing`
* Modified `process_images` to delegate through runner: `ProcessingRunner().run(ProcessingRequest(p))`
* Runner delegates to `process_images_inner(request.processing)`
* Import inside `process_images` function to avoid circular import
* Added contract test `test_processing_runner_delegates`
* Updated Phase III roadmap in `docs/serena.md` (M11 lifecycle, M12 instrumentation, M13 txt2img, M14 API, M15 queue)

**Why it mattered:**
* First Phase III execution boundary
* Created single abstraction layer between callers and pipeline
* Zero blast radius: all callers unchanged; ProcessingRunner is thin adapter

**Seam added:**
* `ProcessingRunner` is unified execution entrypoint
* Call graph: UI/API/scripts → `process_images` → `ProcessingRunner.run()` → `process_images_inner`

---

### M11 — Runner Lifecycle Surface

**What changed:**
* Refactored `ProcessingRunner.run()` to delegate through lifecycle stages:
  * `state = prepare(request)`
  * `result = execute(state)`
  * `return finalize(state, result)`
* `prepare(request)` — Returns request (pass-through in M11)
* `execute(state)` — Calls `process_images_inner(state.processing)`
* `finalize(state, result)` — Returns result (pass-through in M11)
* Added contract test `test_runner_lifecycle_order` (subclass verifies ordering)

**Why it mattered:**
* Lifecycle structure created for future instrumentation
* prepare → execute → finalize order explicit and contract-tested
* Enabled M12 instrumentation hooks, progress tracking, cancellation

**Seam added:**
* Lifecycle stages: `prepare()` → `execute()` → `finalize()`
* Lifecycle order verified by contract test

---

### M12 — Runtime Instrumentation Hooks

**What changed:**
* Added optional instrumentation hooks to `ProcessingRunner`:
  * `on_prepare(state)` — Called after prepare
  * `on_execute(state, result)` — Called after execute
  * `on_finalize(state, result)` — Called after finalize
* Hooks are no-op by default
* Updated `run()` to invoke hooks: `prepare → on_prepare → execute → on_execute → finalize → on_finalize`
* Added contract test `test_runner_hooks_called` (subclass verifies hook invocation)

**Why it mattered:**
* Instrumentation seam established for progress, tracing, cancellation
* Future milestones can plug into hooks without modifying pipeline

**Seam added:**
* Instrumentation hooks: `on_prepare()`, `on_execute()`, `on_finalize()`
* Hook invocation order verified by contract test

---

### M13 — txt2img Path Through Runner

**What changed:**
* Verified `modules/txt2img.py` calls `process_images(p)` only (lines 83, 109)
* No direct `process_images_inner` calls in txt2img path
* `process_images` delegates to `ProcessingRunner().run(ProcessingRequest(p))` (M10)
* Added contract test `test_txt2img_path_uses_runner` (monkeypatches runner, calls `process_images`, asserts runner invoked)

**Why it mattered:**
* txt2img → runner flow **provably true** and regression-protected
* No routing changes required (already flows through `process_images` → runner)

**Invariant added:**
* txt2img UI path flows through `ProcessingRunner` (contract-tested)

---

### M14 — API Integration

**What changed:**
* Verified API (`modules/api/api.py`) calls `process_images(p)` only (text2imgapi, img2imgapi)
* No direct `process_images_inner` calls in API path
* Added contract test `test_api_txt2img_uses_runner` (monkeypatches CI env + runner, calls API method, asserts runner invoked)
* Updated `CODEOWNERS` for fork (unblocks code owner review)

**Why it mattered:**
* API → runner flow **provably true** and regression-protected
* Together with M13, **all execution entrypoints** now flow through runner

**Invariant added:**
* API path flows through `ProcessingRunner` (contract-tested)

---

### M15 — Queue / Background Runner Preparation

**What changed:**
* Introduced `ExecutionQueue` in `modules/runtime/execution_queue.py` (pass-through)
* `ExecutionQueue.submit(state, fn)` delegates to `fn(state)` (no real queue implementation)
* Modified `ProcessingRunner` constructor: `__init__(queue=None, use_queue=False)`
* Queue wraps `execute` only when `use_queue=True`
* Extracted `_execute(state)` hook for future async/retries/cancellation
* Updated `run()`: if `use_queue`, call `queue.submit(state, self._execute)`, else call `_execute(state)` directly
* Default behavior unchanged (`use_queue=False`)
* Added contract tests: `test_queue_mode_uses_queue`, `test_queue_mode_preserves_lifecycle_order`, `test_default_mode_unchanged`

**Why it mattered:**
* Queue insertion seam created without affecting callers
* Lifecycle order preserved when queue enabled
* Execution logic extracted behind `_execute` hook for future orchestration
* Completed Phase III — Runner & Service Boundary

**Seam added:**
* Optional queue insertion at runner layer (`use_queue` flag)
* `_execute(state)` hook for future orchestration (async, retries, cancellation)

---

## 3. Net Architectural Effect

**Before Phase III:**
* No abstraction layer between callers and pipeline
* `process_images` directly calls `process_images_inner`
* No lifecycle structure
* No instrumentation seam
* No queue seam
* txt2img/API routing implicit (no contract tests)

**After Phase III:**
* `ProcessingRunner` is unified execution boundary
* Call graph: UI/API/scripts → `process_images` → `ProcessingRunner.run()` → `process_images_inner`
* Lifecycle structure: `prepare → execute → finalize`
* Instrumentation hooks: `on_prepare`, `on_execute`, `on_finalize`
* Queue seam: optional queue wraps `execute` only; default synchronous
* txt2img/API routing contract-tested
* Phase III complete; codebase ready for Phase IV runtime extraction

---

## 4. Guardrails / Invariants Established

| Invariant | Enforcement |
|-----------|-------------|
| Unified execution boundary | `ProcessingRunner` is the unified execution boundary for current entrypoints |
| Public entrypoint stable | `process_images(p)` remains public API |
| Lifecycle order | `prepare → execute → finalize` (contract-tested) |
| Instrumentation hooks | `on_prepare`, `on_execute`, `on_finalize` (contract-tested) |
| txt2img routing | txt2img → `process_images` → runner (contract-tested) |
| API routing | API → `process_images` → runner (contract-tested) |
| Queue insertion optional | `use_queue=False` by default; no behavior change |
| Lifecycle preserved when queued | prepare → execute (via queue) → finalize order unchanged |

---

## 5. Key Files / Modules Introduced or Changed

**Introduced:**
* `modules/runtime/runner.py` — `ProcessingRunner`, `ProcessingRequest`
* `modules/runtime/execution_queue.py` — `ExecutionQueue` (pass-through)
* `test/quality/test_processing_runner.py` — Runner contract tests (delegation, lifecycle, hooks, queue)
* `test/quality/test_txt2img_runner_contract.py` — txt2img routing contract
* `test/quality/test_api_runner_contract.py` — API routing contract

**Changed:**
* `modules/processing.py` — `process_images` delegates through runner (M10)
* `CODEOWNERS` — Updated for fork (@m-cahill)

---

## 6. Deferred Work Handed to Phase IV

* Runtime module extraction (orchestration logic out of `processing.py`)
* Sampler runner extraction
* Decode/save separation
* Model provider interface
* Runtime tests with mockable boundaries

---

## 7. Agent Context / How to Think About the Repo Now

### Where the safe seams are

* **`ProcessingRunner`** — Unified execution boundary; only entry point to pipeline
* **Lifecycle surface** — `prepare()` → `execute()` → `finalize()` order is stable
* **Instrumentation hooks** — `on_prepare()`, `on_execute()`, `on_finalize()` are safe insertion points
* **Queue seam** — `use_queue` flag enables queue insertion without caller changes
* **`_execute(state)` hook** — Internal execution hook for future async/retries/cancellation

### What not to disturb

* `process_images(p)` is the public entrypoint (do not change signature or remove)
* Lifecycle order must remain `prepare → execute → finalize`
* Instrumentation hook order must remain `prepare → on_prepare → execute → on_execute → finalize → on_finalize`
* Queue seam must remain optional and disabled by default (`use_queue=False`)
* txt2img/API routing must flow through `process_images` → runner (contract-tested)

### Which patterns are now established

* **Execution boundary abstraction:** All execution flows through `ProcessingRunner.run()`
* **Lifecycle structure:** Explicit stages with pass-through default behavior
* **Hook-based instrumentation:** Hooks are no-op by default; subclasses or future extensions can override
* **Optional queue insertion:** Queue wraps `execute` only; constructor injection; default synchronous
* **Contract testing:** txt2img and API routing protected by automated tests

### What Phase IV is expected to build on

Phase IV will begin **runtime extraction**:
* Extract execution-phase orchestration from `process_images_inner` into `modules/runtime/`
* Move runtime logic behind runner boundary without altering behavior
* Sampler runner extraction (M17)
* Decode/save separation (M18)
* Model provider interface (M19)
* Runtime tests with mockable boundaries (M20)

Phase III created the **execution boundary** (ProcessingRunner with lifecycle, hooks, queue seam). Phase IV will extract runtime orchestration logic behind this boundary, using the seams established in Phases II–III.

### Safe assumptions for future agents

* `ProcessingRunner` is the unified execution boundary for current entrypoints (do not bypass)
* All callers (UI, API, scripts) flow through `process_images` → runner
* Lifecycle order is stable and contract-tested
* Instrumentation hooks are safe insertion points (no behavior change by default)
* Queue seam exists but is disabled by default (`use_queue=False`)
* Runtime logic still lives primarily in `modules/processing.py` (extraction deferred to Phase IV)
* `process_images_inner` is the inner loop; `ProcessingRunner.execute()` delegates to it
* Runner boundary is thin adapter in Phase III; Phase IV will move orchestration behind it

### Execution boundary is now established

**What is now true:** Runtime logic remains largely inside `processing.py`. The execution boundary (ProcessingRunner) wraps it with lifecycle, hooks, and queue seam, but does not yet relocate orchestration logic.

**Phase IV expectation:** Extract runtime orchestration logic behind the runner boundary without altering user-visible behavior. The runner surface remains stable; internal orchestration moves to `modules/runtime/`.

---

## 8. Phase-end Truth State

Facts a future agent may assume after Phase III:

* `process_images` remains the public entrypoint
* `ProcessingRunner` wraps execution with lifecycle stages (prepare → execute → finalize)
* txt2img and API paths are contract-tested through runner
* Queue insertion exists but is off by default (`use_queue=False`)
* Orchestration still largely lives in `modules/processing.py`
