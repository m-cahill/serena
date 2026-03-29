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

**Latest recorded `pull_request` CI** (SHA `90ee0de8cc5b5e259f2f708ced63a0ebbb786f7e` — matches `gh api repos/m-cahill/serena/pulls/94 --jq .head.sha` and `gh run view` for the runs below; if another commit lands after this, re-check head and runs):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23699547587** | `pull_request` | `90ee0de8cc5b5e259f2f708ced63a0ebbb786f7e` | **success** |
| **Smoke Tests** | **23699547601** | `pull_request` | `90ee0de8cc5b5e259f2f708ced63a0ebbb786f7e` | **success** |

Mirror `push` on same SHA: Linter **23699546546**, Smoke **23699546528** — both **success**.

Prior tip `a300c4e83ce66e18c1ebf0f5afc04d9b9642ee01` (doc-only predecessor): PR Linter **23699493619**, Smoke **23699493626** — both **success** (`pull_request`); mirror `push` Linter **23699492917**, Smoke **23699492923** — both **success**.

Prior tip `3b44969a217ec19c0bd7a236ae05264db1815932`: PR Linter **23699427747**, Smoke **23699427751** — both **success** (`pull_request`); mirror `push` Linter **23699426993**, Smoke **23699426991** — both **success**. Earlier branch tips had additional green `pull_request` runs; **576b3935** remains the refactor-only baseline in §A.

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
