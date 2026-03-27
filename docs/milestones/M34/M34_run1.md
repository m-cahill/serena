# M34 — Run 1 (PR CI)

**Branch:** `m34-runtime-context-model-identity`

**Purpose:** Record PR **Linter** and **Smoke** workflow results for M34. **Quality** on `main` is **post-merge** only (fill after merge + push to `main`).

---

## Authoritative PR head (current tip)

| Field | Value |
|-------|--------|
| **PR** | **[#90](https://github.com/m-cahill/serena/pull/90)** — *feat(M34): Runtime context model-identity seam* |
| **Head SHA (validated by CI below)** | **`6a249f2cbf1d3d5b21b1877185927a0494920a05`** |
| **Head commit** | `docs(M34): fill M34_run1 with PR #90 Linter/Smoke evidence (head 65aa7219)` |

This tip includes the **filled `M34_run1.md`** and is the SHA merge would apply. **No failed** Linter or Smoke runs for this SHA.

---

## CI (PR) — primary evidence (head `6a249f2c`)

### Linter

| Field | Value |
|-------|--------|
| **Workflow run** | **`23631029429`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23631029429 |
| **Result** | **success** |
| **headSha** | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| eslint | `68830145159` | success |
| ruff | `68830145153` | success |

### Smoke Tests

| Field | Value |
|-------|--------|
| **Workflow run** | **`23631029475`** |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23631029475 |
| **Result** | **success** |
| **headSha** | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |
| **Event** | `pull_request` |

| Job | Job ID | Result |
|-----|--------|--------|
| smoke tests | `68830145314` | success |

---

## Duplicate workflow runs (same head `6a249f2c`, no failures)

A second Linter run and second Smoke run were triggered for the **same** `pull_request` / **same head SHA**. **All success.**

| Workflow | Alternate run ID | URL | Result | headSha |
|----------|------------------|-----|--------|---------|
| Linter | `23631028766` | https://github.com/m-cahill/serena/actions/runs/23631028766 | success | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |
| Smoke Tests | `23631028775` | https://github.com/m-cahill/serena/actions/runs/23631028775 | success | `6a249f2cbf1d3d5b21b1877185927a0494920a05` |

**Primary documentation:** **`23631029429`** (Linter) and **`23631029475`** (Smoke).

---

## Earlier PR CI (implementation + first docs commit, head `65aa7219`)

**M34 runtime/code** (`feat(M34): ModelIdentity…` and `docs(M34): record PR #90…`) was validated at **`65aa7219ddd25c9f968b12a336df427129a563a1`** before the **`M34_run1.md` evidence fill** commit. **Linter** and **Smoke** were **green**; **no failed runs** for that head.

| Workflow | Run ID | URL | Result | headSha |
|----------|--------|-----|--------|---------|
| Linter | `23628995102` | https://github.com/m-cahill/serena/actions/runs/23628995102 | success | `65aa7219ddd25c9f968b12a336df427129a563a1` |
| Smoke Tests | `23628995101` | https://github.com/m-cahill/serena/actions/runs/23628995101 | success | `65aa7219ddd25c9f968b12a336df427129a563a1` |

Duplicate runs (same head `65aa7219`, all success): Linter **`23628993965`**, Smoke **`23628993960`**.

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

**PR #90 tip `6a249f2cbf1d3d5b21b1877185927a0494920a05`:** **Linter** (`23631029429`) and **Smoke Tests** (`23631029475`) **green**. Implementation predecessor **`65aa7219`** also **green** on Linter/Smoke as recorded above. **Quality** on `main` **after merge** only.
