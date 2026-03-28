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

## PR head reconciliation (pre-merge)

GitHub **`gh pr view 92 --json headRefOid`** at merge time reported **`c410771fcc0b305015e51d0468f5f05b98e4796a`**, a **doc-only** tip **after** the last SHA block written in an earlier revision of this file (**`e70d282a…`**). **No** additional pre-merge doc commit was made solely to align the file; merge authority used the **green** `pull_request` checks on **`c410771f`**.

**Authoritative merge tip:** **`c410771fcc0b305015e51d0468f5f05b98e4796a`**

| Role | Workflow | Run ID | Result | `headSha` | Event |
|------|----------|--------|--------|-----------|--------|
| **PR gate** | **Linter** | **`23676919831`** | **success** | **`c410771fcc0b305015e51d0468f5f05b98e4796a`** | `pull_request` |
| **PR gate** | **Smoke Tests** | **`23676919933`** | **success** | **`c410771fcc0b305015e51d0468f5f05b98e4796a`** | `pull_request` |

**Earlier green PR tips (same PR, implementation / intermediate docs):** **`75356919…`**, **`151f42e3…`**, **`e70d282a…`** — see revision history; all **`pull_request`** Linter + Smoke **success** for those SHAs.

---

## Merge to `main`

| Field | Value |
|-------|--------|
| **Merge method** | GitHub **merge commit** (`gh pr merge 92 --merge`) |
| **Merge commit SHA** | **`ab4c4679397091ef8de2d46db3afadf3113a6979`** |
| **Merged at (GitHub)** | **2026-03-28T04:02:44Z** UTC |

**`main` tip** after merge matches merge commit **`ab4c4679…`**.

---

## Post-merge `main` CI (binding “after”)

Triggered by **`push`** to **`main`** for merge commit **`ab4c4679397091ef8de2d46db3afadf3113a6979`**.

| Check | Run ID | Result | `headSha` (workflow) |
|-------|--------|--------|----------------------|
| **Linter** | **`23677054517`** | **success** | **`ab4c4679397091ef8de2d46db3afadf3113a6979`** |
| **Quality Tests** | **`23677054515`** | **success** | **`ab4c4679397091ef8de2d46db3afadf3113a6979`** |

**Quality summary (run `23677054515`, log):** **213** tests passed; **TOTAL** coverage **48%**; **`coverage report --fail-under=42`** as configured in workflow (**`run_quality_tests.yaml`**). **No** workflow edit in M36.

---

## Gate decision

**Unchanged at 42%.** Post-merge measured TOTAL remains **~48%** (same band as M35); margin over the floor is **not** materially wider in a way that justifies raising **`--fail-under`** without risking brittle red-line behavior. Any future raise must follow a later milestone with measured headroom (see `M36_plan.md`).
