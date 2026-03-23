# M26 — CI run 1

**Branch:** `m26-locked-manifests-ci-env` (merged via squash)  
**PR:** https://github.com/m-cahill/serena/pull/45  
**Follow-up:** https://github.com/m-cahill/serena/pull/46 (`--no-build-isolation`)  
**Merge:** squash to `main`; M26 + hotfixes land as chained pushes  
**Date:** 2026-03-22 (PR opened); run notes updated 2026-03-23 UTC

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (`on_pull_request`, PR head) | [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195) | **pass** | `ruff` + `eslint`; `npm ci`, lockfile guard, `npm ls` artifact path |
| Smoke (`run_smoke_tests`, PR) | [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182) | **pass** | Unchanged multi-step Python install (~2m56s) |
| Quality (`main`, attempt 1) | [23422081467](https://github.com/m-cahill/serena/actions/runs/23422081467) | **fail** | **Install:** CLIP under PEP 517 isolation → `ModuleNotFoundError: No module named 'pkg_resources'`. |
| Quality (`main`, attempt 2, post #46) | [23422117923](https://github.com/m-cahill/serena/actions/runs/23422117923) | **fail** | **Install:** with `--no-build-isolation`, `clip` processed **before** `wheel` (alphabetical lockfile order) → `invalid command 'bdist_wheel'`, `file clip.py … not found`. |
| Quality (`main`, attempt 3) | _TBD_ | _TBD_ | **Fix:** move `setuptools==70.0.0` + `wheel==0.45.1` to top of `requirements-ci.txt` after index URLs; document post-`uv` edit in contract. |

### PR check matrix (pre-merge #45)

All checks **pass** on PR #45: **ruff**, **eslint**, **smoke tests**.

## Evidence

- **PR tier:** Linter + Smoke green as above.
- **Quality (attempts 1–2):** failed in **install** before `pip-audit`, `verify_pinned_deps`, tests, or coverage.

## Remediation log

1. **#46:** `pip install --no-build-isolation -r requirements-ci.txt` + contract update.  
2. **Lockfile order:** pre‑M26 explicitly installed `setuptools` / `wheel` before CLIP; uv-sorted lockfile violated that ordering — **edit `requirements-ci.txt`** after compile (see `ci_environment_contract.md`).

## Follow-ups

- Record **attempt 3** Quality: run ID, `pip-audit`, coverage %, artifacts.
- If `pip-audit` fails after install succeeds: bump pins via `requirements-ci.in` → recompile → **post-process** setuptools/wheel lines.

## Final verdict

**M26 not closed** until Quality is green on `main` (install, `pip-audit`, verify script, coverage ≥ 40%, artifacts).
