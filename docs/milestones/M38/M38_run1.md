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

**PR head SHA (binding):** `eb0ee54759399675bd0b7e207150f0f6c5f50cb6` — confirm with `gh pr view 94 --repo m-cahill/serena --json headRefOid` before merge.  
**Message:** `docs(M38): M38_run1 — authoritative PR head 89e4ffd7 + CI run IDs`  
Doc commits after **576b3935** add/update milestone docs; M38 code paths unchanged.

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23698120117** | `pull_request` | `eb0ee54759399675bd0b7e207150f0f6c5f50cb6` | **success** |
| **Smoke Tests** | **23698120120** | `pull_request` | `eb0ee54759399675bd0b7e207150f0f6c5f50cb6` | **success** |

Mirror `push` on same SHA: Linter **23698119419**, Smoke **23698119423** — both **success**.

Prior tip `89e4ffd7…`: PR Linter **23698066410**, Smoke **23698066388** — both **success** (`pull_request`). Prior `7c4f5e0c…`: PR Linter **23698010765**, Smoke **23698010777** — both **success** (`pull_request`).

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

Earlier intermediate tips (e.g. `fabd3aa1…`, `91a51bb0…`) also had green `pull_request` Linter + Smoke; **576b3935** remains the refactor-only baseline in §A.

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
