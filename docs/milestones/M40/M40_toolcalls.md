# M40 tool calls

| Timestamp (UTC) | Tool | Purpose | Files |
|-----------------|------|---------|-------|
| 2026-03-29 | write | Milestone stub (seeded at M39 doc closeout) | `M40_plan.md`, `M40_toolcalls.md` |
| 2026-03-29 | shell/docs | M39 merge #95, post-merge CI, `_EffOptsView` fix on `main`, closeout docs | `M39_run1.md`, `serena.md`, `serena_allowed_legacy_surfaces.md`, `M40_plan.md` |
| 2026-03-29T~ | git/shell | M40 start: branch `m40-coverage-wave-legacy-modules`, baseline Quality coverage | `M40_run1.md` |
| 2026-03-29 | write | M40 Quality tests (helpers, infotext, runtime, types) + milestone run/plan docs | `test/quality/test_m40_*.py`, `M40_run1.md`, `M40_plan.md` |
| 2026-03-29 | write | M40 recovery: defer infotext/types imports until after `initialize` (fix Quality collection on `main`) | `test_m40_processing_infotext.py`, `test_m40_processing_types.py`, `M40_run1.md` |
| 2026-03-29 | write | M40 recovery: defer `processing_runtime` import — remove module-level check; add `initialize` to runtime tests | `test_m40_processing_runtime.py`, `M40_run1.md` |
| 2026-03-29 | write | M40 recovery: remove `processing_helpers` module-level import; add `initialize` to all helper tests (fixes `sd_models.model_path` errors) | `test_m40_processing_helpers.py`, `M40_run1.md` |
| 2026-03-30 | write | M40 test fixes: random tensor shape assertion; set `token_merging_ratio` on instance (not ctor kw) | `test_m40_processing_helpers.py`, `test_m40_processing_types.py` |
| 2026-03-30 | write / shell | M40 doc closeout: `M40_run1.md` (PR stack, binding Quality **23722341901**, per-file cov, gate **42%**); `M40_plan.md` complete; `M40_summary.md` (**summaryprompt**); `M40_audit.md` (**unifiedmilestoneauditpromptV2**); `serena.md` ledger + Phase IX; seed **`M41_plan.md`**, **`M41_toolcalls.md`** | `docs/milestones/M40/*`, `docs/milestones/M41/*`, `docs/serena.md` |
