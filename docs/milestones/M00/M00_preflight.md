# M00 Preflight — Detected Surfaces & Constraints

**Date:** 2025-03-06  
**Branch:** m00-kickoff-baseline-e2e  
**Baseline tag:** baseline-pre-refactor  
**Baseline SHA:** 82a973c04367123ae98bd9abdf80d9eda9b910e2

---

## 1. Project Shape

- **Full-stack Python + JS app**
- **Entry points:** `launch.py`, `webui.py`
- **Core package:** `modules/` (~150+ Python files)
- **Extensions:** `extensions-builtin/`, `scripts/`
- **Tests:** `test/` (7 test modules)

---

## 2. Runtime Surfaces

| Surface | Location | Evidence |
|---------|----------|----------|
| **Gradio UI** | `modules/ui.py`, `webui.py` | Port 7860 default; `create_ui()` builds all tabs |
| **FastAPI API** | `modules/api/api.py` | Routes under `/sdapi/v1/*` (txt2img, img2img, options, progress, etc.) |
| **Launch/bootstrap** | `launch.py`, `modules/launch_utils.py` | `launch.py` → `launch_utils.start()` → `webui.start()` |
| **Extension/script loading** | `modules/extensions.py`, `modules/script_loading.py`, `modules/scripts.py` | `list_extensions()`, `load_module()`, `Script` base class |

**API routes exercised by tests:**
- `/sdapi/v1/txt2img` (test_txt2img.py)
- `/sdapi/v1/img2img` (test_img2img.py)
- `/sdapi/v1/extra-single-image` (test_extras.py)
- `/sdapi/v1/options`, `/sdapi/v1/cmd-flags`, samplers, upscalers, etc. (test_utils.py)

**No health endpoint:** No `/sdapi/v1/health` or equivalent; tests use txt2img/img2img as integration probes.

---

## 3. Existing Test Baseline

| Component | Location | Evidence |
|-----------|----------|----------|
| **Lint workflows** | `.github/workflows/on_pull_request.yaml` | ruff (Python), eslint (JS) |
| **Pytest server-backed tests** | `.github/workflows/run_tests.yaml` | Server started in background, `wait-for-it 127.0.0.1:7860`, pytest against base_url |
| **Coverage collection** | `run_tests.yaml:45-69` | `coverage run` for server, `pytest --cov . --cov-report=xml`, `coverage combine`, `coverage report -i` |
| **Test modules** | `test/*.py` | test_txt2img, test_img2img, test_extras, test_utils, test_torch_utils, test_face_restorers |
| **Session fixture** | `conftest.py:36-37` | `initialize` imports `webui` (session scope) |

**Coverage:** No `--cov-fail-under`; no threshold enforced.

---

## 4. Packaging Posture

- **Python:** `requirements.txt` (mixed pins), `requirements-test.txt` (pytest, pytest-cov, pytest-base-url), `requirements_versions.txt`
- **JS:** `package.json`; `package-lock.json` is gitignored
- **CI install:** `pip install wait-for-it -r requirements-test.txt`; `launch.py --skip-torch-cuda-test --exit` for env setup
- **M00 scope:** Do not introduce new packaging backend

---

## 5. Environment Constraints

| Constraint | Value | Evidence |
|------------|-------|----------|
| **Python** | 3.10.6 (CI), py39 target (ruff) | `run_tests.yaml:17`, `pyproject.toml` |
| **Node** | 18 (CI) | `on_pull_request.yaml:35` |
| **Ruff** | 0.3.3 | `on_pull_request.yaml:23` |
| **Model/test-server** | Empty model; CPU path | `run_tests.yaml:--use-cpu all`, `--do-not-download-clip` |
| **Port** | 7860 | `cmd_args.py:78`, `ui.py:57` |
| **TORCH_INDEX_URL** | CPU wheel URL for CI | `run_tests.yaml:38` |

---

## 6. CI Constraints

| Workflow | Triggers | Condition | Blocking |
|----------|----------|-----------|----------|
| **Linter** | push, pull_request | Fork PRs only (head.repo != base.repo) | Yes |
| **Tests** | push, pull_request | Same condition | Yes |
| **warns_merge_master** | pull_request to master | Always | Yes (exit 1) |

**Fork behavior:** Lint and Tests run only when `github.event.pull_request.head.repo.full_name != github.event.pull_request.base.repo.full_name` — i.e., when PR is from a fork. Same-repo PRs skip these jobs.

**Secrets:** No explicit secrets required for baseline lint/tests. Models cached with key `2023-12-30`.

---

## 7. Gaps Identified by Audit

- No test tiers (smoke / quality / nightly)
- No coverage threshold
- `package-lock.json` gitignored; CI uses `npm i --ci` not `npm ci`
- Actions use tags (`@v4`, `@v5`) not SHA
- No pip-audit or npm audit in CI
- No CONTRIBUTING.md
- No health endpoint for smoke

---

## 8. Repo Layout (Key Paths)

```
.
├── launch.py
├── webui.py
├── modules/
│   ├── shared.py          # Global state hub
│   ├── processing.py      # Core pipeline
│   ├── ui.py
│   ├── api/
│   ├── launch_utils.py
│   ├── initialize.py
│   └── ...
├── test/
│   ├── conftest.py
│   ├── test_txt2img.py
│   ├── test_img2img.py
│   └── ...
├── extensions-builtin/
├── scripts/
├── .github/workflows/
│   ├── on_pull_request.yaml
│   ├── run_tests.yaml
│   └── warns_merge_master.yml
├── pyproject.toml
├── package.json
└── requirements*.txt
```
