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

**Latest recorded `pull_request` CI** (SHA `0aea272e9bdaa6a9da641fe8551bac73b4445d9d` — matches current `gh pr view` `headRefOid` and `gh run view` for the runs below):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23699064284** | `pull_request` | `0aea272e9bdaa6a9da641fe8551bac73b4445d9d` | **success** |
| **Smoke Tests** | **23699064282** | `pull_request` | `0aea272e9bdaa6a9da641fe8551bac73b4445d9d` | **success** |

Mirror `push` on same SHA: Linter **23699063803**, Smoke **23699063800** — both **success**.

Prior tip `00ed3400a338bafc7ed0ad39167efc8e7046681c` (doc-only predecessor): PR Linter **23699009746**, Smoke **23699009747** — both **success** (`pull_request`); mirror `push` Linter **23699009218**, Smoke **23699009223** — both **success**. Earlier branch tips had additional green `pull_request` runs; **576b3935** remains the refactor-only baseline in §A.

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
