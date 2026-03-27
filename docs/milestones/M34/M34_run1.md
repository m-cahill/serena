# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (CI green; `gh run view` headSha)** | **`953f1eb80701e80e2e60eac49a2e31d6fcace376`** |
| **Linter (workflow run)** | **`23666940349`** — https://github.com/m-cahill/serena/actions/runs/23666940349 — **success** |
| **Smoke Tests (workflow run)** | **`23666940323`** — https://github.com/m-cahill/serena/actions/runs/23666940323 — **success** |

**Note:** **M34** runtime code is unchanged from **`7becd909`** / **`65aa7219`**; later commits are **documentation / ledger** on this branch. **Duplicate** workflow runs for head **`953f1eb8`**: Linter **`23666939512`**, Smoke **`23666939491`** (both **success**, same **`headSha`**). **No failed** Linter or Smoke runs for this head — earlier tips (including **`5ee59031`**, **`f155e0ca`**, **`dce6f9bb`**, **`dfc01f35`**, **`ebb46e21`**, **`809de851`**, **`8314abd8`**, **`0089bbd4`**, **`e81caab9`**, **`02052e0d`**, **`c7981b31`**, **`74ab007d`**, **`245819c7`**, **`e7c27ab5`**, **`a9a6038a`**, **`1a576a50`**, **`4784a3cb`**, **`3bf92229`**, **`26e8b6f0`**, **`71caacff`**) are tabulated below for traceability.

---

## CI (PR) — primary evidence (head `953f1eb8`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23666940349`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23666940349 |
| **Result** | **success** |
| **headSha** | `953f1eb80701e80e2e60eac49a2e31d6fcace376` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68951152015` | success |
| ruff | `68951152014` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23666940323`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23666940323 |
| **Result** | **success** |
| **headSha** | `953f1eb80701e80e2e60eac49a2e31d6fcace376` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68951151982` | success |

---

## Duplicate workflow runs (same head `953f1eb8`, no failures)

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23666939512` | https://github.com/m-cahill/serena/actions/runs/23666939512 | success | `953f1eb80701e80e2e60eac49a2e31d6fcace376` |
| Smoke Tests | `23666939491` | https://github.com/m-cahill/serena/actions/runs/23666939491 | success | `953f1eb80701e80e2e60eac49a2e31d6fcace376` |

**Primary documentation:** **`23666940349`** (Linter) and **`23666940323`** (Smoke).

---

## Earlier PR tips (traceability; all green; no superseded failures)

### Head `02052e0d`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23663662592` | https://github.com/m-cahill/serena/actions/runs/23663662592 | success | `02052e0d5ae1433418f336acf85e0987b68cf67b` |
| Smoke Tests | `23663662588` | https://github.com/m-cahill/serena/actions/runs/23663662588 | success | `02052e0d5ae1433418f336acf85e0987b68cf67b` |

Duplicates (same head, success): Linter `23663661543`, Smoke `23663661532`.

### Head `e81caab9`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23663861862` | https://github.com/m-cahill/serena/actions/runs/23663861862 | success | `e81caab98f49ea6609f6cbb6c69dedfd9395a222` |
| Smoke Tests | `23663861911` | https://github.com/m-cahill/serena/actions/runs/23663861911 | success | `e81caab98f49ea6609f6cbb6c69dedfd9395a222` |

Duplicates (same head, success): Linter `23663860510`, Smoke `23663860519`.

### Head `0089bbd4`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23664043460` | https://github.com/m-cahill/serena/actions/runs/23664043460 | success | `0089bbd4757a433848e5fe973585dcf01427a5be` |
| Smoke Tests | `23664043477` | https://github.com/m-cahill/serena/actions/runs/23664043477 | success | `0089bbd4757a433848e5fe973585dcf01427a5be` |

Duplicates (same head, success): Linter `23664042295`, Smoke `23664042289`.

### Head `8314abd8`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23664194874` | https://github.com/m-cahill/serena/actions/runs/23664194874 | success | `8314abd8f91625d3cb3aafbf12a9b7442ce6bba8` |
| Smoke Tests | `23664194869` | https://github.com/m-cahill/serena/actions/runs/23664194869 | success | `8314abd8f91625d3cb3aafbf12a9b7442ce6bba8` |

Duplicates (same head, success): Linter `23664193187`, Smoke `23664193202`.

### Head `809de851`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23664346495` | https://github.com/m-cahill/serena/actions/runs/23664346495 | success | `809de8515cc2b69e8b64388578a18e7d724a3996` |
| Smoke Tests | `23664346494` | https://github.com/m-cahill/serena/actions/runs/23664346494 | success | `809de8515cc2b69e8b64388578a18e7d724a3996` |

Duplicates (same head, success): Linter `23664344028`, Smoke `23664344021`.

