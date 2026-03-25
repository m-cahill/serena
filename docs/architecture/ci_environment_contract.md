# CI environment contract (Serena)

This document defines **deterministic, reproducible** CI environments for the Serena fork. Runtime behavior of the application is unchanged by this contract; it governs **how CI installs tools and dependencies**.

## Guarantee

**Committed manifests are the source of truth.** For the Quality workflow, **CI environments are reproducible from `requirements-ci.txt`**, a **pinned OpenAI CLIP URL** installed with fixed `pip` flags (workflow step, same commit as the lockfile), and **`pip-audit`** run as a **blocking merge gate** (artifact + **job fails** on unresolved advisories per **pip-audit policy** below; **M28a+**). **Radon** runs on **`modules/`** for **cyclomatic complexity visibility** (artifact + optional warning for grade **D/E/F**; **non-blocking** through M27 per **complexity policy** below). For JavaScript lint, **CI installs are reproducible from `package-lock.json` via `npm ci`.**

## Python — Quality workflow (`run_quality_tests.yaml`)

| Item | Source of truth |
|------|-----------------|
| Interpreter | GitHub **`actions/setup-python`** with **`python-version: 3.10.6`** (as declared in the workflow). |
| Application + test + transitive deps | **`requirements-ci.txt`** (locked) **plus** OpenAI **CLIP** from the **pinned GitHub archive URL** in the workflow (not in the uv lockfile; see install rules). |
| Pip cache key inputs | `requirements-ci.txt`, `requirements*.txt`, `launch.py` (see workflow `cache-dependency-path`). |

### Install rule

1. **`pip install -r requirements-ci.txt`** — installs the **uv-compiled** locked tree (pytest, torch, open-clip-torch, etc.). **OpenAI CLIP is intentionally omitted** from this file: treating the GitHub archive as a normal `requirements.txt` line drives **PEP 517** metadata generation, which fails on CI (`clip.py` not found, `invalid command 'bdist_wheel'`, etc.).
2. **OpenAI CLIP (pinned commit `d50d76daa670286dd6cacf3bcd80b5e4823fc8e1`)** — **documented exception**: download the GitHub **`.zip`** for that commit, unzip to `/tmp`, then **`pip install --no-build-isolation /tmp/CLIP-<sha>`** (directory install). This matches **pre‑M26** **`pip install …zip --no-build-isolation`** without relying on **`--no-use-pep517`** (not available on the runner’s pip). Changing the SHA or install mechanics requires an explicit milestone/review.
3. **`bash scripts/ci/verify_pinned_deps.sh requirements-ci.txt dependency_snapshot.txt`** — verifies pins in the lockfile and writes **`dependency_snapshot.txt`** (`pip freeze`, includes **clip** once step 2 has run). **Runs before `pip-audit`:** installing **`pip-audit`** can upgrade overlapping dependencies (e.g. **`requests`**) and would otherwise make the lockfile check falsely fail.
4. **`pip-audit`** — runs after verify; output is captured to **`pip_audit_report.txt`** and uploaded as a CI artifact. **M28a+:** non-zero exit **fails the Quality job** (blocking). Nightly remains informational (`pip-audit || true`). See **pip-audit policy** below.

### Regenerating `requirements-ci.txt`

Input file: **`requirements-ci.in`** (ordered direct requirements mirroring post‑M25 Quality logic).

The **OpenAI CLIP** GitHub archive is **not** in `requirements-ci.in` / `requirements-ci.txt` (install rule 2 above). The **`open_clip`** source ZIP is also **not** listed because some resolver tooling cannot extract that archive (duplicate ZIP entries). Resolution matches the **effective** post‑M25 state: **`open-clip-torch==2.20.0`** from PyPI.

Regenerate the lock on a machine with **`uv`**:

```bash
uv pip compile requirements-ci.in -o requirements-ci.txt \
  --python-version 3.10 --python-platform x86_64-manylinux_2_28 \
  --emit-index-url --no-annotate \
  --custom-compile-command "uv pip compile requirements-ci.in -o requirements-ci.txt --python-version 3.10 --python-platform x86_64-manylinux_2_28 --emit-index-url --no-annotate"
```

Use **`x86_64-manylinux_2_28`** (or newer manylinux tag supported by `uv`) to align with **`ubuntu-latest`** runners.

**PyTorch extra index vs PyPI:** The CPU wheel index can expose **outdated** versions of some pure-Python packages. When resolving upgrades for those, add **`--index-strategy unsafe-best-match`** so **PyPI** is considered (trusted indexes only; see `uv` docs). For **M28b-style** small batches that bump only named packages, use **`--upgrade-package <pkg>`** once per package and mirror the full command in the lockfile header **`#` comment** and in **`--custom-compile-command`**.

**Do not** replace **`requirements.txt`** or **`requirements_versions.txt`**; they remain for non–Quality workflows and developer flows unless a later milestone consolidates them.

## pip-audit policy (Phase VI)

