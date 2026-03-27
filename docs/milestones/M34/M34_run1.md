# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (CI green; `gh run view` headSha)** | **`7667bba4c66c91aa60a7e52f1c6d9824298e8d7d`** |
| **Head commit** | `docs(M34): M34_run1 — PR #90 head 1a250705 + Linter 23633992443 / Smoke 23633992448` |
| **Linter (workflow run)** | **`23634107933`** — https://github.com/m-cahill/serena/actions/runs/23634107933 — **success** |
| **Smoke Tests (workflow run)** | **`23634107926`** — https://github.com/m-cahill/serena/actions/runs/23634107926 — **success** |

**Note:** **M34** runtime code is unchanged from **`7becd909`** / **`65aa7219`**; commits after that are **documentation / ledger** on this branch. Duplicate workflow runs for the same head: Linter **`23634107152`**, Smoke **`23634107156`** (both **success**, same **headSha**). **Detailed** tables for earlier tips are below for traceability.

---

## CI (PR) — primary evidence (head `7667bba4`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23634107933`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23634107933 |
| **Result** | **success** |
| **headSha** | `7667bba4c66c91aa60a7e52f1c6d9824298e8d7d` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68839584844` | success |
| ruff | `68839584855` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23634107926`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23634107926 |
| **Result** | **success** |
| **headSha** | `7667bba4c66c91aa60a7e52f1c6d9824298e8d7d` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68839584814` | success |

---

## Duplicate workflow runs (same head `7667bba4`, no failures)

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23634107152` | https://github.com/m-cahill/serena/actions/runs/23634107152 | success | `7667bba4c66c91aa60a7e52f1c6d9824298e8d7d` |
| Smoke Tests | `23634107156` | https://github.com/m-cahill/serena/actions/runs/23634107156 | success | `7667bba4c66c91aa60a7e52f1c6d9824298e8d7d` |

**Primary documentation:** **`23634107933`** (Linter) and **`23634107926`** (Smoke).

---

## Earlier PR tips (traceability; all green; no superseded failures)

### Head `1a250705`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633992443` | https://github.com/m-cahill/serena/actions/runs/23633992443 | success | `1a250705ab9502f87c156f781e554d5ad203470b` |
| Smoke Tests | `23633992448` | https://github.com/m-cahill/serena/actions/runs/23633992448 | success | `1a250705ab9502f87c156f781e554d5ad203470b` |

Duplicates (same head, success): Linter `23633991993`, Smoke `23633991989`.

### Head `549904f7`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633873462` | https://github.com/m-cahill/serena/actions/runs/23633873462 | success | `549904f7e15a116e40ed63f55130e2dd63786a93` |
| Smoke Tests | `23633873442` | https://github.com/m-cahill/serena/actions/runs/23633873442 | success | `549904f7e15a116e40ed63f55130e2dd63786a93` |

Duplicates (same head, success): Linter `23633872151`, Smoke `23633872166`.

### Head `b1e5cea3`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633758896` | https://github.com/m-cahill/serena/actions/runs/23633758896 | success | `b1e5cea3092eb0b5faf013ee0a90479d6411619b` |
| Smoke Tests | `23633758909` | https://github.com/m-cahill/serena/actions/runs/23633758909 | success | `b1e5cea3092eb0b5faf013ee0a90479d6411619b` |

Duplicates (same head, success): Linter `23633757923`, Smoke `23633757925`.

### Head `6b4b377d`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633630805` | https://github.com/m-cahill/serena/actions/runs/23633630805 | success | `6b4b377d0376a34f1bc1cd05e0735ac2e9832732` |
| Smoke Tests | `23633630807` | https://github.com/m-cahill/serena/actions/runs/23633630807 | success | `6b4b377d0376a34f1bc1cd05e0735ac2e9832732` |

Duplicates (same head, success): Linter `23633629767`, Smoke `23633629786`.

### Head `7d92ecae`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633499637` | https://github.com/m-cahill/serena/actions/runs/23633499637 | success | `7d92ecaee41730c09018635e00236d6a6d3b0751` |
| Smoke Tests | `23633499636` | https://github.com/m-cahill/serena/actions/runs/23633499636 | success | `7d92ecaee41730c09018635e00236d6a6d3b0751` |

Duplicates (same head, success): Linter `23633498886`, Smoke `23633498846`.

### Head `5691611d`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633375020` | https://github.com/m-cahill/serena/actions/runs/23633375020 | success | `5691611d234ad3d01b04b16ee6fdd5582685c1e2` |
| Smoke Tests | `23633375021` | https://github.com/m-cahill/serena/actions/runs/23633375021 | success | `5691611d234ad3d01b04b16ee6fdd5582685c1e2` |

Duplicates (same head, success): Linter `23633374162`, Smoke `23633374165`.

### Head `dddb3920`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633256238` | https://github.com/m-cahill/serena/actions/runs/23633256238 | success | `dddb3920874a20ee4c9ad82c405df758c4f2535e` |
| Smoke Tests | `23633256223` | https://github.com/m-cahill/serena/actions/runs/23633256223 | success | `dddb3920874a20ee4c9ad82c405df758c4f2535e` |

Duplicates (same head, success): Linter `23633255453`, Smoke `23633255456`.

### Head `01fbb7df`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633144141` | https://github.com/m-cahill/serena/actions/runs/23633144141 | success | `01fbb7df8438acbacf4857d60aa6bf80e1d65b75` |
| Smoke Tests | `23633144144` | https://github.com/m-cahill/serena/actions/runs/23633144144 | success | `01fbb7df8438acbacf4857d60aa6bf80e1d65b75` |

Duplicates (same head, success): Linter `23633143530`, Smoke `23633143522`.

### Head `0be479fc`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23633044983` | https://github.com/m-cahill/serena/actions/runs/23633044983 | success | `0be479fcaf77c383371a5a72c615895400f18bd0` |
| Smoke Tests | `23633044981` | https://github.com/m-cahill/serena/actions/runs/23633044981 | success | `0be479fcaf77c383371a5a72c615895400f18bd0` |

Duplicates (same head, success): Linter `23633043958`, Smoke `23633043970`.

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

**Merge review:** **PR #90** tip **`7667bba4c66c91aa60a7e52f1c6d9824298e8d7d`** — **Linter** workflow **`23634107933`** and **Smoke Tests** workflow **`23634107926`** — **success** (verified **`headSha`** on each run). **No failed** Linter or Smoke workflows observed for the documented tip chain. Intermediate tips (**`1a250705`**, **`549904f7`**, **`b1e5cea3`**, **`6b4b377d`**, **`7d92ecae`**, **`5691611d`**, **`dddb3920`**, **`01fbb7df`**, **`0be479fc`**, **`3faec321`**, **`8fea3852`**, **`ab7b003d`**, **`46c3fa74`**, **`88e961f6`**, **`bebde38e`**, **`cf092bbd`**, **`5da40bfe`**, **`996b2514`**, **`9321a441`**, **`ffbaf457`**, **`77e565f5`**, **`1269c3f3`**, **`01aa27f9`**, **`6a249f2c`**, **`65aa7219`**) — **success** as tabulated above. **M34** implementation SHA remains **`7becd909`** / ledger **`65aa7219`** for code. **Quality** on **`main`** — **post-merge** only.
