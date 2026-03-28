# M35 — Summary

**Milestone:** Remove tolerated `shared.sd_model` orchestration coupling in `processing.py`  
**Status:** **Complete** (2026-03-28 UTC)  
**PR:** [#91](https://github.com/m-cahill/serena/pull/91)  
**Merge commit:** `45e6f4fbfb8f6ed2dfc336423d1f414f66c77549` (merge commit; not squash)

---

## What shipped

- **`_orchestration_model(p)`** in **`modules/processing.py`**: supported-path orchestration uses **`p.model_provider.get_model(p)`** when **`ProcessingRunner.prepare`** has set **`model_provider`**; otherwise **`shared.sd_model`** (fallback for non-runner / no-provider paths).
- **Removed** load-bearing **direct** **`shared.sd_model`** reads on the supported path (process entry, cond cache, HR lowvram branch, img2img init, **`edit_image_conditioning`**, etc.).
- **`StableDiffusionProcessing.sd_model`** remains a **compatibility** **`return shared.sd_model`** (documented); **not** the internal orchestration authority.
- **Tests:** **`test_orchestration_identity_ignores_mismatched_shared_sd_model`** in **`test/quality/test_runtime_mock.py`**; **`docs/architecture/serena_allowed_legacy_surfaces.md`** updated for the narrowed seam; **`modules/runtime/model_provider.py`** docstring cross-reference.

---

## Governance notes

- **Narrow scope:** orchestration / model-access seam only — **no** broad **`shared.opts`** / **`shared.state`** cleanup, **no** runtime module redesign, **no** CI weakening.
- **Runtime modules** unchanged: still **`ModelProvider`**-only for model access (**M19** boundary).
- **CI:** PR approval on head **`564ebd27`** — Linter **`23673315409`**, Smoke **`23673315420`**; post-merge **`main`** Linter **`23673838902`**, Quality **`23673838908`** (**203** pass, **48%** coverage as reported). Policy unchanged.

---

## Evidence

- **`docs/milestones/M35/M35_run1.md`** — merge metadata, PR approval tip, pre-merge snapshot note, post-merge Linter/Quality.
- **`docs/milestones/M35/M35_audit.md`**, this summary.
