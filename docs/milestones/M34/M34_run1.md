# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (validated by primary CI below)** | **`01aa27f9c4786d37a82fd43478fcf5f87d5d1567`** |
| **Head commit** | `docs(M34): M34_run1 — primary CI at tip 6a249f2c + historical 65aa7219` |

This is the **current PR tip** (includes the complete **`M34_run1.md`** narrative). **Linter** and **Smoke** are **green** for this SHA (see below). **No failed** checks for this head.

---

## CI (PR) — primary evidence (head `01aa27f9`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23631114397`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23631114397 |
| **Result** | **success** |
| **headSha** | `01aa27f9c4786d37a82fd43478fcf5f87d5d1567` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68830401032` | success |
| ruff | `68830401035` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23631114399`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23631114399 |
| **Result** | **success** |
| **headSha** | `01aa27f9c4786d37a82fd43478fcf5f87d5d1567` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68830401050` | success |

---

## Duplicate workflow runs (same head `01aa27f9`, no failures)

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23631113346` | https://github.com/m-cahill/serena/actions/runs/23631113346 | success | `01aa27f9c4786d37a82fd43478fcf5f87d5d1567` |
| Smoke Tests | `23631113357` | https://github.com/m-cahill/serena/actions/runs/23631113357 | success | `01aa27f9c4786d37a82fd43478fcf5f87d5d1567` |

**Primary documentation:** **`23631114397`** (Linter) and **`23631114399`** (Smoke).

---

## Earlier PR tips (traceability; all green, no superseded failures)

### Head `6a249f2c` — first filled `M34_run1` + CI for that doc state

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23631029429` | https://github.com/m-cahill/serena/actions/runs/23631029429 | success | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |
| Smoke Tests | `23631029475` | https://github.com/m-cahill/serena/actions/runs/23631029475 | success | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |

Duplicates (same head, success): Linter `23631028766`, Smoke `23631028775`.

### Head `65aa7219` — M34 implementation + PR #90 ledger line (before full `M34_run1` expansion)

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

**PR #90 current tip `01aa27f9c4786d37a82fd43478fcf5f87d5d1567`:** **Linter** (`23631114397`) and **Smoke Tests** (`23631114399`) **success**. Earlier tips **`6a249f2c`** and **`65aa7219`** also **green** as recorded above — **no failed** workflow for these heads. **Quality** on `main` **after merge** only.
