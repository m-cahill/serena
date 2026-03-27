# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (CI green; `gh run view` headSha)** | **`0be479fcaf77c383371a5a72c615895400f18bd0`** |
| **Head commit** | `docs(M34): M34_run1 — authoritative head 3faec321 + Linter/Smoke run IDs` |
| **Linter (workflow run)** | **`23633044983`** — https://github.com/m-cahill/serena/actions/runs/23633044983 — **success** |
| **Smoke Tests (workflow run)** | **`23633044981`** — https://github.com/m-cahill/serena/actions/runs/23633044981 — **success** |

**Note:** **M34** runtime code is unchanged from **`7becd909`** / **`65aa7219`**; commits after that are **documentation / ledger** on this branch. Duplicate workflow runs for the same head: Linter **`23633043958`**, Smoke **`23633043970`** (both **success**, same **headSha**). **Detailed** tables for earlier tips are below for traceability.

---

## CI (PR) — primary evidence (head `0be479fc`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23633044983`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23633044983 |
| **Result** | **success** |
| **headSha** | `0be479fcaf77c383371a5a72c615895400f18bd0` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68836462719` | success |
| ruff | `68836462706` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23633044981`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23633044981 |
| **Result** | **success** |
| **headSha** | `0be479fcaf77c383371a5a72c615895400f18bd0` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68836462722` | success |

---

## Duplicate workflow runs (same head `0be479fc`, no failures)

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23633043958` | https://github.com/m-cahill/serena/actions/runs/23633043958 | success | `0be479fcaf77c383371a5a72c615895400f18bd0` |
| Smoke Tests | `23633043970` | https://github.com/m-cahill/serena/actions/runs/23633043970 | success | `0be479fcaf77c383371a5a72c615895400f18bd0` |

**Primary documentation:** **`23633044983`** (Linter) and **`23633044981`** (Smoke).

---

## Earlier PR tips (traceability; all green; no superseded failures)

### Head `3faec321`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23632914402` | https://github.com/m-cahill/serena/actions/runs/23632914402 | success | `3faec3218aedb1dea48cb5364cbf92d53f1fa216` |
| Smoke Tests | `23632914393` | https://github.com/m-cahill/serena/actions/runs/23632914393 | success | `3faec3218aedb1dea48cb5364cbf92d53f1fa216` |

Duplicates (same head, success): Linter `23632913601`, Smoke `23632913612`.

### Head `8fea3852`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23632797485` | https://github.com/m-cahill/serena/actions/runs/23632797485 | success | `8fea3852c5dba7a16b662173a769ecf912ac656a` |
| Smoke Tests | `23632797462` | https://github.com/m-cahill/serena/actions/runs/23632797462 | success | `8fea3852c5dba7a16b662173a769ecf912ac656a` |

Duplicates (same head, success): Linter `23632796365`, Smoke `23632796370`.

### Head `ab7b003d`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23632681848` | https://github.com/m-cahill/serena/actions/runs/23632681848 | success | `ab7b003dd7a960de3a42711aeb0adc3d4d1c0b5b` |
| Smoke Tests | `23632681873` | https://github.com/m-cahill/serena/actions/runs/23632681873 | success | `ab7b003dd7a960de3a42711aeb0adc3d4d1c0b5b` |

Duplicates (same head, success): Linter `23632680793`, Smoke `23632680787`.

### Head `1269c3f3`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23631342096` | https://github.com/m-cahill/serena/actions/runs/23631342096 | success | `1269c3f395fe51931a7faeb8bc9d9291d9499153` |
| Smoke Tests | `23631342094` | https://github.com/m-cahill/serena/actions/runs/23631342094 | success | `1269c3f395fe51931a7faeb8bc9d9291d9499153` |

Duplicates (same head, success): Linter `23631341419`, Smoke `23631341408`.

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

**Merge review:** **PR #90** tip **`0be479fcaf77c383371a5a72c615895400f18bd0`** — **Linter** workflow **`23633044983`** and **Smoke Tests** workflow **`23633044981`** — **success** (verified **`headSha`** on each run). **No failed** Linter or Smoke workflows observed for the documented tip chain. Intermediate tips (**`3faec321`**, **`8fea3852`**, **`ab7b003d`**, **`46c3fa74`**, **`88e961f6`**, **`bebde38e`**, **`cf092bbd`**, **`5da40bfe`**, **`996b2514`**, **`9321a441`**, **`ffbaf457`**, **`77e565f5`**, **`1269c3f3`**, **`01aa27f9`**, **`6a249f2c`**, **`65aa7219`**) — **success** as tabulated above. **M34** implementation SHA remains **`7becd909`** / ledger **`65aa7219`** for code. **Quality** on **`main`** — **post-merge** only.
