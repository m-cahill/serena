# M38 — CI run record 1 (PR)

**Milestone:** M38 — `processing.py` class and helper decomposition  
**PR:** https://github.com/m-cahill/serena/pull/94  
**Branch:** `m38-processing-class-helper-decomposition`

## Local vs CI

Local `pytest` was **not** used as binding proof for M38 (incomplete local dependency set, e.g. `einops` / `cv2` in some environments). **GitHub Actions** on this PR is the authoritative verification surface for Linter + Smoke.

---

## A. Refactor-only tip (merge-critical code)

**Commit:** `576b39354003aa3bc7a3b41cc38564c654b7b671`  
**Message:** `refactor(M38): split processing classes into processing_types/helpers/infotext`

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23697815570** | `pull_request` | `576b39354003aa3bc7a3b41cc38564c654b7b671` | **success** |
| **Smoke Tests** | **23697815572** | `pull_request` | `576b39354003aa3bc7a3b41cc38564c654b7b671` | **success** |

Mirror `push` on same SHA: Linter **23697806689**, Smoke **23697806695** — both **success**.

---

## B. Current PR tip (authoritative for merge)

Before merging, confirm the PR head with `gh pr view 94 --repo m-cahill/serena --json headRefOid` and ensure the latest `pull_request` **Linter** + **Smoke Tests** on that OID are **success** (GitHub also runs duplicate `push` workflows on the branch; prefer `pull_request` for PR evidence).

**Latest recorded `pull_request` CI** (SHA `2e5086f3415023d6eda3c5e41cc23babd0d8abda` — matches `gh api repos/m-cahill/serena/pulls/94 --jq .head.sha` and `gh run view` for the runs below; if another commit lands after this, re-check head and runs):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23699620246** | `pull_request` | `2e5086f3415023d6eda3c5e41cc23babd0d8abda` | **success** |
| **Smoke Tests** | **23699620252** | `pull_request` | `2e5086f3415023d6eda3c5e41cc23babd0d8abda` | **success** |

Mirror `push` on same SHA: Linter **23699619533**, Smoke **23699619537** — both **success**.

Prior tip `90ee0de8cc5b5e259f2f708ced63a0ebbb786f7e` (predecessor to the doc sync above): PR Linter **23699547587**, Smoke **23699547601** — both **success** (`pull_request`); mirror `push` Linter **23699546546**, Smoke **23699546528** — both **success**.

Earlier doc-only / branch tips (`a300c4e8`, `3b44969a`, …) and **576b3935** (refactor baseline, §A) also had green `pull_request` + mirror `push` runs recorded in git history of this file.

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
