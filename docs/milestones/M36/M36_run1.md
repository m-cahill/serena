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

### Implementation commit (tests-only)

**Head SHA:** **`75356919e7e7dc3dd0b6ed5df5f17b7ae82440a1`** (`test(M36): provider/orchestration seams…`). Validated via `gh run view <id> --json headSha`.

| Role | Workflow | Run ID | Result | `headSha` | Event |
|------|----------|--------|--------|-----------|--------|
| **PR gate** | **Linter** | **`23676605494`** | **success** | **`75356919e7e7dc3dd0b6ed5df5f17b7ae82440a1`** | `pull_request` |
| **PR gate** | **Smoke Tests** | **`23676605498`** | **success** | **`75356919e7e7dc3dd0b6ed5df5f17b7ae82440a1`** | `pull_request` |

**Duplicate `push` (same tip, non-gating):** Linter **`23676596052`**, Smoke **`23676596056`** — both **success**.

### Current PR tip (includes `M36_run1` CI evidence)

**Head SHA:** **`151f42e3c9cf6f48f50794724bea34f157454e55`** (`docs(M36): M36_run1 — PR #92…`).

| Role | Workflow | Run ID | Result | `headSha` | Event |
|------|----------|--------|--------|-----------|--------|
| **PR gate** | **Linter** | **`23676686946`** | **success** | **`151f42e3c9cf6f48f50794724bea34f157454e55`** | `pull_request` |
| **PR gate** | **Smoke Tests** | **`23676686942`** | **success** | **`151f42e3c9cf6f48f50794724bea34f157454e55`** | `pull_request` |

**Duplicate `push` (doc commit tip):** Linter **`23676685985`**, Smoke **`23676685991`** — both **success**.

### Latest branch tip (current PR `head`; doc commit `e70d282a`)

**Head SHA:** **`e70d282ae0eb25811a30104f8c4b702e13351982`**

| Role | Workflow | Run ID | Result | `headSha` | Event |
|------|----------|--------|--------|-----------|--------|
| **PR gate** | **Linter** | **`23676841052`** | **success** | **`e70d282ae0eb25811a30104f8c4b702e13351982`** | `pull_request` |
| **PR gate** | **Smoke Tests** | **`23676841058`** | **success** | **`e70d282ae0eb25811a30104f8c4b702e13351982`** | `pull_request` |

**Duplicate `push`:** Linter **`23676840473`**, Smoke **`23676840475`** — both **success**.

**Failed / superseded:** none observed for the tips recorded above.

---

## Post-merge `main` Quality (binding “after”)

*(Fill after merge: run ID, tests passed, TOTAL coverage, final `--fail-under` if changed.)*

---

## Gate decision

**Undecided in this PR phase.** `--fail-under` remains **42%** until post-merge **Quality Tests** on **`main`** reports measured TOTAL coverage and a safe margin for any threshold bump (see `M36_plan.md`).
