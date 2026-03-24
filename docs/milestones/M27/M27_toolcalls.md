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
| 2026-03-23 | gh | Open PR #54 on fork (`-R m-cahill/serena`; default `gh` repo was upstream) | https://github.com/m-cahill/serena/pull/54 |
| 2026-03-24 | gh | Squash-merge PR #54 (gate approved) | `m-cahill/serena` → `main` |
| 2026-03-24 | gh | Watch Quality on `main` | run **23473843412** — fail `fail-under=42` (40% TOTAL) |
| 2026-03-24 | Write | Add coverage tests + `M27_run1.md` | `test/quality/*_m27.py`, `test_api_extended.py`, `M27_run1.md` |
| 2026-03-24 | gh | Open PR #55 (coverage follow-up) | https://github.com/m-cahill/serena/pull/55 |
| 2026-03-24 | StrReplace | M27: pytest-only coverage — no server `coverage run`, no `combine` | `run_quality_tests.yaml` |
| 2026-03-24 | StrReplace | Coverage policy (M27) in CI contract | `ci_environment_contract.md` |
| 2026-03-24 | StrReplace | Governance decision + final verdict (measurement fix) | `M27_run1.md` |
| 2026-03-24 | Shell | Commit on `m27-coverage-measurement-fix`, push | `git` |
| 2026-03-24 | gh | Open PR #63 (M27 pytest-only coverage) | https://github.com/m-cahill/serena/pull/63 |
| 2026-03-24 | gh | Merge PR #63; watch Quality **23513449859** (pass, 47%, Radon) | `main` |
| 2026-03-24 | Write / StrReplace | M27 closeout: `M27_run1` post-fix, `M27_summary`, `M27_audit`, ledger, `M27_plan`, M28 stubs | `docs/` |
| 2026-03-24 | Shell | Annotated tag **`v0.0.27-m27`** on M27 closeout commit | `git` |

*(Append entries before significant tool invocations per `.cursorrules`.)*
