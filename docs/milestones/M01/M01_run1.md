# M01 CI Run 1 — Analysis

**Date:** 2025-03-07  
**Branch:** m01-ci-truthfulness  
**Trigger:** Initial M01 push (9b96c916)

---

## 1. Workflow Identity

| Workflow | Run ID | Trigger | Status | Duration |
|----------|--------|---------|--------|----------|
| Linter | 22809624913 | push | ✓ success | 18s |
| Tests | 22809624907 | push | ✗ failure | 47s |

---

## 2. Failure: CLIP pkg_resources

**Step:** Setup environment  
**Error:** `ModuleNotFoundError: No module named 'pkg_resources'` during CLIP wheel build

**Fix applied:** Add `--no-build-isolation` to clip pip install in `modules/launch_utils.py` (commit 9ae76265)

---

## 3. Run 2 (9ae76265): CLIP fixed, new failure

| Workflow | Run ID | Status |
|----------|--------|--------|
| Tests | 22809670597 | ✗ failure |

**Step:** Setup environment (after CLIP)  
**Error:** `fatal: could not read Username for 'https://github.com': No such device or address` when cloning `Stability-AI/stablediffusion`

**Fix applied:** Add GITHUB_TOKEN to repo URLs, cache repositories (commit 23575dc7)

---

## 4. Run 3 (23575dc7): GITHUB_TOKEN made it worse

**Error:** `remote: Repository not found` — GITHUB_TOKEN is scoped to current repo, cannot access Stability-AI.

**Reverted:** Token-based URLs. Using default URLs.

---

## 5. Current Blocker

Git clone of `Stability-AI/stablediffusion` fails:
- Without token: "could not read Username" (possible rate limit / credential helper)
- With token: "Repository not found" (token has no cross-org access)

**Note:** M00 never reached this step (failed at CLIP). This is a newly discovered CI gap. May require:
- Repositories cache from successful run
- Or alternative repo source (e.g. mirror, submodule)
