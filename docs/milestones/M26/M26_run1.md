# M26 — CI run 1

**Branch:** `m26-locked-manifests-ci-env`  
**PR:** https://github.com/m-cahill/serena/pull/45  
**Date:** 2026-03-22 (PR opened); run notes updated 2026-03-23 UTC

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (`on_pull_request`, PR head) | [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195) | **pass** | `ruff` + `eslint`; `npm ci`, lockfile guard, `npm ls` artifact path |
| Smoke (`run_smoke_tests`, PR) | [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182) | **pass** | Unchanged multi-step Python install (~2m56s) |
| Quality (`run_quality_tests`, **main** only) | _pending merge_ | _TBD_ | First signal after merge: `requirements-ci.txt`, `pip-audit` (hard fail), coverage ≥ 40%, new pip artifacts |

### PR check matrix (latest)

All checks **pass** on PR #45 as of capture: **ruff**, **eslint**, **smoke tests**.

## Evidence

- **PR tier:** Linter uploads `npm-ls-json` when configured; Smoke unchanged (no `requirements-ci.txt` yet on this tier).
- **Post-merge Quality (pending):** expect artifacts `pip-freeze`, `dependency-snapshot`, `ci-environment`, `coverage-xml`; `pip-audit` must exit **0**.

## Follow-ups

- After merge to `main`: record Quality run ID, coverage %, and `pip-audit` outcome (or paste log excerpt if non-zero).
- If Quality fails on `pip-audit`: bump pins via `requirements-ci.in` → recompile `requirements-ci.txt` (no gate weakening).
