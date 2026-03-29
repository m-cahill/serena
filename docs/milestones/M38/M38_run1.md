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

**Latest recorded `pull_request` CI** (SHA `a1f09c898fa4528277e24a2ef0b07593cff68879` — matches `gh api repos/m-cahill/serena/pulls/94 --jq .head.sha` at last update and `gh run view` for the runs below; doc-only commits advance the tip — if `head.sha` is newer, use `pull_request` Linter + Smoke on the **current** head):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23699940461** | `pull_request` | `a1f09c898fa4528277e24a2ef0b07593cff68879` | **success** |
| **Smoke Tests** | **23699940451** | `pull_request` | `a1f09c898fa4528277e24a2ef0b07593cff68879` | **success** |

Mirror `push` on same SHA: Linter **23699939865**, Smoke **23699939863** — both **success**.

Prior tip `8a6f76e32f5436b900f88fb917ff2e36fd0267b0`: PR Linter **23699866190**, Smoke **23699866183** — both **success** (`pull_request`); mirror `push` Linter **23699865557**, Smoke **23699865562** — both **success**.

Earlier doc-only / branch tips (`2e5086f3`, `90ee0de8`, `a300c4e8`, `3b44969a`, …) and **576b3935** (refactor baseline, §A) also had green `pull_request` + mirror `push` runs recorded in git history of this file.

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
