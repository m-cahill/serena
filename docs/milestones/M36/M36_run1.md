# M36 — Run 1 (CI)

**Milestone:** M36 — Coverage lift and gate recalibration  
**Branch:** `m36-coverage-lift-gate-recalibration`  
**PR:** https://github.com/m-cahill/serena/pull/92  

---

## Baseline (“before”) — authoritative

From M35 post-merge Quality (ledger binding):

| Field | Value |
|-------|--------|
| Quality run ID | **`23673838908`** |
| `main` merge (M35) | **`45e6f4fbfb8f6ed2dfc336423d1f414f66c77549`** |
| Tests passed | **203** |
| TOTAL coverage (log) | **~48%** |
| Coverage gate | **42%** (`--fail-under=42`) |

---

## PR CI (Linter + Smoke) — authoritative `pull_request` gates

**PR head at approval snapshot:** **`75356919e7e7dc3dd0b6ed5df5f17b7ae82440a1`** (M36 implementation commit; validated via `gh run view <id> --json headSha`).

| Role | Workflow | Run ID | Result | `headSha` | Event |
|------|----------|--------|--------|-----------|--------|
| **PR gate** | **Linter** | **`23676605494`** | **success** | **`75356919e7e7dc3dd0b6ed5df5f17b7ae82440a1`** | `pull_request` |
| **PR gate** | **Smoke Tests** | **`23676605498`** | **success** | **`75356919e7e7dc3dd0b6ed5df5f17b7ae82440a1`** | `pull_request` |

**Duplicate / non-gating runs (same branch tip):** `push` on `m36-coverage-lift-gate-recalibration` also triggered Linter **`23676596052`** and Smoke Tests **`23676596056`** (both **success**, same **`75356919…`**). Per Serena convention, **`pull_request`** runs are the merge-readiness checks; `push` duplicates are noted for provenance only.

**Failed / superseded:** none observed for the authoritative PR head above.

---

## Post-merge `main` Quality (binding “after”)

*(Fill after merge: run ID, tests passed, TOTAL coverage, final `--fail-under` if changed.)*

---

## Gate decision

**Undecided in this PR phase.** `--fail-under` remains **42%** until post-merge **Quality Tests** on **`main`** reports measured TOTAL coverage and a safe margin for any threshold bump (see `M36_plan.md`).
