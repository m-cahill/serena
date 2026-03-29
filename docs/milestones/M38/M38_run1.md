# M38 — CI run record 1 (PR)

**Milestone:** M38 — `processing.py` class and helper decomposition  
**PR:** https://github.com/m-cahill/serena/pull/94  
**Branch:** `m38-processing-class-helper-decomposition`  
**PR head SHA (authoritative, current tip):** `91a51bb0c54bcc8e2040ea5e247c8fd7938c993a`

Includes doc-only commit `docs(M38): M38_run1.md — PR #94 CI evidence` on top of refactor commit `576b39354003aa3bc7a3b41cc38564c654b7b671`. **Binding PR checks** below are for this tip.

## Local vs CI

Local `pytest` was **not** used as binding proof for M38 (incomplete local dependency set, e.g. `einops` / `cv2` in some environments). **GitHub Actions** on this PR is the authoritative verification surface for Linter + Smoke.

## PR checks (authoritative — `pull_request`, head `91a51bb0`)

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23697887173** | `pull_request` | `91a51bb0c54bcc8e2040ea5e247c8fd7938c993a` | **success** |
| **Smoke Tests** | **23697887187** | `pull_request` | `91a51bb0c54bcc8e2040ea5e247c8fd7938c993a` | **success** |

Validated via:

`gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`

## Superseded / earlier PR tip (`576b3935`)

The first push of the refactor (without `M38_run1.md`) produced green **`pull_request`** runs **23697815570** (Linter) and **23697815572** (Smoke) at `headSha` `576b39354003aa3bc7a3b41cc38564c654b7b671`. Superseded after doc commit; kept for provenance only.

## Duplicate / mirror runs (same tip `91a51bb0`, `push` event)

| Workflow | Run ID | Event | Conclusion |
|----------|--------|-------|------------|
| Linter | 23697886773 | `push` | success |
| Smoke Tests | 23697886781 | `push` | success |

**Authoritative PR gate:** use the **`pull_request`** runs (**23697887173**, **23697887187**).

## Post-merge `main` (Quality)

**Placeholder — not run yet.** After merge to `main`, record the binding **Quality Tests** workflow run ID and conclusion from `push` to `main` (workflow: `run_quality_tests.yaml`).

---

**Status:** PR open — **do not merge** until explicit approval (per program gates).
