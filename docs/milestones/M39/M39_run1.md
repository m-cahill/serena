# M39 — CI run record 1 (PR)

**Milestone:** M39 — Remaining legacy surface narrowing  
**PR:** https://github.com/m-cahill/serena/pull/95  
**Branch:** `m39-remaining-legacy-surface-narrowing`

## Local vs CI

Local `pytest` on `test/quality/test_m39_eff_opts_snapshot.py` was used for fast contract checks. **GitHub Actions** on the PR is the authoritative verification surface for Linter + Smoke.

---

## A. PR head (authoritative merge approval tip)

**Commit:** `d0bb6afa841272f9e7ec5c7e342c61a95a1a465f`  
**Message:** `docs(M39): authoritative PR tip fe2494fb (Linter 23719300652, Smoke 23719300655)` — follows **`eee9af2a`** (refactor) and doc closeout commits.

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23719373729** | `pull_request` | `d0bb6afa841272f9e7ec5c7e342c61a95a1a465f` | **success** |
| **Smoke Tests** | **23719373734** | `pull_request` | `d0bb6afa841272f9e7ec5c7e342c61a95a1a465f` | **success** |

**Superseded tips (historical):** `fe2494fb` — Linter **`23719300652`**, Smoke **`23719300655`**; `c83e14cd` — Linter **`23719231700`**, Smoke **`23719231692`**; `eee9af2a` — Linter **`23719147857`**, Smoke **`23719147871`**.

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
