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

**PR head SHA:** `7c4f5e0cb4082571031d1b6b45e69a8a4f95c4a1`  
**Message:** `docs(M38): M38_run1.md — refactor SHA + current tip CI (PR #94)`  
Doc commits after **576b3935** add/update milestone docs; M38 code paths unchanged.

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23698010765** | `pull_request` | `7c4f5e0cb4082571031d1b6b45e69a8a4f95c4a1` | **success** |
| **Smoke Tests** | **23698010777** | `pull_request` | `7c4f5e0cb4082571031d1b6b45e69a8a4f95c4a1` | **success** |

Mirror `push` on same SHA: Linter **23698009971**, Smoke **23698009969** — both **success**.

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

Prior intermediate tips (e.g. `fabd3aa1…`, `91a51bb0…`) also had green `pull_request` Linter + Smoke; **576b3935** remains the refactor-only baseline in §A.

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
