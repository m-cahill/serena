# M34 — Summary

**Milestone:** Runtime context model-identity seam  
**Status:** **Complete** (2026-03-27 UTC)  
**PR:** [#90](https://github.com/m-cahill/serena/pull/90)  
**Merge commit:** `b94c93d38e521437a18bb1660d35b31c90220be0` (merge commit; not squash)

---

## What shipped

- **Explicit runtime-owned model identity:** `ModelIdentity` and `model_identity_from_model()` in `modules/runtime_context.py`; `RuntimeContext` now carries **`model_identity`** alongside existing fields.
- **`process_images_inner`** populates **`p.runtime_context`** with that identity (from the same source as existing `p.sd_model_name` / `p.sd_model_hash` assignments) **before** the first `scripts.process` call — additive-first, no user-visible behavior change intended.
- **Tests** in `test/quality/test_runtime_mock.py` cover identity fields and ordering relative to script hooks (with a **test-only** `MagicMock` scripts object for the hook-ordering test after merge-closeout fixes on `main`).

## Governance notes

- **Additive-first:** New types and fields; no broad refactor of global state.
- **Tolerated coupling unchanged:** M34 **did not** remove the remaining **`processing.py` ↔ `shared.sd_model`** orchestration coupling called out in the architecture/audit stream; that work is **deferred to M35** (narrow scope: orchestration seam, not a global-state cleanup sweep).
- **CI:** PR **Linter** + **Smoke** green on authoritative head **`8e209ed2`**; post-merge **Quality** binding green on **`main`** commit **`1bc04394`** (run **`23671154433`**, **202** passed, **48%** coverage as reported). Policy and gates unchanged.

## Evidence

- **`docs/milestones/M34/M34_run1.md`** — PR CI, merge metadata, post-merge Linter/Quality IDs, merge-first Quality failure + binding green tip.
