# M39 — Summary

**Milestone:** Remaining legacy surface narrowing  
**Status:** PR **#95** — Linter + Smoke green on head **`fe2494fb`** (post-merge Quality: record in **`M39_run1.md`** after merge)  
**PR:** https://github.com/m-cahill/serena/pull/95  
**Branch:** `m39-remaining-legacy-surface-narrowing`

---

## What shipped

- **`_eff_opts(p)`** in **`modules/processing_helpers.py`** — returns **`p.opts_snapshot`** when present, else **`shared.opts`**.
- **Migrated** direct **`shared.opts`** reads on supported paths:
  - **`processing_types.py`**: inpainting mask weight, **`use_old_scheduling`**, **`hires_fix_use_firstpass_conds`** (no remaining **`shared.opts`** substring in file body).
  - **`processing_infotext.py`**: conditional mask weight for infotext.
  - **`processing.py`**: **`overlay_inpaint`** branch in **`process_images_inner`** decode/save loop.
  - **`modules/runtime/processing_runtime.py`**: live preview + progress type gate at batch entry.
- **Regression:** **`test/quality/test_m39_eff_opts_snapshot.py`** — file-based contract tests (no heavy imports).
- **Docs:** **`docs/architecture/serena_allowed_legacy_surfaces.md`** §2.2; **`M39_plan.md`**, **`M39_toolcalls.md`**.

---

## Governance notes

- **`StableDiffusionProcessing.sd_model`** compatibility property **unchanged** (explicit non-goal).
- **No** **`ProcessingRunner`** contract change; **no** CI weakening; **no** broad **`opts.`** migration beyond this scoped **`shared.opts`** pass.
- Remaining **`opts.`** reads in **`processing_types`** and elsewhere are **documented** as future milestone-governed work, not M39 scope.

---

## Evidence

- **`docs/milestones/M39/M39_run1.md`** — PR §A Linter / Smoke run IDs.  
- This summary and **`M39_audit.md`**.
