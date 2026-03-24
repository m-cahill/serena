# M27 — Tool calls log

**Branch:** `m27-coverage-complexity-gates`  
**Started:** 2026-03-23

| Timestamp (UTC) | Tool / action | Purpose | Targets |
|-----------------|---------------|---------|---------|
| 2026-03-23 | Write | Seed milestone tracking and strict tool log | `M27_toolcalls.md`, `M27_plan.md` |
| 2026-03-23 | Write | Materialize canonical M27 plan in repo | `M27_plan.md` |
| 2026-03-23 | StrReplace | Raise Quality coverage gate M26→M27 | `.github/workflows/run_quality_tests.yaml` |
| 2026-03-23 | StrReplace | Add Radon observability + D/E/F warning + artifact | `.github/workflows/run_quality_tests.yaml` |
| 2026-03-23 | StrReplace | Document complexity policy + artifacts | `docs/architecture/ci_environment_contract.md` |
| 2026-03-23 | StrReplace | Coverage gate 42% + radon checklist | `docs/PR_guardrail_checklist.md` |
| 2026-03-23 | Shell | Verify combined coverage ≥42% locally | `pytest`, `coverage` |
| 2026-03-23 | Shell | Create branch, commit, push, open PR | `git`, `gh` |
| 2026-03-23 | StrReplace | Fix complexity table phase label (M27 warn-first) | `ci_environment_contract.md` |
| 2026-03-23 | StrReplace | Proactive coverage: deprecation format + class decorator | `test/quality/test_deprecation_scaffolding.py` |
| 2026-03-23 | Shell | Git branch, commit, push, open PR to main | `m27-coverage-complexity-gates` |

*(Append entries before significant tool invocations per `.cursorrules`.)*
