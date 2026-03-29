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

**PR head SHA:** `89e4ffd72780973f80747b99062cd9bac54f9767`  
**Message:** `docs(M38): M38_run1 — PR tip 7c4f5e0c Linter/Smoke (authoritative)`  
Doc commits after **576b3935** add/update milestone docs; M38 code paths unchanged.

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23698066410** | `pull_request` | `89e4ffd72780973f80747b99062cd9bac54f9767` | **success** |
| **Smoke Tests** | **23698066388** | `pull_request` | `89e4ffd72780973f80747b99062cd9bac54f9767` | **success** |

Mirror `push` on same SHA: Linter **23698065962**, Smoke **23698065964** — both **success**.

Prior tip `7c4f5e0c…` (doc update before §B alignment): PR Linter **23698010765**, Smoke **23698010777** — both **success** (`pull_request`).

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

Earlier intermediate tips (e.g. `fabd3aa1…`, `91a51bb0…`) also had green `pull_request` Linter + Smoke; **576b3935** remains the refactor-only baseline in §A.

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
