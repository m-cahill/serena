# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (merge candidate)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (validated by primary CI below)** | **`1269c3f395fe51931a7faeb8bc9d9291d9499153`** |
| **Head commit** | `docs(M34): M34_run1 — authoritative CI for PR tip 01aa27f9` |

**Note:** Further docs-only commits may advance the PR tip; **runtime / implementation** for M34 is unchanged from **`7becd909`** / **`65aa7219`**. The **primary Linter / Smoke** runs below are **GitHub-verified** for **`1269c3f395fe51931a7faeb8bc9d9291d9499153`** (`gh run view` **headSha**).

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

## Latest PR tip (includes this file)

After the evidence commits above, **PR #90** **`headRef`** was **`ffbaf457e186d8f363aadc819a883f992089754f`**. **Linter** and **Smoke** were **success** for that SHA (docs-only delta; no `modules/` or `test/` change vs **`1269c3f3`**).

| Workflow | Run ID | URL | Result | headSha (verified) |
|----------|--------|-----|--------|--------------------|
| Linter | **`23631449100`** | https://github.com/m-cahill/serena/actions/runs/23631449100 | success | `ffbaf457e186d8f363aadc819a883f992089754f` |
| Smoke Tests | **`23631449121`** | https://github.com/m-cahill/serena/actions/runs/23631449121 | success | `ffbaf457e186d8f363aadc819a883f992089754f` |

Duplicate runs (same head `ffbaf457`, success): Linter **`23631448471`**, Smoke **`23631448466`**.

### Subsequent tip (this doc file updated)

| Field | Value |
|-------|--------|
| **headRef** | **`77e565f56da0f5e560c8227c40e1593429eb2ff8`** |
| Linter | **`23631542758`** — https://github.com/m-cahill/serena/actions/runs/23631542758 — **success** |
| Smoke Tests | **`23631542742`** — https://github.com/m-cahill/serena/actions/runs/23631542742 — **success** |

Duplicate runs (same head `77e565f5`, success): Linter **`23631541576`**, Smoke **`23631541583`**.

---

## Verdict (PR CI)

**Primary evidence (detailed tables):** head **`1269c3f395fe51931a7faeb8bc9d9291d9499153`** — **Linter** (`23631342096`) and **Smoke Tests** (`23631342094`) **success** (verified **headSha** on workflow runs). **Latest push** **`ffbaf457`** — **Linter** (`23631449100`) and **Smoke** (`23631449121`) **success**. Earlier tips (**`01aa27f9`**, **`6a249f2c`**, **`65aa7219`**) also **green** — **no failed** workflows for those heads. **Quality** on `main` **after merge** only.
