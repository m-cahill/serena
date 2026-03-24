# M26 — CI run 1

**PRs:** [#45](https://github.com/m-cahill/serena/pull/45)–[#51](https://github.com/m-cahill/serena/pull/51), [#52](https://github.com/m-cahill/serena/pull/52) _verify order_  
**Date:** 2026-03-22–23 UTC

## Governance — `pip-audit` (post–attempt 5)

**Decision:** **`pip-audit` is informational (non-blocking) for M26–M27.** Output is **`tee`**’d to **`pip_audit_report.txt`** and uploaded; workflow emits **`::warning`** when the audit exits non-zero. **Strict failure** is **deferred to M28** (supply-chain / remediation milestone), because clearing advisories requires dependency upgrades that change **behavior and compatibility**, not just CI infra.

Documented in **`docs/architecture/ci_environment_contract.md`** (section **pip-audit policy (Phase VI)**).

## Workflows

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (PR #45) | [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195) | **pass** | `npm ci`, lockfile |
| Smoke (PR #45) | [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182) | **pass** | Legacy Python path |
| Quality **main** attempt 1 | [23422081467](https://github.com/m-cahill/serena/actions/runs/23422081467) | **fail** | CLIP PEP 517 isolation → `pkg_resources` |
| Quality **main** attempt 2 (#46) | [23422117923](https://github.com/m-cahill/serena/actions/runs/23422117923) | **fail** | CLIP `pyproject.toml` path → `bdist_wheel` / `clip.py` |
| Quality **main** attempt 3 (#47) | [23422156078](https://github.com/m-cahill/serena/actions/runs/23422156078) | **fail** | Same as attempt 2 |
| Quality **main** attempt 4 (#48) | [23422287711](https://github.com/m-cahill/serena/actions/runs/23422287711) | **fail** | **`no such option: --no-use-pep517`** |
| Quality **main** attempt 5 (#49) | [23422412262](https://github.com/m-cahill/serena/actions/runs/23422412262) | **fail** | Install + CLIP OK; **strict `pip-audit` exit 1** (many CVEs on frozen tree). |
| Quality **main** attempt 6 (#51) | [23467606465](https://github.com/m-cahill/serena/actions/runs/23467606465) | **fail** | Informational **`pip-audit`** OK; **`verify_pinned_deps`**: `requests` expected **2.28.1**, got **2.32.5** — **`pip install pip-audit`** upgraded **`requests`** before verify ran. |
| Quality **main** attempt 7 (#52) | _after merge_ | _TBD_ | **Fix:** run **verify lockfile** before **`pip-audit`** (workflow + contract). |

## Root cause (install) — resolved (#48 / #49)

OpenAI CLIP: use **workflow** `curl` + `unzip` + **`pip install --no-build-isolation /tmp/CLIP-<sha>`**; CLIP **not** in `requirements-ci.txt`.

## Final verdict

**M26 closeout** pending **attempt 7** Quality green (verify, tests, coverage ≥ 40%, artifacts including **`pip-audit-report`**).
