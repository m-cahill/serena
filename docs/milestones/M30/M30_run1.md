# M30 — Evidence inventory and cross-check (run 1)

**Milestone:** M30 — QA / evidence publishing  
**Mode:** Selective deep verification (M26–M29); earlier milestones per `docs/serena.md` unless doubt arises  
**Date (UTC):** 2026-03-26

---

## 1. Scope

| Source | Use |
|--------|-----|
| `docs/serena.md` | Primary ledger spine for M00–M25 and program narrative |
| `docs/milestones/M26`–`M29` | Direct verification of `run1` / `summary` / `audit` vs ledger |

---

## 2. M26–M29 alignment (verified)

| Milestone | Merge / anchor (ledger) | Binding Quality | Audit | Key artifact(s) | Match |
|-----------|-------------------------|-----------------|-------|-------------------|-------|
| **M26** | `67692434` @ Quality **23467772232** | [23467772232](https://github.com/m-cahill/serena/actions/runs/23467772232) | 5.0 / 5 (`M26_audit.md`) | `pip_freeze.txt`, `dependency_snapshot.txt`, `ci_environment.txt`, `pip_audit_report.txt` | OK — matches `M26_run1.md`, `M26_summary.md` |
| **M27** | `e3c0d554` @ Quality **23513449859** | [23513449859](https://github.com/m-cahill/serena/actions/runs/23513449859) | 5.0 / 5 (`M27_audit.md`) | `radon-report`, pytest-only coverage report | OK — matches `M27_run1.md`, `M27_summary.md` |
| **M28** | Topic finalize `f88e1e9c` (see §3) | **No isolated green `main` run** (see §3) | 5.0 / 5 (`M28_audit.md`) | `M28_run1.md` batches; deferrals in `ci_environment_contract.md` | OK — narrative clarified in §3; ledger updated |
| **M29** | `1b2e2f69` @ Quality **23618918747** | [23618918747](https://github.com/m-cahill/serena/actions/runs/23618918747) | 5.0 / 5 (`M29_audit.md`) | `performance_snapshot.txt` (artifact **performance-snapshot**) | OK — matches `M29_run1.md` (binding section), `M29_summary.md` |

**Internal consistency (M29):** `M29_run1.md` documents an earlier **BLOCKED** period and recovery; final binding **23618918747** agrees with `M29_summary.md`, `M29_audit.md`, and `docs/serena.md`. No contradiction in **final** claims.

---

## 3. M28 — Quality run ID and `main` history (correction)

**Issue:** Ledger listed **Quality TBD** for M28; `M28_run1.md` still had a placeholder line for “first green Quality” on the closing commit.

**Finding (factual):**

1. **PR [#64](https://github.com/m-cahill/serena/pull/64)** squash-merged M28 work (M28a/M28b), M28 finalize commits (**`f88e1e9c`**, tag peel **`c97c406`**, etc.), and M29 feature work into **`main`** as **`f18b73f2`**. Topic-branch SHAs **`f88e1e9c`** / **`c97c406`** are **not** first-parent ancestors of current **`main`** (they exist on **`m28-security-supply-chain`** history).
2. The **first** Quality workflow on **`main`** after that squash was **[23566817312](https://github.com/m-cahill/serena/actions/runs/23566817312)** — **failure** (M29 follow-up chain began here).
3. Therefore there is **no** GitHub Actions run ID that represents “M28 alone green on **`main`**.” Supply-chain policy and dependency graph are **subsequently** validated by the **binding** post-recovery run **23618918747** (M29.2), which exercises the same locked manifest and **blocking `pip-audit`** policy.

**Applied corrections:**

- `docs/serena.md` — M28 row: replaced **TBD** with explicit explanation + pointer to binding stack proof **23618918747**; set PR **#64** where ledger had **?**.
- `docs/milestones/M28/M28_run1.md` — replaced placeholder with short **Quality run ID** subsection (this finding).
- `docs/milestones/M28/M28_summary.md` — removed “append Quality run ID” instruction; replaced with cross-reference to `M30_run1.md` §3.

---

## 4. Optional checks performed

- **`gh run list`** on `m-cahill/serena` for `run_quality_tests.yaml` — confirmed **23618918747** / **23513449859** / **23467772232** and absence of a **`main`** success run solely for **`f88e1e9c`** / **`c97c406`**.
- **`git merge-base --is-ancestor`** — confirmed **`f88e1e9c`** not on current **`main`** first-parent line (explains tag/branch vs squash).

---

## 5. M30 evidence record (ledger / PR)

| Item | Value |
|------|--------|
| Milestone | M30 |
| **PR** | **[#82](https://github.com/m-cahill/serena/pull/82)** — `M30: QA / evidence publishing` |
| Branch pushed | `m30-qa-evidence-publishing` → `origin` |
| Merge commit (`main`) | *Fill after merge* |
| **Binding CI for M30** | **N/A** — documentation-only milestone; no code-path or Quality gate required for M30 closeout |
| Audit target | 5.0 / 5 (`M30_audit.md`) |
| Key artifact(s) | `serena_evidence_bundle.md`, `serena_case_study_summary.md`, `serena_evidence_matrix.md`, this file, `M30_summary.md`, `M30_audit.md`, updated `docs/serena.md` |

---

## 6. PR #82 checks — provenance only

These results are **PR hygiene** (eslint / ruff / smoke). They are **not** claimed as a “binding” M30 proof surface; M30 remains **doc-only**.

| Check | Result | Representative workflow run(s) |
|-------|--------|--------------------------------|
| **eslint** | **pass** | Jobs under [23620057974](https://github.com/m-cahill/serena/actions/runs/23620057974), [23620061075](https://github.com/m-cahill/serena/actions/runs/23620061075) |
| **ruff** | **pass** | Same workflow runs as eslint (paired jobs) |
| **smoke tests** | **pass** | e.g. [23620057948](https://github.com/m-cahill/serena/actions/runs/23620057948) (~2m52s), [23620061105](https://github.com/m-cahill/serena/actions/runs/23620061105) (~3m7s) |

*GitHub may show duplicate check rows for the same PR (multiple workflow runs); all completed **pass**.*

---

## 7. Post-merge (fill after merge to `main`)

| Item | Value |
|------|--------|
| Merge commit | *TBD* |
| Post-merge workflows on `main` | *Optional provenance only — e.g. if Quality runs on push; not required for M30* |
| Annotated tag | `v0.0.30-m30` — *create/push after merge* |
