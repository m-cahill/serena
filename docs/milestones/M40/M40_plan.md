# M40 — Coverage wave on legacy/high-value modules

**Status:** **Complete** (2026-03-30 UTC)  
**Primary PR:** [#96](https://github.com/m-cahill/serena/pull/96) (recovery PRs [#97](https://github.com/m-cahill/serena/pull/97)–[#100](https://github.com/m-cahill/serena/pull/100) — see `M40_run1.md`)

## Intent

Phase IX internal score-lift: **test-first** coverage on recently stabilized surfaces (M38 splits, M39 `_eff_opts` / snapshot behavior), without structural refactors or threshold chasing.

## Scope (delivered)

**In**

- `test/quality/test_m40_*.py` for `processing_helpers`, `processing_infotext`, `processing_types`, `processing_runtime`.
- Milestone documentation and ledger updates.
- **Gate:** left at **42%** (binding `main` **49%** TOTAL — see `M40_run1.md` §F).

**Out**

- Broad `processing.py` rewrites, M41 performance SLO enforcement, CI weakening.

## Verification

- PRs: Linter + Smoke green.
- Post-merge `main`: Linter + Quality green — **Quality `23722341901`**, **243** pass, **49%** TOTAL.
