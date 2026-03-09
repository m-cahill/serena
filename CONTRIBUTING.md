# Contributing to Serena

Serena is a governed refactor program for AUTOMATIC1111/stable-diffusion-webui. This guide helps you run verification locally and understand CI behavior.

---

## Quickstart

1. Install dependencies: `pip install -r requirements-test.txt` and runtime deps per `requirements_versions.txt`
2. Create stub repositories: `python scripts/dev/create_stub_repos.py`
3. Run tests: see [Local verification](#local-verification) below

---

## Local verification

To verify the project builds and tests pass without a real model:

```bash
python launch.py --skip-prepare-environment --skip-torch-cuda-test --exit
pytest test/smoke
```

For full CI parity (including server startup and API tests), start the test server in one terminal, then run pytest in another. See `.github/workflows/run_smoke_tests.yaml` for the exact commands CI uses.

**Test tiers:** `test/smoke` (fast, PR gate), `test/quality` (deeper unit tests), `test/nightly` (heavy tests). Run `pytest test` for the full suite.

---

## CI parity

CI uses deterministic stub repositories and fake inference to avoid external clones and real model loading. To reproduce CI locally:

1. Run `python scripts/dev/create_stub_repos.py` before any launch or test
2. Use `--skip-prepare-environment` when launching
3. CI sets `CI=true` (GitHub Actions default); txt2img/img2img return a deterministic 1×1 PNG in CI instead of invoking the model

---

## Stub repositories

CI uses stub repositories to satisfy import paths without cloning large external repos (e.g. ldm, sgm). See `scripts/dev/create_stub_repos.py` for implementation. The script creates minimal placeholder modules so the application can start and API contract tests can run.

---

## Development workflow

1. Create a branch from `main`
2. Make changes; run `ruff .` and `pytest test` locally
3. Open a PR targeting `m-cahill/serena:main`; CI runs linter, tests, and coverage
4. Do not push directly to `main`; merge via PR after CI passes

For milestone-specific workflow, see `docs/serena.md` and `docs/milestones/`.

---

## Serena repository workflow

Serena operates as an **independent governed fork** of AUTOMATIC1111/stable-diffusion-webui. The upstream repository is used only as a **reference baseline** for audit comparisons.

All development must occur within the Serena repository (`m-cahill/serena`).

**Correct PR flow:**

```
feature-branch → PR → m-cahill/serena:main
```

**Incorrect PR flow (never do this):**

```
m-cahill/serena → AUTOMATIC1111/stable-diffusion-webui
```

Upstream PRs must never be opened. CI includes a guardrail that fails if workflows run outside `m-cahill/serena`.

---

## Pre-push hook (optional)

To prevent accidentally pushing to upstream or other non-Serena remotes, install the pre-push hook:

```bash
cp scripts/dev/prevent_upstream_push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

The hook aborts the push if the target remote URL does not contain `m-cahill/serena`.
