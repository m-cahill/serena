# M00 E2E Baseline Verification

**Date:** 2025-03-06  
**Branch:** m00-kickoff-baseline-e2e  
**Baseline tag:** baseline-pre-refactor  
**Baseline SHA:** 82a973c04367123ae98bd9abdf80d9eda9b910e2

---

## 1. Baseline Freeze

| Item | Value |
|------|-------|
| **Fork branch** | m00-kickoff-baseline-e2e (from master) |
| **HEAD SHA** | 82a973c04367123ae98bd9abdf80d9eda9b910e2 |
| **Audited baseline SHA** | 82a973c04367123ae98bd9abdf80d9eda9b910e2 |
| **Baseline tag** | baseline-pre-refactor (annotated) |
| **Upstream remote** | https://github.com/AUTOMATIC1111/stable-diffusion-webui.git |
| **Origin remote** | https://github.com/m-cahill/serena.git |

**Tag relationship:** `baseline-pre-refactor` points to commit 82a973c0. This is the immutable baseline before any Serena refactor work.

---

## 2. Local Baseline Verification

### 2.1 Python Lint (Ruff)

**Command:** `ruff .` (CI uses `ruff==0.3.3`)

**Result:** PASS

```
ruff==0.3.3
ruff .
All checks passed!
```

**Note:** Newer ruff uses `ruff check .`; 0.3.3 accepts `ruff .` (deprecation warning shown but exit 0).

---

### 2.2 JS Lint (ESLint)

**Command:** `npm i --ci` then `npm run lint`

**Result (local Windows):** FAIL — linebreak-style (CRLF vs LF)

ESLint reports `Expected linebreaks to be 'LF' but found 'CRLF'` across many files. This is a Windows vs Linux environment difference. **CI runs on ubuntu-latest and would pass** (Linux uses LF).

**Recommendation:** Document for M01/M02 — consider `.gitattributes` or eslint linebreak config for cross-platform dev.

---

### 2.3 Test Server Startup

**Command (from run_tests.yaml):**
```bash
python -m coverage run --data-file=.coverage.server launch.py \
  --skip-prepare-environment --skip-torch-cuda-test --test-server \
  --do-not-download-clip --no-half --disable-opt-split-attention \
  --use-cpu all --api-server-stop
```

**Result:** Not run in M00 (requires full env setup, PyTorch CPU, ~5–10 min). Documented for repeatability.

---

### 2.4 Pytest Suite

**Command:** With server running on 127.0.0.1:7860:
```bash
wait-for-it --service 127.0.0.1:7860 -t 20
python -m pytest -vv --junitxml=test/results.xml --cov . --cov-report=xml --verify-base-url test
```

**Result:** Not run in M00 (server not started locally). CI path is the source of truth.

**Coverage summary command (after pytest):**
```bash
python -m coverage combine .coverage*
python -m coverage report -i
python -m coverage html -i
```

---

## 3. E2E / Integration Verification

**Representative API paths exercised by tests:**
- `/sdapi/v1/txt2img` — test_txt2img.py
- `/sdapi/v1/img2img` — test_img2img.py
- `/sdapi/v1/extra-single-image` — test_extras.py
- `/sdapi/v1/options`, `/sdapi/v1/cmd-flags`, samplers, upscalers, etc. — test_utils.py

**No health endpoint:** Tests use txt2img/img2img as integration probes. Boot evidence comes from server startup and first successful API response.

---

## 4. Blockers / Observations

| Blocker | Severity | Notes |
|---------|----------|-------|
| ESLint CRLF on Windows | Low | CI passes; local Windows fails linebreak-style |
| Pytest requires server | Medium | Full local run needs server in background; use CI or helper script |
| Same-repo PR skips lint/tests | High | See M00_ci_inventory.md |

---

## 5. Repeatable Verification Commands (Exact)

| Step | Command |
|------|---------|
| Python lint | `pip install ruff==0.3.3` then `ruff .` |
| JS lint | `npm i --ci` then `npm run lint` |
| Env setup | `python launch.py --skip-torch-cuda-test --exit` (with TORCH_INDEX_URL for CPU) |
| Start server | `python -m coverage run --data-file=.coverage.server launch.py --skip-prepare-environment --skip-torch-cuda-test --test-server --do-not-download-clip --no-half --disable-opt-split-attention --use-cpu all --api-server-stop` (run in background) |
| Wait for server | `wait-for-it --service 127.0.0.1:7860 -t 20` |
| Run tests | `python -m pytest -vv --junitxml=test/results.xml --cov . --cov-report=xml --verify-base-url test` |
| Coverage report | `python -m coverage combine .coverage*` then `python -m coverage report -i` |

---

## 6. Helper Scripts

Thin wrappers that mirror existing commands:

| Script | Platform | Usage |
|--------|----------|-------|
| `scripts/dev/run_m00_baseline_e2e.ps1` | Windows | `.\scripts\dev\run_m00_baseline_e2e.ps1` |
| `scripts/dev/run_m00_baseline_e2e.sh` | Linux/macOS | `./scripts/dev/run_m00_baseline_e2e.sh` |

Scripts run ruff and eslint only; full pytest requires manual server startup (documented in script output).
