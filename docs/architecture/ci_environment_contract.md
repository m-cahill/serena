# CI environment contract (Serena)

This document defines **deterministic, reproducible** CI environments for the Serena fork. Runtime behavior of the application is unchanged by this contract; it governs **how CI installs tools and dependencies**.

## Guarantee

**Committed manifests are the source of truth.** For the Quality workflow, **CI environments are reproducible from `requirements-ci.txt` plus the documented `pip-audit` bootstrap** (see below). For JavaScript lint, **CI installs are reproducible from `package-lock.json` via `npm ci`.**

## Python — Quality workflow (`run_quality_tests.yaml`)

| Item | Source of truth |
|------|-----------------|
| Interpreter | GitHub **`actions/setup-python`** with **`python-version: 3.10.6`** (as declared in the workflow). |
| Application + test + transitive deps | **`requirements-ci.txt`** (locked). |
| Pip cache key inputs | `requirements-ci.txt`, `requirements*.txt`, `launch.py` (see workflow `cache-dependency-path`). |

### Install rule

1. **`pip install -r requirements-ci.txt`** — single step for the locked environment (includes test tools such as `pytest`, `wait-for-it`, and runtime stack).
2. **`pip install pip-audit`** — **documented exception**: the audit tool is not part of the application runtime; it is installed only to scan the frozen environment. Failures from **`pip-audit`** are **CI failures** (no `continue-on-error`).
3. **`bash scripts/ci/verify_pinned_deps.sh requirements-ci.txt dependency_snapshot.txt`** — verifies `pkg==version` pins and direct references (e.g. CLIP zip), and writes **`dependency_snapshot.txt`** (`pip freeze`).

### Regenerating `requirements-ci.txt`

Input file: **`requirements-ci.in`** (ordered direct requirements mirroring post‑M25 Quality logic).

The GitHub **`open_clip`** source ZIP is **not** listed in `requirements-ci.in` because some resolver tooling cannot extract that archive (duplicate ZIP entries). Resolution matches the **effective** post‑M25 state: **`open-clip-torch==2.20.0`** from PyPI after installs.

Regenerate the lock on a machine with **`uv`**:

```bash
uv pip compile requirements-ci.in -o requirements-ci.txt \
  --python-version 3.10 --python-platform x86_64-manylinux_2_28 \
  --emit-index-url --no-annotate \
  --custom-compile-command "uv pip compile requirements-ci.in -o requirements-ci.txt --python-version 3.10 --python-platform x86_64-manylinux_2_28 --emit-index-url --no-annotate"
```

Use **`x86_64-manylinux_2_28`** (or newer manylinux tag supported by `uv`) to align with **`ubuntu-latest`** runners.

**Do not** replace **`requirements.txt`** or **`requirements_versions.txt`**; they remain for non–Quality workflows and developer flows unless a later milestone consolidates them.

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
3. `bash scripts/ci/verify_pinned_deps.sh requirements-ci.txt dependency_snapshot.txt`

JavaScript:

1. Use **Node 18** if you need a lockfile identical to Actions; otherwise expect minor lockfile drift.
2. `npm ci && npm run lint`

## Artifacts (Quality)

Typical uploads include **`coverage.xml`**, **`pip_freeze.txt`** (copy of `dependency_snapshot.txt`), **`dependency_snapshot.txt`**, and **`ci_environment.txt`** (metadata + `requirements-ci.txt` digest).
