# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (CI green; `gh run view` headSha)** | **`8e209ed224481ea582be1bdce9aa115a4ae3f869`** |
| **Linter (workflow run)** | **`23669814419`** — https://github.com/m-cahill/serena/actions/runs/23669814419 — **success** |
| **Smoke Tests (workflow run)** | **`23669814433`** — https://github.com/m-cahill/serena/actions/runs/23669814433 — **success** |

**Note:** **M34** runtime code is unchanged from **`7becd909`** / **`65aa7219`**; later commits are **documentation / ledger** on this branch. **Duplicate** workflow runs for head **`8e209ed2`**: Linter **`23669813327`**, Smoke **`23669813334`** (both **success**, same **`headSha`**). **No failed** Linter or Smoke runs for this tip — earlier tips (including **`29ad3c27`**, **`f9bc6dd9`**, **`059671ea`**, **`409737e5`**, **`656449f0`**, **`776166df`**, **`124b22f9`**, **`900d971a`**, **`8fc64fc2`**, **`e9494338`**, **`20d7d479`**, **`ab95de62`**, **`818acc4c`**, **`0913ba0d`**, **`db8bf371`**, **`953f1eb8`**, **`5ee59031`**, **`f155e0ca`**, **`dce6f9bb`**, **`dfc01f35`**, **`ebb46e21`**, **`809de851`**, **`8314abd8`**, **`0089bbd4`**, **`e81caab9`**, **`02052e0d`**, **`c7981b31`**, **`74ab007d`**, **`245819c7`**, **`e7c27ab5`**, **`a9a6038a`**, **`1a576a50`**, **`4784a3cb`**, **`3bf92229`**, **`26e8b6f0`**, **`71caacff`**) are tabulated below for traceability.

---

## CI (PR) — primary evidence (head `8e209ed2`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23669814419`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23669814419 |
| **Result** | **success** |
| **headSha** | `8e209ed224481ea582be1bdce9aa115a4ae3f869` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68960585404` | success |
| ruff | `68960585413` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23669814433`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23669814433 |
| **Result** | **success** |
| **headSha** | `8e209ed224481ea582be1bdce9aa115a4ae3f869` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68960585373` | success |

---

## Duplicate workflow runs (same head `8e209ed2`, push event)

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23669813327` | https://github.com/m-cahill/serena/actions/runs/23669813327 | success | `8e209ed224481ea582be1bdce9aa115a4ae3f869` |
| Smoke Tests | `23669813334` | https://github.com/m-cahill/serena/actions/runs/23669813334 | success | `8e209ed224481ea582be1bdce9aa115a4ae3f869` |

**Primary documentation:** **`23669814419`** (Linter) and **`23669814433`** (Smoke).

---

## Earlier PR tips (traceability; all green; no superseded failures)

### Head `29ad3c27`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23669692847` | https://github.com/m-cahill/serena/actions/runs/23669692847 | success | `29ad3c278f5819a1350c3b14c5a9cdfee20b9f06` |
| Smoke Tests | `23669692841` | https://github.com/m-cahill/serena/actions/runs/23669692841 | success | `29ad3c278f5819a1350c3b14c5a9cdfee20b9f06` |

Duplicates (same head, success): Linter `23669691677`, Smoke `23669691667`.

### Head `f9bc6dd9`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23669527266` | https://github.com/m-cahill/serena/actions/runs/23669527266 | success | `f9bc6dd9ee61c3a0126aa0607e5c5f1a907b5cd8` |
| Smoke Tests | `23669527272` | https://github.com/m-cahill/serena/actions/runs/23669527272 | success | `f9bc6dd9ee61c3a0126aa0607e5c5f1a907b5cd8` |

Duplicates (same head, success): Linter `23669526293`, Smoke `23669526265`.

### Head `059671ea`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23669404006` | https://github.com/m-cahill/serena/actions/runs/23669404006 | success | `059671ea93a75b8d87c0d69f796f5bfb7c5822c6` |
| Smoke Tests | `23669404027` | https://github.com/m-cahill/serena/actions/runs/23669404027 | success | `059671ea93a75b8d87c0d69f796f5bfb7c5822c6` |

Duplicates (same head, success): Linter `23669402577`, Smoke `23669402558`.

### Head `409737e5`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23669234218` | https://github.com/m-cahill/serena/actions/runs/23669234218 | success | `409737e5febafce6e819d8c13503c9b2ec18bade` |
| Smoke Tests | `23669234253` | https://github.com/m-cahill/serena/actions/runs/23669234253 | success | `409737e5febafce6e819d8c13503c9b2ec18bade` |

Duplicates (same head, success): Linter `23669232729`, Smoke `23669232753`.

