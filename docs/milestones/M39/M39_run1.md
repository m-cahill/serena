# M39 — CI run record 1 (PR)

**Milestone:** M39 — Remaining legacy surface narrowing  
**PR:** https://github.com/m-cahill/serena/pull/95  
**Branch:** `m39-remaining-legacy-surface-narrowing`

## Local vs CI

Local `pytest` on `test/quality/test_m39_eff_opts_snapshot.py` was used for fast contract checks. **GitHub Actions** on the PR is the authoritative verification surface for Linter + Smoke.

---

## A. PR head (merge-ready — includes doc closeout)

**Commit:** `c83e14cda42d4f33fe0603bedb9fbbc0dec4d9d2`  
**Tip message:** `docs(M39): run1 summary audit ledger M40 stubs; serena PR #95 CI` (follows **`eee9af2a`** — `refactor(M39): route supported-path opts reads via _eff_opts`)

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23719231700** | `pull_request` | `c83e14cda42d4f33fe0603bedb9fbbc0dec4d9d2` | **success** |
| **Smoke Tests** | **23719231692** | `pull_request` | `c83e14cda42d4f33fe0603bedb9fbbc0dec4d9d2` | **success** |

**Earlier code-only tip (superseded for merge approval):** `eee9af2a` — Linter **`23719147857`**, Smoke **`23719147871`**.

Validated via `gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`.

---

## B. Post-merge `main` (Linter + Quality)

**Pending merge.** After PR **#95** merges to **`main`**, record here:

| Workflow | Run ID | Event | Conclusion |
|----------|--------|-------|------------|
| **Linter** | *(fill after merge)* | `push` | |
| **Quality Tests** | *(fill after merge)* | `push` | |

**Quality (expected):** test count and **TOTAL** coverage should remain at or above M38 (**217** pass, **48%** cov band); gate **42%** unchanged.

---

## C. Implementation note

- **`_eff_opts(p)`** in **`modules/processing_helpers.py`** prefers **`p.opts_snapshot`** when set (after **`process_images_inner`** snapshot line); otherwise **`shared.opts`**.
- **Eliminated** direct **`shared.opts`** reads in **`processing_types.py`**, **`processing_infotext.py`**, **`processing.py`** (overlay branch), **`processing_runtime.py`** (preview gate). **`processing.py`** still calls **`create_opts_snapshot(shared.opts)`** — intentional capture point (M07).
