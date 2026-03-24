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

---

## M28b — Batch 2 (Pillow / image stack) — 2026-03-25

**Intent:** Move **Pillow** into the **10.3+** line (`pillow>=10.3.0,<11` per `requirements-ci.in`) to clear **Pillow 9.x** advisory rows.

### Co-upgrade: `blendmodes`

**`blendmodes==2022`** declares `pillow<10`, so a Pillow 10 upgrade is **unsatisfiable** without bumping blendmodes. **`blendmodes==2024`** supports **`Pillow>=10,<11`** and **`numpy<2`** (avoids the NumPy 2 jump required by **`blendmodes==2025`**). This is a **mandatory compatibility co-change**, not an unrelated dep bump.

| Package     | Before   | After    |
|-------------|----------|----------|
| `pillow`    | 9.5.0    | **10.4.0** |
| `blendmodes`| 2022     | **2024** |

### Lockfile regeneration

Same **`uv pip compile`** pattern as batch 1, with **`--upgrade-package pillow`** added to the header (HTTP upgrade packages retained).

### pip-audit (local, `pip-audit -r requirements-ci.txt`)

| Metric | After batch 1 | After batch 2 |
|--------|---------------|---------------|
| “Found N known vulnerabilities” | 81 | **77** |
| Packages with findings | 13 | **13** |

**Pillow:** All advisory rows tied to **Pillow 9.5.0** in the prior report are **gone** (replaced by a single row for **10.4.0**). **One** row remains for **`pillow 10.4.0`** (**CVE-2026-25990**; advisory fix version **12.1.1** — outside the **`<11`** cap for this batch). Further reduction may require a later milestone decision (Pillow 11+ / major).

### Runtime / tests

- No edits to **`modules/images.py`** or **`modules/extras.py`**; **`processing.py`** import **`from blendmodes.blend import blendLayers, BlendType`** unchanged for **blendmodes 2024**.
- **Local:** full pytest / `verify_pinned_deps.sh` not run here; **CI** is the binding check.

### CI summary

- **Quality:** `pip-audit` step still **expected to fail** until more packages are remediated; non-audit steps **expected green** if the environment matches the lock.

---

## M28b — Batch 3 (FastAPI / Starlette / h11) — 2026-03-25

**Intent:** Raise **`fastapi`**, **`starlette`**, **`h11`** to advisory-safe ranges (`fastapi>=0.110,<1`, `starlette>=0.37,<1`, `h11>=0.14,<1` in `requirements-ci.in`).

### Co-upgrades (required for a solvable graph)

| Package | Issue | Resolution |
|---------|--------|------------|
| **`httpcore`** | `0.15.0` pins **`h11>=0.11,<0.13`** — conflicts with **`h11>=0.14`** | **`httpcore>=1.0,<2`** |
| **`httpx`** | Old line tied to httpcore 0.15 | **`httpx>=0.27,<1`** (resolves to **0.28.1** with httpcore **1.x**) |

### Resolver outcome (major)

Upgrading FastAPI past **~0.100** pulls **Pydantic v2** (`pydantic==2.12.5`, `pydantic-core`). **Runtime updates (compatibility only):**

- **`modules/api/models.py`:** `create_model(..., __config__=ConfigDict(populate_by_name=True, validate_assignment=True))` replaces v1 `__config__` mutation after `create_model`.
- **`modules/api/api.py`:** helpers for **`model_dump` / `.dict`**, **`model_fields` / `__fields__`**, **`model_copy` / `.copy`** so infotext + txt2img/img2img API paths work on Pydantic v2.

### Pin changes (lockfile excerpt)

| Package | Before (post batch 2) | After batch 3 |
|---------|------------------------|---------------|
| fastapi | 0.94.0 | **0.135.2** |
| starlette | 0.26.1 | **0.52.1** |
| h11 | 0.12.0 | **0.16.0** |
| httpcore | 0.15.0 | **1.0.9** |
| httpx | 0.24.1 | **0.28.1** |
| pydantic | 1.10.26 | **2.12.5** (transitive) |

### pip-audit (local, `pip-audit -r requirements-ci.txt`)

| Metric | After batch 2 | After batch 3 |
|--------|---------------|---------------|
| “Found N known vulnerabilities” | 77 | **71** |
| Packages with findings | 13 | **13** |

**Cleared from advisory output in this mode:** prior **fastapi / starlette / h11** rows (and **httpx** client CVE rows tied to the old pair). **CI summary:** binding pass/fail on **Quality** (non-audit steps) TBD on push; local full pytest not run.

---

## M28b — Batch 4 (setuptools / wheel / filelock / GitPython) — 2026-03-25

**Intent:** Bump low-risk tooling / packaging / lock / Git bindings without touching ML or Pillow policy.

### `requirements-ci.in`

| Package | Spec |
|---------|------|
| setuptools | `>=70,<80` (was `==70.0.0`) |
| wheel | `>=0.43,<1` (was `==0.45.1`) |
| filelock | `>=3.13,<4` (new explicit line; was transitive only) |
| GitPython | `>=3.1.40,<4` (was `==3.1.32`) |

### Resolved pins (`requirements-ci.txt`)

| Package | Before (batch 3 lock) | After batch 4 |
|---------|------------------------|---------------|
| setuptools | 70.0.0 | **79.0.1** |
| wheel | 0.45.1 | **0.46.3** |
| filelock | 3.20.0 | **3.25.2** |
| gitpython | 3.1.32 | **3.1.46** |

### pip-audit (local, `pip-audit -r requirements-ci.txt`)

| Metric | After batch 3 | After batch 4 |
|--------|---------------|---------------|
| “Found N known vulnerabilities” | 71 | **62** |
| Packages with findings | 13 | **12** |

### Runtime

- No application code changes; **GitPython** / **filelock** / **setuptools** / **wheel** are infrastructure-adjacent. **Local pytest / verify_pinned_deps** not run; **CI** is binding.

### CI summary

- **Quality:** `pip-audit` still expected to **fail** until ML / remaining stacks are addressed; other jobs expected **green** on matching install.