### Head `656449f0`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23669112091` | https://github.com/m-cahill/serena/actions/runs/23669112091 | success | `656449f0b210cfef4895e44367ec94f390f6367e` |
| Smoke Tests | `23669112065` | https://github.com/m-cahill/serena/actions/runs/23669112065 | success | `656449f0b210cfef4895e44367ec94f390f6367e` |

Duplicates (same head, success): Linter `23669110752`, Smoke `23669110750`.

### Head `776166df`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23668913287` | https://github.com/m-cahill/serena/actions/runs/23668913287 | success | `776166df23cd85d41c334937c336004e9b11831b` |
| Smoke Tests | `23668913329` | https://github.com/m-cahill/serena/actions/runs/23668913329 | success | `776166df23cd85d41c334937c336004e9b11831b` |

Duplicates (same head, success): Linter `23668912050`, Smoke `23668912021`.

### Head `124b22f9`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23668723195` | https://github.com/m-cahill/serena/actions/runs/23668723195 | success | `124b22f98d9c2255b2772484d7d0d23ab0daf391` |
| Smoke Tests | `23668723190` | https://github.com/m-cahill/serena/actions/runs/23668723190 | success | `124b22f98d9c2255b2772484d7d0d23ab0daf391` |

Duplicates (same head, success): Linter `23668721690`, Smoke `23668721686`.

### Head `900d971a`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23668534848` | https://github.com/m-cahill/serena/actions/runs/23668534848 | success | `900d971a5ef71ed5a77a6a60c4fb87c42dff9a8f` |
| Smoke Tests | `23668534840` | https://github.com/m-cahill/serena/actions/runs/23668534840 | success | `900d971a5ef71ed5a77a6a60c4fb87c42dff9a8f` |

Duplicates (same head, success): Linter `23668533912`, Smoke `23668533899`.

### Head `8fc64fc2`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23668298135` | https://github.com/m-cahill/serena/actions/runs/23668298135 | success | `8fc64fc27fb47742e7032328252537c5fc478f94` |
| Smoke Tests | `23668298116` | https://github.com/m-cahill/serena/actions/runs/23668298116 | success | `8fc64fc27fb47742e7032328252537c5fc478f94` |

Duplicates (same head, success): Linter `23668296706`, Smoke `23668296720`. **Smoke** PR run **`23668298116`**: first attempt **failed** (CI flake: test server did not listen on **`127.0.0.1:7860`** within the wait window); **`gh run rerun --failed`** completed **success** (same workflow run ID).

### Head `e9494338`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23667754052` | https://github.com/m-cahill/serena/actions/runs/23667754052 | success | `e9494338844f7f732457301468a7d8b19d36772c` |
| Smoke Tests | `23667754060` | https://github.com/m-cahill/serena/actions/runs/23667754060 | success | `e9494338844f7f732457301468a7d8b19d36772c` |

Duplicates (same head, success): Linter `23667753011`, Smoke `23667752985`.

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

### Head `953f1eb8`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23666940349` | https://github.com/m-cahill/serena/actions/runs/23666940349 | success | `953f1eb80701e80e2e60eac49a2e31d6fcace376` |
| Smoke Tests | `23666940323` | https://github.com/m-cahill/serena/actions/runs/23666940323 | success | `953f1eb80701e80e2e60eac49a2e31d6fcace376` |

Duplicates (same head, success): Linter `23666939512`, Smoke `23666939491`.

### Head `db8bf371`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23667074977` | https://github.com/m-cahill/serena/actions/runs/23667074977 | success | `db8bf37174c253c7a26ab9dd7ad7dcd90cdf23e7` |
| Smoke Tests | `23667074975` | https://github.com/m-cahill/serena/actions/runs/23667074975 | success | `db8bf37174c253c7a26ab9dd7ad7dcd90cdf23e7` |

Duplicates (same head, success): Linter `23667073553`, Smoke `23667073567`.

### Head `0913ba0d`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23667206878` | https://github.com/m-cahill/serena/actions/runs/23667206878 | success | `0913ba0dec73706258669d7af5dff6b5bd6296a7` |
| Smoke Tests | `23667206863` | https://github.com/m-cahill/serena/actions/runs/23667206863 | success | `0913ba0dec73706258669d7af5dff6b5bd6296a7` |

Duplicates (same head, success): Linter `23667205757`, Smoke `23667205810`.

### Head `818acc4c`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23667357476` | https://github.com/m-cahill/serena/actions/runs/23667357476 | success | `818acc4c491f80b06728d41ac33c977931bc52f9` |
| Smoke Tests | `23667357477` | https://github.com/m-cahill/serena/actions/runs/23667357477 | success | `818acc4c491f80b06728d41ac33c977931bc52f9` |

Duplicates (same head, success): Linter `23667355702`, Smoke `23667355715`.

### Head `ab95de62`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23667495160` | https://github.com/m-cahill/serena/actions/runs/23667495160 | success | `ab95de62981a3b665694a4bcb32c28484d327a20` |
| Smoke Tests | `23667495172` | https://github.com/m-cahill/serena/actions/runs/23667495172 | success | `ab95de62981a3b665694a4bcb32c28484d327a20` |

