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

## B. Current PR tip (includes milestone docs on branch)

**PR head SHA (latest at record time):** `fabd3aa16802af45f6767737016616968204c1ac`  
Doc-only commits after **576b3935** add/update `M38_run1.md` under `docs/milestones/M38/`; behavior unchanged.

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23697956447** | `pull_request` | `fabd3aa16802af45f6767737016616968204c1ac` | **success** |
| **Smoke Tests** | **23697956455** | `pull_request` | `fabd3aa16802af45f6767737016616968204c1ac` | **success** |

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

Intermediate tip `91a51bb0` (first `M38_run1.md` add): **23697887173** (Linter), **23697887187** (Smoke) — both **success** (`pull_request`).

---

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
