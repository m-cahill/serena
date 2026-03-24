# CI environment contract (Serena)

This document defines **deterministic, reproducible** CI environments for the Serena fork. Runtime behavior of the application is unchanged by this contract; it governs **how CI installs tools and dependencies**.

## Guarantee

**Committed manifests are the source of truth.** For the Quality workflow, **CI environments are reproducible from `requirements-ci.txt`**, a **pinned OpenAI CLIP URL** installed with fixed `pip` flags (workflow step, same commit as the lockfile), and **`pip-audit`** run for **visibility** (artifact + warning; **non-blocking** through M27 per **pip-audit policy** below). For JavaScript lint, **CI installs are reproducible from `package-lock.json` via `npm ci`.**

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
4. **`pip-audit`** — runs after verify; output is captured to **`pip_audit_report.txt`** and uploaded as a CI artifact. **Failures are non-blocking (informational)** through **M27**; **strict enforcement** (exit non-zero fails the job) is planned for **M28 — Security & Supply Chain Hardening** (see **pip-audit policy** below).

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

**Do not** replace **`requirements.txt`** or **`requirements_versions.txt`**; they remain for non–Quality workflows and developer flows unless a later milestone consolidates them.

## pip-audit policy (Phase VI)

| Phase | Behavior |
|-------|----------|
| **M26–M27** | `pip-audit` runs on every Quality workflow. Findings are **surfaced** (console + **`pip_audit_report.txt`** artifact). The job **does not fail** solely because `pip-audit` reported vulnerabilities; a **visible** workflow warning is emitted when the audit exits non-zero. |
| **M28+** | **Strict enforcement**: `pip-audit` (or successor gate) is expected to **fail the job** on unresolved advisories, aligned with supply-chain hardening and intentional dependency upgrades. |

Rationale: clearing all current advisories requires **upgrading major runtime pins** (e.g. gradio, pillow, transformers), which is **behavior and compatibility work**, not environment determinism. **M26** establishes reproducible installs; **M28** owns remediation and enforcement.

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
5. Optional: `pip install pip-audit` and `pip-audit` (informational; may upgrade shared packages)

JavaScript:

1. Use **Node 18** if you need a lockfile identical to Actions; otherwise expect minor lockfile drift.
2. `npm ci && npm run lint`

## Artifacts (Quality)

Typical uploads include **`coverage.xml`**, **`pip_freeze.txt`** (copy of `dependency_snapshot.txt`), **`dependency_snapshot.txt`**, **`pip_audit_report.txt`**, and **`ci_environment.txt`** (metadata + `requirements-ci.txt` digest).
