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

Before merging, confirm the PR head with `gh api repos/m-cahill/serena/pulls/94 --jq .head.sha` (often fresher than `gh pr view` JSON right after a push) and ensure the latest `pull_request` **Linter** + **Smoke Tests** on that OID are **success** (GitHub also runs duplicate `push` workflows on the branch; prefer `pull_request` for PR evidence).

**Latest recorded `pull_request` CI** (SHA `f02f8d0e91f8ec6c22cd0c14aba80bae601af371` — matches `gh api repos/m-cahill/serena/pulls/94 --jq .head.sha` at last validation and `gh run view` for the runs below; doc-only commits advance the tip — if `head.sha` is newer, use `pull_request` Linter + Smoke on the **current** head):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23700206099** | `pull_request` | `f02f8d0e91f8ec6c22cd0c14aba80bae601af371` | **success** |
| **Smoke Tests** | **23700206121** | `pull_request` | `f02f8d0e91f8ec6c22cd0c14aba80bae601af371` | **success** |

Mirror `push` on same SHA: Linter **23700205196** — **success**; Smoke **23700205201** — **failure** (duplicate branch `push` run; prefer `pull_request` rows above for PR merge checks).

Prior tip `bee324e73a37e36a30616b67ca5e2f1a5c1aa2ee`: PR Linter **23700088809**, Smoke **23700088819** — both **success** (`pull_request`); mirror `push` Linter **23700088026**, Smoke **23700088032** — both **success**.

Earlier doc-only / branch tips (`8d53aa83`, `a1f09c89`, …) and **576b3935** (refactor baseline, §A) also had green `pull_request` + mirror `push` runs recorded in git history of this file.

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