| Phase | Behavior |
|-------|----------|
| **M26–M27** | `pip-audit` ran on every Quality workflow. Findings were **surfaced** (console + **`pip_audit_report.txt`** artifact). The job **did not fail** solely because `pip-audit` reported vulnerabilities; a **visible** workflow warning was emitted when the audit exited non-zero. |
| **M28a+ (Quality)** | **Strict enforcement**: `pip-audit` **fails the job** on unresolved advisories. Remediation is **M28b** (small-batch dependency upgrades + regression tests). |
| **Nightly** | **Informational only** (non-zero exit ignored in workflow): exploratory signal; not a merge gate. |

**Documented deferrals (M28b+):** If an advisory has **no fixed release on PyPI**, the Quality workflow may pass **`pip-audit --ignore-vuln <CVE-ID>`** for that ID **only when** the CVE, package, reason, and follow-up are recorded in **`docs/milestones/M28/M28_run1.md`**. Remove ignores when a fixed wheel is published and pins are bumped.

## pip-audit deferrals (M28)

The following CVEs are temporarily ignored due to lack of upstream fixes on PyPI:

- **CVE-2025-69872** (**diskcache**)
- **CVE-2026-4539** (**pygments**)

These **must** be removed from **`--ignore-vuln`** once fixed versions are published and **`requirements-ci.txt`** is updated.

Rationale: clearing all current advisories requires **upgrading major runtime pins** (e.g. gradio, pillow, transformers), which is **behavior and compatibility work**, not environment determinism. **M26** establishes reproducible installs; **M28** splits **enforcement** (M28a) from **remediation** (M28b).

## Complexity policy (Phase VI)

| Phase | Behavior |
|-------|----------|
| **M27** (warn-first) | **Radon** runs on every Quality workflow against **`modules/`** only (`radon cc modules -s -a`). Output is written to **`radon_report.txt`** and uploaded as a CI artifact. If any analyzed block has cyclomatic **rank D, E, or F**, the workflow emits a **visible** `::warning` (GitHub Actions). The job **does not fail** on complexity. Ranks **A–C** do not trigger a warning (legacy-heavy code is expected to include many **C** blocks). |
| **Later** | **Blocking** complexity gates (fail the job) and/or refactors to reduce complexity are **out of scope for M27** and may be scheduled in a later milestone. |

Scope is intentionally limited to **`modules/`** (not `test/`, `scripts/`, or repository root files) so the signal matches the architectural surface under refactor.

## Coverage policy (M27)

- The **Quality coverage gate** is based on **pytest execution only** (`pytest` with **`--cov`** / pytest-cov). A single **`.coverage`** file from that run is the source for **`coverage report`**, **`coverage xml`**, and **`coverage html`**.
- **Server startup is not included** in coverage measurement: the test server is started with plain **`python launch.py …`** (no **`coverage run`** on **`launch.py`**, no **`.coverage.server`**, and **no `coverage combine`** step).
- **Rationale:** import and startup paths exercised when the server boots **artificially inflate** the covered share of the denominator relative to what tests actually exercise; **pytest-only** coverage better reflects **test value and progress** toward the documented **`--fail-under=42`** gate.

## Python — Smoke / Linter (unchanged in M26)

Smoke tests and the Python linter job **continue to use** the prior multi-step install (`requirements-test.txt`, `requirements_versions.txt`, explicit torch/CLIP/open_clip steps, etc.). A later milestone may align them with `requirements-ci.txt`.

## JavaScript — Linter job (`on_pull_request.yaml`)

| Item | Source of truth |
|------|-----------------|
| Node.js | GitHub **`actions/setup-node`** with **`node-version: 18`** (same as today; no `.nvmrc` in M26). |
| Dependencies | **`package-lock.json`** committed to the repo. |

### Install rule

1. Assert **`package-lock.json`** exists (`test -f package-lock.json`).
2. **`npm ci`**
3. **`npm run lint`**
4. **`npm ls --all --json > npm_ls.json`** — uploaded as a CI artifact for supply-chain visibility.

**Do not** use **`npm install`** in CI for this job.

## Local reproduction (approximate)

Quality (Linux x86_64, Python 3.10.6):

1. Create a virtualenv with Python **3.10.6**.
2. `pip install -r requirements-ci.txt`
3. Download CLIP `d50d76daa670286dd6cacf3bcd80b5e4823fc8e1` archive, unzip, then `pip install --no-build-isolation /tmp/CLIP-d50d76daa670286dd6cacf3bcd80b5e4823fc8e1` (see workflow for exact commands).
4. `bash scripts/ci/verify_pinned_deps.sh requirements-ci.txt dependency_snapshot.txt` (before `pip-audit` if you run it locally)
5. `pip install pip-audit` then `pip-audit` after the same install order as CI (install **before** `pip-audit` can upgrade shared deps). **M28a+:** expect non-zero exit until advisories are cleared in **M28b**.

JavaScript:

1. Use **Node 18** if you need a lockfile identical to Actions; otherwise expect minor lockfile drift.
2. `npm ci && npm run lint`

## Artifacts (Quality)

Typical uploads include **`coverage.xml`**, **`htmlcov/`**, **`pip_freeze.txt`** (copy of `dependency_snapshot.txt`), **`dependency_snapshot.txt`**, **`pip_audit_report.txt`**, **`radon_report.txt`**, and **`ci_environment.txt`** (metadata + `requirements-ci.txt` digest).