### Head `ebb46e21`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23664506905` | https://github.com/m-cahill/serena/actions/runs/23664506905 | success | `ebb46e21e4916a0b76f83506aa85aa7ebce538c8` |
| Smoke Tests | `23664506914` | https://github.com/m-cahill/serena/actions/runs/23664506914 | success | `ebb46e21e4916a0b76f83506aa85aa7ebce538c8` |

Duplicates (same head, success): Linter `23664505584`, Smoke `23664505569`.

### Head `dfc01f35`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23664662561` | https://github.com/m-cahill/serena/actions/runs/23664662561 | success | `dfc01f35f6165a16ac70694820c9876b63c32c4b` |
| Smoke Tests | `23664662508` | https://github.com/m-cahill/serena/actions/runs/23664662508 | success | `dfc01f35f6165a16ac70694820c9876b63c32c4b` |

Duplicates (same head, success): Linter `23664661100`, Smoke `23664661126`.

### Head `dce6f9bb`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23665040641` | https://github.com/m-cahill/serena/actions/runs/23665040641 | success | `dce6f9bb0499708b4fb2d4c7f77e79ddafe7eec4` |
| Smoke Tests | `23665040630` | https://github.com/m-cahill/serena/actions/runs/23665040630 | success | `dce6f9bb0499708b4fb2d4c7f77e79ddafe7eec4` |

Duplicates (same head, success): Linter `23665039362`, Smoke `23665039364`.

### Head `f155e0ca`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23665190205` | https://github.com/m-cahill/serena/actions/runs/23665190205 | success | `f155e0ca160afbd858e6ce299371b2741bf81c1f` |
| Smoke Tests | `23665190202` | https://github.com/m-cahill/serena/actions/runs/23665190202 | success | `f155e0ca160afbd858e6ce299371b2741bf81c1f` |

Duplicates (same head, success): Linter `23665188860`, Smoke `23665188887`.

### Head `5ee59031`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23666266370` | https://github.com/m-cahill/serena/actions/runs/23666266370 | success | `5ee590315fe2ed625037c747f8838ec762b6e39c` |
| Smoke Tests | `23666266366` | https://github.com/m-cahill/serena/actions/runs/23666266366 | success | `5ee590315fe2ed625037c747f8838ec762b6e39c` |

Duplicates (same head, success): Linter `23666264276`, Smoke `23666264244`.

### Head `c7981b31`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23662031988` | https://github.com/m-cahill/serena/actions/runs/23662031988 | success | `c7981b31a626e3680d546f1617ea53345215e1f6` |
| Smoke Tests | `23662031986` | https://github.com/m-cahill/serena/actions/runs/23662031986 | success | `c7981b31a626e3680d546f1617ea53345215e1f6` |

Duplicates (same head, success): Linter `23662030901`, Smoke `23662030908`.

### Head `74ab007d`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23661844003` | https://github.com/m-cahill/serena/actions/runs/23661844003 | success | `74ab007d7355ba1887065e78cc2dc8232b1d0cf6` |
| Smoke Tests | `23661843999` | https://github.com/m-cahill/serena/actions/runs/23661843999 | success | `74ab007d7355ba1887065e78cc2dc8232b1d0cf6` |

Duplicates (same head, success): Linter `23661841886`, Smoke `23661841897`.

### Head `245819c7`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23661601519` | https://github.com/m-cahill/serena/actions/runs/23661601519 | success | `245819c7148dfc19fdf37a4686159511dd5c7f19` |
| Smoke Tests | `23661601549` | https://github.com/m-cahill/serena/actions/runs/23661601549 | success | `245819c7148dfc19fdf37a4686159511dd5c7f19` |

Duplicates (same head, success): Linter `23661600005`, Smoke `23661600013`.

### Head `e7c27ab5`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23635116812` | https://github.com/m-cahill/serena/actions/runs/23635116812 | success | `e7c27ab5603b17f6a7b9614f1c8b921f8f503673` |
| Smoke Tests | `23635116843` | https://github.com/m-cahill/serena/actions/runs/23635116843 | success | `e7c27ab5603b17f6a7b9614f1c8b921f8f503673` |

Duplicates (same head, success): Linter `23635115859`, Smoke `23635115857`.

### Head `a9a6038a`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23635000130` | https://github.com/m-cahill/serena/actions/runs/23635000130 | success | `a9a6038ac5c2a95590c3173bd6c0174751739265` |
| Smoke Tests | `23635000125` | https://github.com/m-cahill/serena/actions/runs/23635000125 | success | `a9a6038ac5c2a95590c3173bd6c0174751739265` |

Duplicates (same head, success): Linter `23634999315`, Smoke `23634999311`.

