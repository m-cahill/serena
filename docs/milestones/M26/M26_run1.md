# M26 — CI run 1

**PRs:** [#45](https://github.com/m-cahill/serena/pull/45) (M26), [#46](https://github.com/m-cahill/serena/pull/46) (`--no-build-isolation`), [#47](https://github.com/m-cahill/serena/pull/47) (setuptools/wheel order)  
**Follow-up (CLIP / PEP 517):** PR _TBD_ — remove CLIP from uv lockfile; **`pip install --no-use-pep517`** for pinned CLIP URL after locked tree  
**Date:** 2026-03-22–23 UTC

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (PR #45) | [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195) | **pass** | `npm ci`, lockfile |
| Smoke (PR #45) | [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182) | **pass** | Legacy Python path |
| Quality **main** attempt 1 | [23422081467](https://github.com/m-cahill/serena/actions/runs/23422081467) | **fail** | CLIP PEP 517 isolation → `pkg_resources` |
| Quality **main** attempt 2 (#46) | [23422117923](https://github.com/m-cahill/serena/actions/runs/23422117923) | **fail** | CLIP still via `pyproject.toml` path → `bdist_wheel` / `clip.py` |
| Quality **main** attempt 3 (#47) | [23422156078](https://github.com/m-cahill/serena/actions/runs/23422156078) | **fail** | Same as attempt 2 (ordering alone insufficient) |
| Quality **main** attempt 4 | _after PR merge_ | _TBD_ | **Fix:** CLIP **not** in `requirements-ci.txt`; workflow `pip install --no-use-pep517` + URL |

## Root cause (install)

OpenAI CLIP GitHub archive: **`pip` PEP 517 / `pyproject.toml` metadata** path is **broken** for this tree on **`ubuntu-latest`**; pre‑M26 succeeded because install behaved like **legacy `setup.py`** (**`--no-build-isolation`** and **no PEP 517**). **M26 fix:** keep full lockfile for everything else; **pin CLIP URL + flags in the workflow** (documented exception).

## Final verdict

**M26 not closed** until Quality **attempt 4** is green on `main` (install, `pip-audit`, verify, coverage ≥ 40%, artifacts).
