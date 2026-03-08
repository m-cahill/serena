# M01 CI Run 2 — Analysis

**Date:** 2025-03-07  
**Branch:** m01-ci-truthfulness  
**Trigger:** Skip prepare-environment (31588a1e)

---

## 1. Workflow Identity

| Workflow | Run ID | Status |
|----------|--------|--------|
| Linter | 22809961294 | ✓ success |
| Tests | 22809961290 | ✗ failure |

---

## 2. Result

**Setup environment** and **Smoke startup** passed (--exit handling works).

**Start test server** step completed (process launched in background).

**Run tests** failed: wait-for-it timed out (server never bound to 7860).

---

## 3. Root Cause

From output.txt artifact:

```
ModuleNotFoundError: No module named 'torch'
```

With `--skip-prepare-environment`, we never run `prepare_environment()`, so torch/clip/requirements were never installed.

---

## 4. Fix Applied

Added **Install runtime dependencies** step (commit 69637193):

- pip install torch, torchvision (CPU)
- pip install CLIP (--no-build-isolation)
- pip install open_clip
- pip install -r requirements_versions.txt

---

## 5. Remaining Blocker

`paths.py` asserts `sd_path` exists (repositories/stable-diffusion-stability-ai). The app requires the `repositories/` folder. With `--skip-prepare-environment`, we never clone. Repositories must come from **cache**. Cache key `repos-2023-12-30` has never been populated (clone has not succeeded).

**Options to seed cache:**
- workflow_dispatch job with PAT for cross-org clone
- One-time local bootstrap + cache upload (if supported)
- Add repositories as submodules

---

## 6. Run 3 (69637193): Confirmed

**Error:** `AssertionError: Couldn't find Stable Diffusion in any of: [repositories/stable-diffusion-stability-ai, ...]`

Torch/clip/requirements now install correctly. The app requires `repositories/` (paths.py). Cache `repos-2023-12-30` is empty. Must be seeded for CI to pass.
