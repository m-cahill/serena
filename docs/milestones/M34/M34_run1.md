# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (CI green; `gh run view` headSha)** | **`9321a4412a6e952c2ccd97611a8982f77b82a8b8`** |
| **Head commit (for SHA above)** | `docs(M34): M34_run1 — record tip 77e565f5 Linter/Smoke runs` (`9321a441`) |
| **Linter (workflow run)** | **`23631662306`** — https://github.com/m-cahill/serena/actions/runs/23631662306 — **success** |
| **Smoke Tests (workflow run)** | **`23631662325`** — https://github.com/m-cahill/serena/actions/runs/23631662325 — **success** |

**Note:** **M34** runtime code is unchanged from **`7becd909`** / **`65aa7219`**; commits after that are **documentation / ledger** on this branch. Duplicate workflow runs for the same head: Linter **`23631661246`**, Smoke **`23631661241`** (both **success**, same **headSha**). **Detailed** tables for earlier tips are below for traceability.

---

## CI (PR) — primary evidence (head `1269c3f3`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23631342096`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23631342096 |
| **Result** | **success** |
| **headSha** | `1269c3f395fe51931a7faeb8bc9d9291d9499153` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68831107181` | success |
| ruff | `68831107164` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23631342094`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23631342094 |
| **Result** | **success** |
| **headSha** | `1269c3f395fe51931a7faeb8bc9d9291d9499153` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68831107161` | success |

---

## Duplicate workflow runs (same head `1269c3f3`, no failures)

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23631341419` | https://github.com/m-cahill/serena/actions/runs/23631341419 | success | `1269c3f395fe51931a7faeb8bc9d9291d9499153` |
| Smoke Tests | `23631341408` | https://github.com/m-cahill/serena/actions/runs/23631341408 | success | `1269c3f395fe51931a7faeb8bc9d9291d9499153` |

**Primary documentation:** **`23631342096`** (Linter) and **`23631342094`** (Smoke).

---

## Earlier PR tips (traceability; all green; no superseded failures)

### Head `01aa27f9`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23631114397` | https://github.com/m-cahill/serena/actions/runs/23631114397 | success | `01aa27f9c4786d37a82fd43478fcf5f87d5d1567` |
| Smoke Tests | `23631114399` | https://github.com/m-cahill/serena/actions/runs/23631114399 | success | `01aa27f9c4786d37a82fd43478fcf5f87d5d1567` |

Duplicates (same head, success): Linter `23631113346`, Smoke `23631113357`.

### Head `6a249f2c`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23631029429` | https://github.com/m-cahill/serena/actions/runs/23631029429 | success | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |
| Smoke Tests | `23631029475` | https://github.com/m-cahill/serena/actions/runs/23631029475 | success | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |

Duplicates (same head, success): Linter `23631028766`, Smoke `23631028775`.

### Head `65aa7219` — M34 implementation + first ledger line for PR #90

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23628995102` | https://github.com/m-cahill/serena/actions/runs/23628995102 | success | `65aa7219ddd25c9f968b12a336df427129a563a1` |
| Smoke Tests | `23628995101` | https://github.com/m-cahill/serena/actions/runs/23628995101 | success | `65aa7219ddd25c9f968b12a336df427129a563a1` |

Duplicates (same head, success): Linter `23628993965`, Smoke `23628993960`.

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

**Merge review:** **PR #90** tip **`9321a4412a6e952c2ccd97611a8982f77b82a8b8`** — **Linter** workflow **`23631662306`** and **Smoke Tests** workflow **`23631662325`** — **success** (verified **`headSha`** on each run). **No failed** Linter or Smoke workflows observed for the documented tip chain. Intermediate tips (**`ffbaf457`**, **`77e565f5`**, **`1269c3f3`**, **`01aa27f9`**, **`6a249f2c`**, **`65aa7219`**) — **success** as tabulated above. **M34** implementation SHA remains **`7becd909`** / ledger **`65aa7219`** for code. **Quality** on **`main`** — **post-merge** only.