Duplicates (same head, success): Linter `23667493690`, Smoke `23667493702`.

### Head `20d7d479`

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23667625500` | https://github.com/m-cahill/serena/actions/runs/23667625500 | success | `20d7d4794fb680fb9d0fe2fde067b26d1253eaee` |
| Smoke Tests | `23667625505` | https://github.com/m-cahill/serena/actions/runs/23667625505 | success | `20d7d4794fb680fb9d0fe2fde067b26d1253eaee` |

Duplicates (same head, success): Linter `23667624530`, Smoke `23667624545`.

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
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Merge method** | **Merge commit** (`gh pr merge --merge`) — not squash / not rebase |
| **Merge commit on `main`** | **`b94c93d38e521437a18bb1660d35b31c90220be0`** |
| **Merged at (UTC)** | `2026-03-27T22:47:02Z` |
| **Branch merged** | `m34-runtime-context-model-identity` |
| **Second parent (branch tip at merge)** | **`40ba7361e88b16f04eaa5ff89521b39339ca3c22`** |

**Authoritative PR head (approval / PR CI ledger):** **`8e209ed224481ea582be1bdce9aa115a4ae3f869`** — **Linter** **`23669814419`**, **Smoke** **`23669814433`** (see §CI (PR) above).

---

## CI (`main`, post-merge)

**Proof surface:** **Quality Tests** on `main` is the **binding** post-merge gate (combined pytest + coverage policy unchanged). **Linter** on `main` is recorded alongside.

### A — Push = merge commit only (`b94c93d3`)

Triggered by merge **push** to `main` (merge commit **`b94c93d3`**).

| Workflow | Run ID | URL | Result | `headSha` |
|----------|--------|-----|--------|-----------|
| **Linter** | **`23670713074`** | https://github.com/m-cahill/serena/actions/runs/23670713074 | **success** | `b94c93d38e521437a18bb1660d35b31c90220be0` |
| **Quality Tests** | **`23670713081`** | https://github.com/m-cahill/serena/actions/runs/23670713081 | **failure** | `b94c93d38e521437a18bb1660d35b31c90220be0` |

**Quality failure:** `test_model_identity_available_before_script_hooks` — test stub did not implement the full `scripts` surface invoked by `process_images_inner` / sampling (`AttributeError` on missing hook). **Runtime / M34 product code unchanged;** test-only correction on `main` (see §B).

**Duplicates:** None observed for this push (single Linter + single Quality for `b94c93d3`).

### B — Binding post-merge green (`main` tip after test fix)

Follow-up commits on **`main`** adjust **`test/quality/test_runtime_mock.py`** only ( **`MagicMock`** for `p.scripts` + assertions on `process` and `before_process_batch` ). **Binding** tip:

| Field | Value |
|-------|--------|
| **`main` commit (binding)** | **`1bc04394b3844b4b9c7fda6448567e735d8ec0cc`** |

| Workflow | Run ID | URL | Result | `headSha` |
|----------|--------|-----|--------|-----------|
| **Linter** | **`23671154431`** | https://github.com/m-cahill/serena/actions/runs/23671154431 | **success** | `1bc04394b3844b4b9c7fda6448567e735d8ec0cc` |
| **Quality Tests** | **`23671154433`** | https://github.com/m-cahill/serena/actions/runs/23671154433 | **success** | `1bc04394b3844b4b9c7fda6448567e735d8ec0cc` |

**Quality summary (as reported in workflow log):** **`202 passed`**, **`13 warnings`**, coverage line **`TOTAL ... 48%`** (same combined report shape as prior milestones).

**Intermediate failed pushes (superseded):** `016f234c`, `6e04d331` — Quality failed until stub completed; **no duplicate binding runs** retained — primary authoritative green = **`23671154433`** on **`1bc04394`**.

---

## Verdict (PR CI + post-merge)

**PR CI (pre-merge):** **PR #90** authoritative tip **`8e209ed224481ea582be1bdce9aa115a4ae3f869`** — **Linter** **`23669814419`** and **Smoke Tests** **`23669814433`** — **success**. Earlier tips tabulated above — **success**.

**Merge:** **PR #90** merged to **`main`** as merge commit **`b94c93d38e521437a18bb1660d35b31c90220be0`** (merge commit, **`2026-03-27T22:47:02Z`**).

**Post-merge:** **Quality** **`23670713081`** on merge commit **`b94c93d3`** — **failure** (test stub). **Binding** post-merge **Quality** **`23671154433`** + **Linter** **`23671154431`** on **`1bc04394b3844b4b9c7fda6448567e735d8ec0cc`** — **success**; coverage **48%**, **202** tests passed — **CI policy unchanged**.
