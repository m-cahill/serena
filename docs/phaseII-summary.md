# Phase II Summary — Runtime Seam Preparation

**Phase:** Phase II — Runtime Seam Preparation  
**Milestone Range:** M05–M09  
**Timeframe:** 2026-03-10 → 2026-03-12  
**Overall Outcome:** Five runtime seams introduced in preparation for an execution boundary; global state reads isolated; generation-time opts snapshot threaded; execution context established

---

## 1. Why This Phase Existed

Phase II addressed the **runtime isolation problem**:

* Global state (`shared.opts`, `shared.sd_model`, `shared.device`, `shared.state`) accessed directly during generation
* Override settings mutated global `shared.opts` directly
* No generation-time snapshot of `opts.data`
* No grouped runtime dependencies
* No extraction foothold for future ProcessingRunner (Phase III)

**Architectural pressure relieved:** Created safe seams for runtime state isolation, enabling Phase III execution boundary and Phase IV runtime extraction without behavior drift.

---

## 2. Milestone-by-Milestone Progression

### M05 — Override Isolation / Temporary Opts Seam

**What changed:**
* Introduced `temporary_opts()` context manager in `modules/runtime_utils.py`
* Isolated `override_settings` mutation from global runtime in `process_images`
* Preserved existing behavior: `opts.set(is_api=True, run_callbacks=False)`, setattr restore, `k in opts.data` check
* Model/VAE reload and token merging remain in `process_images` (unchanged)

**Why it mattered:**
* First Phase II runtime seam
* Decoupled override mutation from global `shared.opts`
* Created foundation for M07 opts snapshot injection

**Seam added:**
* `temporary_opts()` context manager isolates override mutation

---

### M06 — Prompt / Seed Prep Extraction

**What changed:**
* Extracted `prepare_prompt_seed_state(p)` into `modules/prompt_seed_prep.py`
* Replaced inline `all_seeds`/`all_subseeds` logic in `process_images_inner`
* Left `setup_prompts()` on `StableDiffusionProcessing` (unchanged)
* Left `fill_fields_from_opts()` in `process_images_inner` (unchanged)
* Mutates `p.seed`/`p.subseed` before call; writes `p.all_seeds`, `p.all_subseeds`

**Why it mattered:**
* Second Phase II runtime seam
* Isolated prompt and seed preparation behind function boundary
* Enabled M07 opts snapshot and M09 execution context

**Seam added:**
* `prepare_prompt_seed_state(p)` extracts prompt/seed preparation

---

### M07 — Opts Snapshot Introduction

**What changed:**
* Created `modules/opts_snapshot.py` with `create_opts_snapshot(opts)`
* Snapshot captured in `process_images_inner` after `prepare_prompt_seed_state`
* Full shallow copy of `opts.data` via `SimpleNamespace`
* Snapshot attached to `p.opts_snapshot`
* Write-only in M07 (no runtime reads replaced yet)

**Why it mattered:**
* Third Phase II runtime seam
* Created generation-time snapshot of `opts.data`
* Enabled M08 snapshot threading and future runtime isolation

**Seam added:**
* `create_opts_snapshot(opts)` captures generation-time snapshot of `opts.data`
* `p.opts_snapshot` available on processing object

---

### M08 — Opts Snapshot Threading

**What changed:**
* Threaded `p.opts_snapshot` into `process_images_inner` for save-related reads
* Migrated 12 opts from `shared.opts` to `p.opts_snapshot`:
  * `save_images_before_face_restoration`
  * `save_images_before_color_correction`
  * `samples_format`, `return_mask`, `save_mask`
  * `return_mask_composite`, `save_mask_composite`
  * `grid_only_if_multiple`, `return_grid`, `grid_save`
  * `grid_format`, `grid_extended_filename`
* `save_samples()`, `sample_hr_pass()`, metadata unchanged (still read `shared.opts`)

**Why it mattered:**
* Fourth Phase II runtime seam
* First runtime boundary where generation pipeline reads save-related config from snapshot, not global state
* Proved snapshot can safely replace `shared.opts` reads

**Seam added:**
* Save-related opts reads migrated to `p.opts_snapshot`
* Deterministic read boundary established

---

### M09 — Execution Context Introduction

**What changed:**
* Created `modules/runtime_context.py` with `RuntimeContext` dataclass
* `RuntimeContext` groups: `model`, `opts_snapshot`, `device`, `state`, `cmd_opts`
* Attached `p.runtime_context` in `process_images_inner` after opts snapshot creation
* Write-only in M09 (no migration of `shared.*` reads yet)

**Why it mattered:**
* Fifth Phase II runtime seam
* Grouped runtime dependencies into single object
* Completed Phase II — Runtime Seam Preparation
* Enabled Phase III ProcessingRunner and future shared state reduction

**Seam added:**
* `RuntimeContext` dataclass groups runtime dependencies
* `p.runtime_context` available on processing object

---

## 3. Net Architectural Effect

