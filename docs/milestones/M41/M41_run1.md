# M41 — Run 1 (binding)

## Preflight baseline (pre-M41)

- **Binding Quality (post–M40 doc closeout):** run **`23722553628`** — **243** pass, **49%** TOTAL, gate **42%** unchanged (`docs/serena.md`).
- **Performance:** `scripts/ci/write_performance_snapshot.py` produced **`performance_snapshot.txt`**; no regression comparison before M41.
- **Workflows:** No explicit `permissions:` blocks; Nightly used **`pip-audit || true`** before full install.

---

## PR

| Item | Value |
|------|--------|
| **URL** | https://github.com/m-cahill/serena/pull/103 |
| **Title** | M41: Performance guardrails (warn-first), workflow polish, README, closeout prep |
| **Approval / PR head SHA** | **`5efdcc83e76081e55194e727367fd7ddf37d7216`** |

### Authoritative PR CI (merge-blocking)

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** | **`23728560305`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728560305 |
| **Smoke Tests** | **`23728560308`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728560308 |

**Notes:** Node.js 20 deprecation annotations on pinned actions (informational; unchanged from prior runs).

---

## Merge

| Item | Value |
|------|--------|
| **Merge commit (`main`)** | **`8e7736f0b53c93fe13f0aab4e3cc7d188acc2408`** |
| **Merged at (GitHub)** | **2026-03-30T04:57:19Z** |

---

## Post-merge `main` (binding)

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** | **`23728637287`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728637287 |
| **Quality Tests** | **`23728637285`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728637285 |

| Metric | Value |
|--------|--------|
| **Tests passed** | **246** (pytest Quality tier; **+3** vs M40 binding **243** — `test_performance_regression_guard.py`) |
| **TOTAL coverage (pytest-only)** | **49%** |
| **Coverage gate** | **42%** (`--fail-under` unchanged) |

### Performance guardrail (M41)

- **Posture:** **Warn-first, non-blocking** — retained as the **final** M41 decision; **not** promoted to a failing gate on Quality.
- **Step:** **Check performance regression vs baseline (M41 warn-first)** completed **success** on run **`23728637285`**; no `::warning` regression lines observed in the step output for this binding run (probe within committed baseline ratio).

### Workflow / polish delivered

- Explicit **`permissions:`** (`contents: read`, **`actions: write`** for artifact uploads) on all four workflows.
- **Smoke / Nightly:** JUnit XML artifact uploads; **Nightly** `pip-audit` aligned with Quality (**blocking**, same **`--ignore-vuln`** IDs), moved after full install; **`pip_audit_report.txt`** uploaded on Nightly.
- **README:** Serena identity block with links to ledger, CONTRIBUTING, architecture lock.
- **`opts_snapshot.py`:** header matches M39 threading reality.
- **`processing.py`:** missing refiner checkpoint → **`ValueError`** (was **`Exception`**).

---

## Doc closeout (PR #104)

| Item | Value |
|------|--------|
| **PR URL** | https://github.com/m-cahill/serena/pull/104 |
| **Merge commit (`main`)** | **`4cccde03e6714e039ca9b4470898c7d0b0df6421`** |
| **Merged at (GitHub)** | **2026-03-30T05:07:26Z** |

### Authoritative CI (doc-only; merge-blocking on PR)

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** | **`23728811492`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728811492 |
| **Smoke Tests** | **`23728811530`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728811530 |

### Post-merge `main` (binding tip including ledger + closeout bundle)

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** | **`23728891095`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728891095 |
| **Quality Tests** | **`23728891097`** | **success** | https://github.com/m-cahill/serena/actions/runs/23728891097 |

**Note:** **246 passed**, **49%** TOTAL (unchanged vs **#103** binding Quality); performance check step **success**.

---

## Closeout

- **`M41_summary.md`**, **`M41_audit.md`**: merged via **PR #104** (**`4cccde03`**).
- **Ledger:** `docs/serena.md` updated — **Phase IX complete**; **M41** = **final** Serena program milestone (see ledger narrative).
