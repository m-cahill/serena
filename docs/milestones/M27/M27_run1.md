# M27 — CI run 1

**PR:** [#54](https://github.com/m-cahill/serena/pull/54) (squash-merged to `main`)  
**Merge commit:** `d1897cf2668b6df35b233e9b0da2e0d135aa4773`  
**Date:** 2026-03-24 UTC

## Quality attempt 1 (post-merge) — **fail (coverage)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality Tests (`main`) | [23473843412](https://github.com/m-cahill/serena/actions/runs/23473843412) | **fail** | **`Show coverage`**: combined **TOTAL 40%** < **`fail-under=42`**. Tests **116** passed. Radon / radon artifact **skipped** (coverage step exited first). `htmlcov` upload skipped (no directory). |

### Log excerpt

```text
TOTAL ... 40%
Coverage failure: total of 40 is less than fail-under=42
```

### Root cause

M26-reported **40%** was **at the floor**; raising the gate to **42%** without enough new covered statements left the combined report **short**. The four deprecation contract tests did not move the **TOTAL** by two percentage points (~**~340** statements on ~**18.8k** total).

### Remediation (follow-up PR)

Branch **`m27-coverage-42-followup`** / **PR #55**: targeted tests only (no threshold relaxation):

- More **GET** API coverage: `hypernetworks`, `realesrgan-models`, `embeddings`.
- **POST** control/refresh: `interrupt`, `skip`, `refresh-embeddings`, `refresh-checkpoints`, `refresh-vae`.
- **`parse_generation_parameters`** (doc-style + compact infotext).
- **`quote` / `unquote`**, **`create_opts_snapshot`**, **`prepare_prompt_seed_state`** branches, **`calculate_sha256`**.

## Linter / Smoke (PR phase)

Capture PR **#54** / **#55** Linter + Smoke run IDs in the table below when closing out (same pattern as M26).

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Linter (PR #54) | _(add)_ | | |
| Smoke (PR #54) | _(add)_ | | |

## Quality attempt 2 (binding)

**Expected after merge of PR #55:** combined coverage **≥ 42%**, **Radon** step runs, **`radon_report.txt`** uploaded, **D/E/F** `::warning` likely (non-blocking).

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | _(after #55 merge)_ | | |

## Final verdict

**Pending:** Quality **attempt 2** green on `main` after **#55**. M27 audit/summary/ledger update remain per **permission** after binding evidence.
