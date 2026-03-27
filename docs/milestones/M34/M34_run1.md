# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (validated)** | **`65aa7219ddd25c9f968b12a336df427129a563a1`** |
| **Head commit** | `docs(M34): record PR #90 in ledger and run1` |

All workflow evidence below is tied to this SHA (GitHub **headSha** on each run).

---

## CI (PR) — primary evidence

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23628995102`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23628995102 |
| **Result** | **success** |
| **headSha** | `65aa7219ddd25c9f968b12a336df427129a563a1` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68823971656` | success |
| ruff | `68823971649` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23628995101`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23628995101 |
| **Result** | **success** |
| **headSha** | `65aa7219ddd25c9f968b12a336df427129a563a1` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68823971659` | success |

---

## Duplicate workflow runs (same head SHA, no failures)

GitHub also recorded a **second** Linter run and **second** Smoke run for the **same** `pull_request` event / same **head SHA** `65aa7219` (duplicate triggers). **All conclusions success** — no superseded failed run for this head.

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23628993965` | https://github.com/m-cahill/serena/actions/runs/23628993965 | success | `65aa7219ddd25c9f968b12a336df427129a563a1` |
| Smoke Tests | `23628993960` | https://github.com/m-cahill/serena/actions/runs/23628993960 | success | `65aa7219ddd25c9f968b12a336df427129a563a1` |

**Authoritative documentation:** Primary table above uses runs **`23628995102`** (Linter) and **`23628995101`** (Smoke); alternate IDs are corroborating duplicates only.

---

## PR merge

| Field | Value |
|-------|--------|
| Merge commit | *(pending approval — not merged)* |

---

## CI (`main`, post-merge)

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter | *(post-merge)* | | |
| Quality | *(post-merge)* | | pytest coverage gate unchanged |

---

## Verdict (PR CI)

**PR CI on head `65aa7219ddd25c9f968b12a336df427129a563a1`:** **Linter** and **Smoke Tests** **green** (see primary runs above). **Quality** on `main` is **out of scope** until merge.