### Head `1a576a50`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634880146` | https://github.com/m-cahill/serena/actions/runs/23634880146 | success | `1a576a50820b2e60f5123179f03d8627df67a4e4` |
| Smoke Tests | `23634880140` | https://github.com/m-cahill/serena/actions/runs/23634880140 | success | `1a576a50820b2e60f5123179f03d8627df67a4e4` |

Duplicates (same head, success): Linter `23634878926`, Smoke `23634878944`.

### Head `4784a3cb`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634730404` | https://github.com/m-cahill/serena/actions/runs/23634730404 | success | `4784a3cb2fd57174774312dbbb4974e70bcb03b5` |
| Smoke Tests | `23634730399` | https://github.com/m-cahill/serena/actions/runs/23634730399 | success | `4784a3cb2fd57174774312dbbb4974e70bcb03b5` |

Duplicates (same head, success): Linter `23634729400`, Smoke `23634729412`.

### Head `3bf92229`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634591829` | https://github.com/m-cahill/serena/actions/runs/23634591829 | success | `3bf9222995d1738f2071dad3845ecc93d6232cdc` |
| Smoke Tests | `23634591828` | https://github.com/m-cahill/serena/actions/runs/23634591828 | success | `3bf9222995d1738f2071dad3845ecc93d6232cdc` |

Duplicates (same head, success): Linter `23634590804`, Smoke `23634590820`.

### Head `26e8b6f0`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634461712` | https://github.com/m-cahill/serena/actions/runs/23634461712 | success | `26e8b6f00b7a3d85a37cb52dbc5450db91d84d30` |
| Smoke Tests | `23634461662` | https://github.com/m-cahill/serena/actions/runs/23634461662 | success | `26e8b6f00b7a3d85a37cb52dbc5450db91d84d30` |

Duplicates (same head, success): Linter `23634460724`, Smoke `23634460720`.

### Head `71caacff`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634336392` | https://github.com/m-cahill/serena/actions/runs/23634336392 | success | `71caacff81de98fb61eb9e62a27b2c6aa457f34c` |
| Smoke Tests | `23634336373` | https://github.com/m-cahill/serena/actions/runs/23634336373 | success | `71caacff81de98fb61eb9e62a27b2c6aa457f34c` |

Duplicates (same head, success): Linter `23634335563`, Smoke `23634335587`.

### Head `94cb78eb`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634219365` | https://github.com/m-cahill/serena/actions/runs/23634219365 | success | `94cb78eb547ea3c3015fcc09e8d518b2806f9c0f` |
| Smoke Tests | `23634219339` | https://github.com/m-cahill/serena/actions/runs/23634219339 | success | `94cb78eb547ea3c3015fcc09e8d518b2806f9c0f` |

Duplicates (same head, success): Linter `23634218106`, Smoke `23634218117`.

### Head `7667bba4`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23634107933` | https://github.com/m-cahill/serena/actions/runs/23634107933 | success | `7667bba4c66c91aa60a7e52f1c6d9824298e8d7d` |
| Smoke Tests | `23634107926` | https://github.com/m-cahill/serena/actions/runs/23634107926 | success | `7667bba4c66c91aa60a7e52f1c6d9824298e8d7d` |

Duplicates (same head, success): Linter `23634107152`, Smoke `23634107156`.

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

**Merge review:** **PR #90** tip **`953f1eb80701e80e2e60eac49a2e31d6fcace376`** — **Linter** workflow **`23666940349`** and **Smoke Tests** workflow **`23666940323`** — **success** (verified **`gh run view` `headSha`** matches the PR head on each run). **No failed** Linter or Smoke workflows observed for this tip. Earlier tips (**`5ee59031`**, **`f155e0ca`**, **`dce6f9bb`**, **`dfc01f35`**, **`ebb46e21`**, **`809de851`**, **`8314abd8`**, **`0089bbd4`**, **`e81caab9`**, **`02052e0d`**, **`c7981b31`**, **`74ab007d`**, **`245819c7`**, **`e7c27ab5`**, **`a9a6038a`**, **`1a576a50`**, **`4784a3cb`**, **`3bf92229`**, **`26e8b6f0`**, **`71caacff`**, **`94cb78eb`**, **`7667bba4`**, **`1a250705`**, **`549904f7`**, **`b1e5cea3`**, **`6b4b377d`**, **`7d92ecae`**, **`5691611d`**, **`dddb3920`**, **`01fbb7df`**, **`0be479fc`**, **`3faec321`**, **`8fea3852`**, **`ab7b003d`**, **`1269c3f3`**, **`01aa27f9`**, **`6a249f2c`**, **`65aa7219`**) — **success** as tabulated above. **M34** implementation SHA remains **`7becd909`** / ledger **`65aa7219`** for code. **Quality** on **`main`** — **post-merge** only.
