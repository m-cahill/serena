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

---

## M28b — Batch 1 (HTTP stack) — 2026-03-25

**Intent:** Upgrade only **`requests`**, **`urllib3`**, **`certifi`**, **`idna`** with minimal lockfile drift.

### Lockfile regeneration

Used **`uv pip compile`** with **`--index-strategy unsafe-best-match`** (PyTorch CPU index lists stale pure-Python stubs; PyPI must participate) and **selective** resolution:

`--upgrade-package requests --upgrade-package urllib3 --upgrade-package certifi --upgrade-package idna`

**Diff vs previous `requirements-ci.txt`:** only the four pins below (plus header comment / CLIP note preserved).

| Package   | Before     | After      |
|-----------|------------|------------|
| certifi   | 2022.12.7  | 2026.2.25  |
| idna      | 3.4        | 3.11       |
| requests  | 2.28.1     | 2.32.5     |
| urllib3   | 1.26.13    | 2.6.3      |

### pip-audit (local, `pip-audit -r requirements-ci.txt`)

| Metric | Before (baseline snapshot) | After batch 1 |
|--------|---------------------------|---------------|
| Vulnerability rows (same mode) | 100 | **81** (`pip-audit` “Found N known vulnerabilities”; no rows for certifi / idna / requests / urllib3) |
| Packages with findings | 17 | **13** |

**Cleared from advisory output in this mode:** HTTP cluster (`certifi`, `idna`, `requests`, `urllib3`). **Remaining:** pillow, diskcache, fastapi, starlette, filelock, gitpython, gradio, h11, protobuf, pytorch-lightning, setuptools, transformers, wheel (unchanged from baseline except HTTP).

### CI expectation

- **Quality:** still **fails** `pip-audit` until later batches; **tests / coverage / verify_pinned_deps** should pass if install matches lock.
- **Local:** full `verify_pinned_deps.sh` / pytest not run here (no Linux CI-sized venv).

### Notes

- `requirements-ci.in` documents batch intent in a comment; selective flags live in **`requirements-ci.txt`** autogen header.
- `docs/architecture/ci_environment_contract.md` updated: **unsafe-best-match** + **`--upgrade-package`** for small-batch bumps.
