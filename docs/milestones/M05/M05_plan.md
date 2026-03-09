# M05 Plan — Override Isolation / Temporary Opts Seam

**Milestone:** M05  
**Title:** Override isolation / temporary opts seam  
**Branch:** `m05-override-isolation`  
**Status:** Planned  
**Depends on:** M04 (complete)

---

## 1. Intent / Target

Introduce the first architectural seam for Phase II: isolate override_settings application and restore from `process_images` into a reusable context manager or helper. This prepares for opts snapshot threading (M07–M08) and reduces direct mutation of global `shared.opts` during a run.

No runtime behavior changes. Override application and restore logic must remain identical.

---

## 2. Scope Boundaries

### In scope

- Extract override apply/restore block in `process_images` into a context manager or helper
- Introduce `temporary_opts(override_settings)` or equivalent seam
- Preserve exact semantics: apply overrides before inner processing, restore in `finally`
- Add unit test for the seam (mock opts, verify apply/restore)

### Explicitly out of scope

- Opts snapshot (immutable view) — M07
- Passing opts into `process_images_inner` — M08
- Changing override_settings semantics
- API or UI changes

---

## 3. Current Behavior (Evidence)

From `processing.py:823-857`:

- Override settings are applied to `shared.opts` via `opts.set(key, value)` before `process_images_inner`
- In `finally`, if `override_settings_restore_afterwards`, opts are restored
- This block is the target for extraction

---

## 4. Implementation Approach

1. Create helper or context manager (e.g. `modules/opts_override.py` or in `processing.py`)
2. Replace inline override block in `process_images` with call to the helper
3. Add minimal unit test that verifies apply/restore behavior
4. Ensure no behavior change; smoke and quality tests pass

---

## 5. Definition of Done

- [ ] Override apply/restore extracted to reusable seam
- [ ] `process_images` uses the seam; logic unchanged
- [ ] Unit test for seam
- [ ] Smoke and Quality CI green
- [ ] Milestone docs and ledger update
