# M26 — CI run 1

**PRs:** [#45](https://github.com/m-cahill/serena/pull/45) (M26), [#46](https://github.com/m-cahill/serena/pull/46), [#47](https://github.com/m-cahill/serena/pull/47), [#48](https://github.com/m-cahill/serena/pull/48), [#49](https://github.com/m-cahill/serena/pull/49)  
**Date:** 2026-03-22–23 UTC

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (PR #45) | [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195) | **pass** | `npm ci`, lockfile |
| Smoke (PR #45) | [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182) | **pass** | Legacy Python path |
| Quality **main** attempt 1 | [23422081467](https://github.com/m-cahill/serena/actions/runs/23422081467) | **fail** | CLIP PEP 517 isolation → `pkg_resources` |
| Quality **main** attempt 2 (#46) | [23422117923](https://github.com/m-cahill/serena/actions/runs/23422117923) | **fail** | CLIP `pyproject.toml` path → `bdist_wheel` / `clip.py` |
| Quality **main** attempt 3 (#47) | [23422156078](https://github.com/m-cahill/serena/actions/runs/23422156078) | **fail** | Same as attempt 2 |
| Quality **main** attempt 4 (#48) | [23422287711](https://github.com/m-cahill/serena/actions/runs/23422287711) | **fail** | Runner pip: **`no such option: --no-use-pep517`** |
| Quality **main** attempt 5 (#49) | [23422412262](https://github.com/m-cahill/serena/actions/runs/23422412262) | **fail** | **Install + CLIP OK.** **`pip-audit` exit 1** — many known CVEs in pinned stack (e.g. gradio, pillow, urllib3, transformers, setuptools, starlette, h11, idna, protobuf, pytorch-lightning, wheel). Same tree as pre-M26; previously **`continue-on-error: true`**. |

## Root cause (install) — resolved (#48 / #49)

OpenAI CLIP: PEP 517 path from a flat `requirements.txt` line fails on CI. **Resolution:** `requirements-ci.txt` excludes CLIP; workflow **downloads pinned zip, unzips, `pip install --no-build-isolation /tmp/CLIP-<sha>`** (GHA pip has no `--no-use-pep517`).

## Root cause (Quality gate) — **open**

**Strict `pip-audit` (M26)** fails on the **frozen** dependency tree. **Remediation** = upgrade pins / advisory policy (M27/M28 scope) **or** an **explicit** program decision to make `pip-audit` informational again until a baseline is cleared.

## Final verdict

**M26 not closed** under the stated gate until either:

- Quality is green with **strict `pip-audit`**, or  
- Governance records an **explicit** adjustment to the audit step for this phase (documented, not silent).

Coverage / `verify_pinned_deps` / server tests were **not reached** in attempt 5 (job failed at `pip-audit`).
