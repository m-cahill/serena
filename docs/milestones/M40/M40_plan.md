# M40 — Coverage wave on legacy/high-value modules

**Status:** In progress  
**Branch:** `m40-coverage-wave-legacy-modules`

## Intent

Phase IX internal score-lift: **test-first** coverage on recently stabilized surfaces (M38 splits, M39 `_eff_opts` / snapshot behavior), without structural refactors or threshold chasing.

## Scope

**In**

- Add `test/quality` regression and contract tests for agreed targets (`processing_helpers`, `processing_infotext`, `processing_types`, `processing_runtime`).
- Record before/after evidence in `M40_run1.md` and closeout artifacts.
- Optional **small** gate increase (e.g. 42% → 44%) only if post-merge Quality shows a **stable, earned** improvement with buffer; default is **no gate change**.

**Out**

- Broad `processing.py` rewrites, new architecture seams (except tiny test-driven seams documented in milestone docs).
- M41 performance SLO work, M42 conditional security deferrals, packaging/workflow redesign.

## Verification

- PR: Linter + Smoke green.
- Post-merge `main`: Linter + Quality green; binding run ID and coverage % recorded in `docs/serena.md` and this milestone folder.

## Closeout checklist (when done)

- [ ] `M40_summary.md`, `M40_audit.md` per prompts
- [ ] `docs/serena.md` ledger row + UTC completion time
- [ ] Seed `docs/milestones/M41/M41_plan.md`, `M41_toolcalls.md`
