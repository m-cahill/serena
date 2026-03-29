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

**Latest recorded `pull_request` CI** (SHA `511c105c6cc596df921b526f16a319e711536663` — matches current PR head from `gh api repos/m-cahill/serena/pulls/94 --jq .head.sha` and `gh run view` for the runs below):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23699275425** | `pull_request` | `511c105c6cc596df921b526f16a319e711536663` | **success** |
| **Smoke Tests** | **23699275432** | `pull_request` | `511c105c6cc596df921b526f16a319e711536663` | **success** |

Mirror `push` on same SHA: Linter **23699274552**, Smoke **23699274551** — both **success**.

Prior tip `c809a3d9267974bf7f5b87e02752990ac41ee1bf` (doc-only predecessor): PR Linter **23699222829**, Smoke **23699222842** — both **success** (`pull_request`); mirror `push` Linter **23699222033**, Smoke **23699222035** — both **success**. Earlier branch tips had additional green `pull_request` runs; **576b3935** remains the refactor-only baseline in §A.

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
