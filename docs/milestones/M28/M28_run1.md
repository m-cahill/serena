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

See **M28b — Batch 5b** for **diskcache** (CVE-2025-69872) and **pygments** (CVE-2026-4539) — no fixed release on PyPI at lock time. Any deferral must list CVE, package, reason, follow-up, and still keep CI green via safest pin / isolation per locked policy.

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

---

## M28b — Batch 5a (Pillow 12.x — CVE-2026-25990) — 2026-03-25

**Governance:** Proceed with **Pillow 12+** (not deferral).

### Dependency reality (PyPI — not optional)

A **pillow-only** bump is **unsatisfiable** with the pre-5a graph:

| Blocker | Constraint |
|---------|------------|
| **blendmodes 2024** | `Pillow>=10,<11` — blocks Pillow 12 |
| **gradio 3.41.2** | `pillow<11` — blocks Pillow 12 |
| **blendmodes 2025** | `numpy>=2.0.2`, `pillow>=10.4` — requires **NumPy 2** |
| **gradio 6.5.0** | First **Gradio** release checked with `pillow<13,>=8` (allows **Pillow 12**); also `numpy<3,>=1`, `fastapi>=0.115.2`, `starlette>=0.40` |

**Batch 5a therefore includes mandatory co-upgrades** (same lockfile / CI install):

| Package | Before | After (resolved) |
|---------|--------|------------------|
| **pillow** | 10.4.0 | **12.1.1** (`pillow>=12.0.0,<13`) |
| **blendmodes** | 2024 | **2025** |
| **numpy** | 1.26.2 | **2.2.6** (`numpy>=2.0.2,<3`) |
| **gradio** | 3.41.2 | **6.5.0** |
| **gradio-client** | (transitive 0.5.0) | **2.0.3** (via Gradio 6) |

**Application code:** No edits in this commit; **Gradio 3 → 6** may require follow-up UI/API fixes if CI surfaces runtime errors — that is **expected risk** for this decision.

### pip-audit (local, `pip-audit -r requirements-ci.txt`)

| Metric | After batch 4 | After batch 5a |
|--------|---------------|----------------|
| “Found N known vulnerabilities” | 62 | **30** |
| **pillow** rows (CVE-2026-25990, etc.) | present on 10.x | **cleared** at **12.1.1** |

### CI summary

- **Quality:** `pip-audit` should still **fail** on remaining packages (e.g. **transformers**, **protobuf**, **gradio-adjacent** noise if any); non-audit steps validate **install + tests + coverage** against this graph.
- **Binding check:** full **Quality** run on the PR branch (Gradio 6 + NumPy 2 + Torch).

---

## M28b — Batch 5a stabilization (Gradio 6 / NumPy 2) — 2026-03-26

**Observed breakages (import-time, Gradio 6):**

| Symptom | Cause | Fix |
|--------|--------|-----|
| `AttributeError: module 'gradio.components' has no attribute 'IOComponent'` | Gradio 6 renamed **`IOComponent` → `Component`** | Patch **`gr.components.Component.__init__`** instead of `IOComponent` (`modules/gradio_extensons.py`) |
| `gradio.components.IOComponent.pil_to_temp_file` missing | Temp-file hook removed from the base class; saving is internal to Gradio | **`install_ui_tempdir_override`**: only assign **`pil_to_temp_file`** when the attribute exists; otherwise no-op (`modules/ui_tempdir.py`). PNG metadata in temp paths may be reduced vs Gradio 3. |
| Doc / extension API comments | Stale name | **`script_callbacks`**: docstring now references **`Component`** |

**NumPy 2:** No code changes in this pass; repo had no `np.bool` / `np.int` aliases in `modules/` (common break pattern).

**Local verification:** Full **Quality** suite not reproduced on this machine (missing **torchvision** / **piexif** in the dev env); **13** extension/deprecation contract tests passed. **CI** remains the binding gate for the full matrix.

**Commits:** stabilization applied as **`m28b: fix gradio 6 compatibility (minimal adapter)`** (see git log).

---

## M28b — Batch 5b (ML stack: protobuf / pytorch-lightning / transformers) — 2026-03-26

