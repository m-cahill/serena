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

**Latest recorded `pull_request` CI** (SHA `5e053285f91eeabfc0a6c148efb620e59554c823` — matches `gh run view` for the runs below):

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23698616974** | `pull_request` | `5e053285f91eeabfc0a6c148efb620e59554c823` | **success** |
| **Smoke Tests** | **23698616976** | `pull_request` | `5e053285f91eeabfc0a6c148efb620e59554c823` | **success** |

Mirror `push` on same SHA: Linter **23698616147**, Smoke **23698616157** — both **success**.

Prior tip `46018d97…`: PR Linter **23698561600**, Smoke **23698561608** — both **success** (`pull_request`). Prior `2aa1cf5b…`: PR Linter **23698509169**, Smoke **23698509175** — both **success** (`pull_request`). Prior `c4354ac2…`: PR Linter **23698454870**, Smoke **23698454876** — both **success** (`pull_request`). Prior `6231f451…`: PR Linter **23698406739**, Smoke **23698406734** — both **success** (`pull_request`). Prior `4f92a13a…`: PR Linter **23698353286**, Smoke **23698353269** — both **success** (`pull_request`). Prior `fad8feb2…`: PR Linter **23698299956**, Smoke **23698299955** — both **success** (`pull_request`). Prior `1febb8b9…`: PR Linter **23698245812**, Smoke **23698245823** — both **success** (`pull_request`). Prior `9f2dda8e…`: PR Linter **23698184743**, Smoke **23698184745** — both **success** (`pull_request`). Prior `eb0ee547…`: PR Linter **23698120117**, Smoke **23698120120** — both **success** (`pull_request`). Prior `89e4ffd7…`: PR Linter **23698066410**, Smoke **23698066388** — both **success** (`pull_request`). Prior `7c4f5e0c…`: PR Linter **23698010765**, Smoke **23698010777** — both **success** (`pull_request`).

If this file is updated again on the branch, re-check `gh pr view` / `gh run list` for the latest `pull_request` Linter + Smoke on the PR head.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

Earlier intermediate tips (e.g. `fabd3aa1…`, `91a51bb0…`) also had green `pull_request` Linter + Smoke; **576b3935** remains the refactor-only baseline in §A.

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
