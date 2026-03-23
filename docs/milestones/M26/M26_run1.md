# M26 — CI run 1

**Branch:** `m26-locked-manifests-ci-env`  
**PR:** _(fill after open)_  
**Date:** 2026-03-22

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (on_pull_request) | _TBD_ | _TBD_ | Expect `npm ci`, `package-lock.json` present |
| Smoke (if applicable) | _TBD_ | _TBD_ | Unchanged Python path |
| Quality (post-merge main) | _TBD_ | _TBD_ | `pip install -r requirements-ci.txt`, coverage ≥ 40% |

## Evidence

- Artifacts: `npm-ls-json`, `pip-freeze`, `dependency-snapshot`, `ci-environment`, `coverage-xml` (as configured).
- `pip-audit`: must exit **0** (no `continue-on-error`).

## Follow-ups

_(None / list CI fixes if any.)_