**Intent:** Close the **ML / heavy runtime** advisory cluster while micro-stepping upgrades.

### Input pins (`requirements-ci.in`)

| Step | Pin | Notes |
|------|-----|--------|
| 1 | `protobuf>=5,<6` | Required **`open-clip-torch>=2.24`** (older pins capped `protobuf<4`). |
| 2 | `pytorch_lightning>=2.2,<3` | Resolved **2.6.1**; existing **`fix_pytorch_lightning()`** maps **`utilities.distributed` → `rank_zero`** for PL2. |
| 3 | `transformers>=4.57,<5` | **4.49.x** still reported multiple CVEs in `pip-audit`; **4.57.6** clears those rows. Requires **`safetensors>=0.4.3`** (resolved **0.7.0**). |
| — | `gradio>=6.7,<7` | Clears **Gradio 6.5.x** CVE rows; resolved **6.10.0** (with **`gradio-client` 2.4.0**, **`hf-gradio` 0.3.0** transitive). |

### pip-audit (local, `pip-audit -r requirements-ci.txt`, Python 3.11)

| Metric | After batch 5a stabilization | After batch 5b |
|--------|---------------------------|----------------|
| “Found N known vulnerabilities” | 30 | **2** |
| Packages with findings | (mixed) | **2** |

**Remaining (no installable fix on PyPI at lock time):**

| CVE | Package | Version | Reason / follow-up |
|-----|---------|---------|---------------------|
| CVE-2025-69872 | **diskcache** | 5.6.3 (latest on PyPI) | Unsafe pickle deserialization; **no release >5.6.3** yet. **Follow-up:** bump `diskcache` when upstream publishes a fix; avoid loading attacker-controlled cache dirs. |
| CVE-2026-4539 | **pygments** | 2.19.2 (latest on PyPI) | ReDoS in **AdlLexer**; advisory fix **≥2.19.3** but **2.19.3 not published**. **Follow-up:** pin **`pygments>=2.19.3`** on first PyPI release. |

**Skipped audit (unchanged):** `torch` / `torchvision` **+cpu** wheels — not on PyPI for `pip-audit -r`; **CI** installs and may surface different rows.

### CI expectation

- **Quality:** `pip-audit` runs with **`--ignore-vuln`** only for the two rows above (**governed** in **`ci_environment_contract.md`**); **`set -o pipefail`** — any **other** advisory **fails** the job.
- **Regression focus:** `transformers` / **`safetensors`** loading paths, **Gradio 6.10** UI shim (same adapter pattern as 6.5).

---

## M28 — Finalization (governance deferrals + Quality gate) — 2026-03-26

**Workflow:** `.github/workflows/run_quality_tests.yaml` — **`pip-audit`** with **`--ignore-vuln CVE-2025-69872`** and **`--ignore-vuln CVE-2026-4539`** only; **`set -o pipefail`** unchanged.

**pip-audit (effective):** **0** unresolved advisories after documented ignores. Expected output (installed env or `pip-audit -r requirements-ci.txt` with same flags): **“No known vulnerabilities found, 2 ignored”**. Raw lockfile audit without ignores: **2** rows (**diskcache**, **pygments**) — **no PyPI fix** at closeout.

**Quality run ID (on `main`):** There is **no** run ID for “M28-only green on **`main`**.” M28 and M29 landed together in **PR #64** (squash merge **`f18b73f2`**). The first **`main`** Quality after that merge was **[23566817312](https://github.com/m-cahill/serena/actions/runs/23566817312)** — **failure** (start of the M29 recovery chain). Topic-branch finalize commits (**`f88e1e9c`**, tag **`c97c406`**) are not first-parent commits on current **`main`**. **Stack-level** verification of the locked manifest + blocking **`pip-audit`** + deferrals is evidenced by the later binding run **23618918747** (see **`docs/milestones/M30/M30_run1.md`** §3).

**Final verdict:** **M28 complete.** All **resolvable** CVEs were cleared via **M28b** dependency upgrades and minimal adapters; **diskcache** and **pygments** are **explicit, contract-backed deferrals** until upstream publishes fixed wheels — **not** a disabled audit or weakened gate.
