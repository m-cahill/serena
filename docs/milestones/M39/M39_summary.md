# M39 — Summary

**Milestone:** Remaining legacy surface narrowing  
**Status:** **Complete** (2026-03-29 UTC)  
**PR:** [#95](https://github.com/m-cahill/serena/pull/95)  
**Merge commit (`main`):** `d4551e6d55c31c5f6b1efd0a5d04956a19d0ea53`  
**Merged at:** 2026-03-29T21:45:43Z  
**Binding post-merge Quality (`main`):** commit **`1b9f304e`** — Quality **`23719932254`** — **222** pass, **48%** TOTAL — see **`M39_run1.md`** §C.

---

## What shipped

- **`_eff_opts(p)`** and **`_EffOptsView`** in **`modules/processing_helpers.py`**: prefer per-run **`p.opts_snapshot`** for attributes present on the snapshot; **missing** keys delegate to **`shared.opts`** (full production snapshots unchanged; sparse test doubles safe).
- **Removed** direct **`shared.opts`** reads on supported paths from **`processing_types.py`**, **`processing_infotext.py`**, **`processing.py`** (overlay inpaint branch), **`modules/runtime/processing_runtime.py`** (preview gate).
- **`create_opts_snapshot(shared.opts)`** remains the **intentional** global capture in **`process_images_inner`**.
- **`StableDiffusionProcessing.sd_model`** compatibility property **unchanged**.
- **`test/quality/test_m39_eff_opts_snapshot.py`** contract tests; **`docs/architecture/serena_allowed_legacy_surfaces.md`** §2.2.
- **Post-merge fix** on **`main`** (**`1b9f304e`**): restores Quality after merge commit **`d4551e6d`** exposed sparse-snapshot **`AttributeError`** — **not** a CI policy change.

---

## Governance

- **No** broad globals purge; **no** **`ProcessingRunner`** contract change; **no** extension-facing deprecation; **no** CI gate weakening (**42%**, **`pip-audit`**, workflows unchanged).
- Migration stayed on **owned seams** (**opts snapshot**, helpers).

---

## Evidence

- **`docs/milestones/M39/M39_run1.md`** — merge, PR approval tip, merge-first Quality failure, binding follow-up **`main`** CI.  
- **`M39_audit.md`**.
