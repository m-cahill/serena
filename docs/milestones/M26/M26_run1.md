# M26 — CI run 1

**Branch:** `m26-locked-manifests-ci-env` (merged via squash)  
**PR:** https://github.com/m-cahill/serena/pull/45  
**Merge:** squash to `main` (M26 subject); first `main` tip after merge includes M26 changes  
**Date:** 2026-03-22 (PR opened); run notes updated 2026-03-23 UTC

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (`on_pull_request`, PR head) | [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195) | **pass** | `ruff` + `eslint`; `npm ci`, lockfile guard, `npm ls` artifact path |
| Smoke (`run_smoke_tests`, PR) | [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182) | **pass** | Unchanged multi-step Python install (~2m56s) |
| Quality (`run_quality_tests`, **main**, post-merge attempt 1) | [23422081467](https://github.com/m-cahill/serena/actions/runs/23422081467) | **fail** | **Install step:** building `clip` from GitHub archive under PEP 517 isolation → `ModuleNotFoundError: No module named 'pkg_resources'`. Pre‑M26 CI used `--no-build-isolation` for CLIP only. |
| Quality (`run_quality_tests`, **main**, post-fix) | _TBD_ | _TBD_ | Fix: `pip install --no-build-isolation -r requirements-ci.txt` + contract doc update (follow-up PR). |

### PR check matrix (pre-merge)

All checks **pass** on PR #45: **ruff**, **eslint**, **smoke tests**.

## Evidence

- **PR tier:** Linter + Smoke green as above.
- **Quality (attempt 1):** failed before `pip-audit`, `verify_pinned_deps`, tests, or coverage — **no signal** yet on audit or ≥40% gate.

## Remediation (binding for M26 closeout)

- **Do not** weaken install or drop CLIP from the lockfile without milestone decision.
- **Do** align install flags with pre‑M26 behavior: **`--no-build-isolation`** for the locked install step (documented in `docs/architecture/ci_environment_contract.md`).

## Follow-ups

- Record **second** Quality run (post-fix) with: run ID, `pip-audit` pass/fail, coverage %, artifact confirmation.
- If `pip-audit` fails after install fix: bump pins via `requirements-ci.in` → recompile `requirements-ci.txt`.

## Final verdict

**M26 not closed** until Quality (post-fix) is green on `main` per gate (install, `pip-audit`, verify script, coverage ≥ 40%, artifacts).