**Before Phase II:**
* Override settings mutate global `shared.opts` directly
* No generation-time snapshot of `opts.data`
* Prompt/seed preparation logic inline in `process_images_inner`
* Runtime dependencies scattered (model, device, state, opts, cmd_opts)
* No extraction foothold for ProcessingRunner

**After Phase II:**
* Override settings isolated via `temporary_opts()` context manager
* Deterministic opts snapshot captured and threaded for save-related reads
* Prompt/seed preparation extracted behind `prepare_prompt_seed_state(p)`
* Runtime dependencies grouped in `RuntimeContext`
* Five runtime seams established as extraction footholds

---

## 4. Guardrails / Invariants Established

| Invariant | Enforcement |
|-----------|-------------|
| Override isolation | `temporary_opts()` wraps override mutation |
| Prompt/seed prep boundary | `prepare_prompt_seed_state(p)` before snapshot |
| Deterministic snapshot | `p.opts_snapshot` captured after prompt/seed prep |
| Snapshot threading | Save-related opts read from `p.opts_snapshot` |
| Runtime context grouping | `p.runtime_context` holds model, opts_snapshot, device, state, cmd_opts |
| Behavior preservation | All runtime seams are mechanical refactors; no logic change |

---

## 5. Key Files / Modules Introduced or Changed

**Introduced:**
* `modules/runtime_utils.py` — `temporary_opts()` context manager
* `modules/prompt_seed_prep.py` — `prepare_prompt_seed_state(p)`
* `modules/opts_snapshot.py` — `create_opts_snapshot(opts)`
* `modules/runtime_context.py` — `RuntimeContext` dataclass
* `test/quality/test_opts_override.py` — Override isolation tests

**Changed:**
* `modules/processing.py` — process_images (temporary_opts), process_images_inner (snapshot, runtime_context, snapshot reads)

---

## 6. Deferred Work Handed to Phase III

* ProcessingRunner introduction
* Lifecycle surface (prepare → execute → finalize)
* Instrumentation hooks
* txt2img/API routing through runner
* Queue insertion seam

---

## 7. Agent Context / How to Think About the Repo Now

### Where the safe seams are

* **`temporary_opts()`** — Override isolation; use this pattern for future opts mutation
* **`prepare_prompt_seed_state(p)`** — Prompt/seed preparation extraction; called before snapshot
* **`create_opts_snapshot(opts)`** — Deterministic snapshot creation; attached to `p.opts_snapshot`
* **`p.opts_snapshot`** — Safe read boundary for save-related opts (12 opts migrated in M08)
* **`p.runtime_context`** — Runtime dependency grouping (model, opts_snapshot, device, state, cmd_opts)

### What not to disturb

* Override mutation must use `temporary_opts()` (do not mutate `shared.opts` directly)
* Prompt/seed prep must occur before snapshot creation
* Snapshot must be created in `process_images_inner` after prompt/seed prep
* Runtime context must be created after snapshot

### Which patterns are now established

* **Mechanical refactors only:** All Phase II changes preserve existing behavior; no logic change
* **Write-then-read pattern:** M07 introduced snapshot (write-only); M08 threaded reads; M09 introduced context (write-only)
* **Incremental migration:** Opts reads migrated incrementally (12 in M08; more deferred to Phase IV)
* **Seam stacking:** Each milestone builds on prior seams (M06 enables M07; M07 enables M08; M08 + M07 enable M09)

### What Phase III is expected to build on

Phase III will introduce the **execution boundary** (ProcessingRunner):
* Lifecycle surface (prepare → execute → finalize)
* Instrumentation hooks (on_prepare, on_execute, on_finalize)
* txt2img/API routing verification
* Queue insertion seam

Phase II created the **runtime seams** (temporary opts, prompt/seed prep, opts snapshot, runtime context). Phase III will create the **execution boundary** that wraps these seams for lifecycle control, instrumentation, and queue insertion. Phase IV will extract runtime logic behind this boundary.

### Safe assumptions for future agents

* `process_images_inner` is the inner loop; `process_images` is the public entrypoint
* `p.opts_snapshot` contains generation-time snapshot of `opts.data`
* `p.runtime_context` groups runtime dependencies (model, opts_snapshot, device, state, cmd_opts)
* Save-related opts should be read from `p.opts_snapshot`, not `shared.opts`
* Override settings use `temporary_opts()` context manager
* Prompt/seed preparation uses `prepare_prompt_seed_state(p)`

---

## 8. Phase-end Truth State

Facts a future agent may assume after Phase II:

* `temporary_opts()` isolates override mutation from global `shared.opts`
* `prepare_prompt_seed_state(p)` extracts prompt/seed prep before snapshot
* `p.opts_snapshot` holds generation-time snapshot of `opts.data`
* `p.runtime_context` groups runtime dependencies (model, opts_snapshot, device, state, cmd_opts)
* Save-related opts (12 migrated in M08) read from `p.opts_snapshot`, not `shared.opts`
