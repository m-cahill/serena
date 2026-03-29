# M38 — CI run record 1 (PR)

**Milestone:** M38 — `processing.py` class and helper decomposition  
**PR:** https://github.com/m-cahill/serena/pull/94  
**Branch:** `m38-processing-class-helper-decomposition`  
**PR head SHA (authoritative):** `576b39354003aa3bc7a3b41cc38564c654b7b671`

## Local vs CI

Local `pytest` was **not** used as binding proof for M38 (incomplete local dependency set, e.g. `einops` / `cv2` in some environments). **GitHub Actions** on this PR is the authoritative verification surface for Linter + Smoke.

## PR checks (authoritative)

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23697815570** | `pull_request` | `576b39354003aa3bc7a3b41cc38564c654b7b671` | **success** |
| **Smoke Tests** | **23697815572** | `pull_request` | `576b39354003aa3bc7a3b41cc38564c654b7b671` | **success** |

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

## Duplicate / mirror runs (same commit)

Pushing the branch also triggered workflows with `event: push` on the same head SHA (Smoke delivery path for feature branches per workflow design):

| Workflow | Run ID | Event | Conclusion |
|----------|--------|-------|------------|
| Linter | 23697806689 | `push` | success |
| Smoke Tests | 23697806695 | `push` | success |

**Authoritative PR gate:** use the **`pull_request`** runs above (**23697815570**, **23697815572**) for merge-readiness on the PR.

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (expected workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
