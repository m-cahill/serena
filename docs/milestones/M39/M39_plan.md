# M39 — Remaining legacy surface narrowing

**Status:** PR **#95** — Linter + Smoke green on merge-ready **`c83e14cd`**; post-merge **`main`** Quality in **`M39_run1.md`** §B  
**Branch:** `m39-remaining-legacy-surface-narrowing`

## Objective

Narrow documented allowed-legacy **`shared.opts`** usage on **Serena-managed execution paths** by preferring **`p.opts_snapshot`** where **`process_images_inner`** already establishes it, without changing behavior, weakening CI, or removing **`StableDiffusionProcessing.sd_model`**.

## Inventory (pre-change)

| Location | Read | Classification |
|----------|------|----------------|
| `processing_types.py` | `shared.opts` (inpainting mask, `use_old_scheduling`, `hires_fix_use_firstpass_conds`) | **Safe to migrate** after snapshot |
| `processing_infotext.py` | `shared.opts.inpainting_mask_weight` | **Safe to migrate** after snapshot |
| `processing.py` | `shared.opts.overlay_inpaint` in inner loop | **Safe to migrate** after snapshot |
| `processing_runtime.py` | `shared.opts.live_previews_enable` + `opts.show_progress_type` | **Safe to migrate** (batch loop runs after snapshot) |
| `processing.py` | `create_opts_snapshot(shared.opts)` | **Intentional capture** — keep |
| `StableDiffusionProcessing.sd_model` | compatibility property | **Compatibility-only** — **not** removed in M39 |

**Out of scope for M39:** Broad migration of **`opts.`** (module alias) reads across **`processing_types`**; upstream-heavy modules (`sd_models.py`, `images.py`, …); **`shared.sd_model`** beyond existing **`_orchestration_model`** + property.

## Implementation

- Introduced **`_eff_opts(p)`** in **`modules/processing_helpers.py`**: return **`p.opts_snapshot`** if set, else **`shared.opts`**.
- Replaced direct **`shared.opts`** reads listed above with **`_eff_opts(self)`** / **`_eff_opts(p)`** as appropriate.
- **`processing_runtime`**: single **`eff = _eff_opts(p)`** for preview gate (no direct **`shared.opts`** in that condition).

## Verification

- **Regression:** `test/quality/test_m39_eff_opts_snapshot.py` — contract tests on source shape (no **`shared.opts`** in migrated **`processing_types`** body except via docstrings in helpers; overlay / infotext / runtime patterns assert **`_eff_opts`** usage).
- **CI:** PR Linter + Smoke; post-merge **`main`** Linter + Quality (unchanged gates: **42%**, blocking **`pip-audit`**, etc.).

## Definition of done

- Allowed-legacy doc updated; ledger updated at closeout.
- No intended behavior drift; extension **`sd_model`** property retained.
