# M28 — Run log 1 (M28a enforcement)

**Branch:** `m28-security-supply-chain`  
**Target:** `m-cahill/serena:main`  
**Date (UTC):** 2026-03-24

## M28a objective

Enable **blocking `pip-audit`** in **Quality** only. **No** dependency / lockfile changes in this step. **Expected:** Quality fails on `main` after merge until **M28b** clears advisories.

## Baseline vulnerability snapshot (pre-remediation)

Source: `docs/milestones/M28/baseline_audit.txt` — `pip-audit -r requirements-ci.txt` on a dev machine (Python 3.11). CI audits the **installed** environment after `requirements-ci.txt` + CLIP; counts may differ slightly.

**Summary**

| Metric | Value |
|--------|-------|
| Reported vulnerability rows (tool output) | 100 |
| Distinct packages with findings | 17 |
| torch / torchvision | Skipped in `-r` mode (CPU extra-index URLs); audited on CI when installed |

**Packages (alphabetic)** — use for M28b batch planning:

certifi, diskcache, fastapi, filelock, gitpython, gradio, h11, idna, pillow, protobuf, pytorch-lightning, requests, setuptools, starlette, transformers, urllib3, wheel.

**Tiering (for M28b)**

1. **Tier 1 — direct / HTTP stack (low blast radius):** certifi, idna, requests, urllib3, pillow (often batched with care).
2. **Tier 2 — app stack / transitive:** fastapi, starlette, h11, gitpython, filelock, wheel, setuptools.
3. **Tier 3 — heavy / major-jump risk:** gradio, transformers, protobuf, pytorch-lightning (align with upstream webui constraints; upgrade last or in dedicated PRs).

## CI change (M28a)

- **`run_quality_tests.yaml`:** `pip-audit | tee pip_audit_report.txt` with **`set -o pipefail`** — non-zero audit **fails** the step; removed M26–M27 warning-only branch.
- **`run_nightly_tests.yaml`:** unchanged (informational `pip-audit`).

## Governance docs

- `docs/architecture/ci_environment_contract.md` — pip-audit policy **M28a+** blocking on Quality.
- `docs/PR_guardrail_checklist.md` — pip-audit blocking expectation.

## Expected CI outcome

After this PR merges to `main`, **Quality** should **fail** at the dependency vulnerability scan until **M28b** upgrades pins and/or documents rare deferrals.

## Next (M28b)

1. Small-batch upgrades (e.g. urllib3 / requests / certifi first).
2. Recompile `requirements-ci.txt` from `requirements-ci.in` with `uv pip compile` per contract.
3. Add regression tests before or with behavior-sensitive bumps.
4. Iterate until `pip-audit` exits 0 and coverage stays **≥ 42%**.

## Deferrals

None yet. Any deferral must list CVE, package, reason, follow-up, and still keep CI green via safest pin / isolation per locked policy.
