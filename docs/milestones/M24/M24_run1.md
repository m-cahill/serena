# M24 — CI monitoring report (run 1)

**Generated:** 2026-03-22 (UTC, `gh` poll)  
**Subject:** [PR #43](https://github.com/m-cahill/serena/pull/43) — M24 Extension API v1 contract and documentation  
**Head:** `m24-extension-api-contract` @ `a184e66b70389a15606094d023b27a6c7d39abe1`  
**Base:** `main` @ `08865e3eeb2d167a88a9b1b85240d9e32e68e1c8`  
**PR state:** OPEN, **MERGEABLE** (per prior poll)

---

## Executive summary

| Gate | Status | Notes |
|------|--------|--------|
| **ruff** | **PASS** | Two successful runs (push + `pull_request`) |
| **eslint** | **PASS** | Jobs on same **Linter** workflow runs as ruff |
| **Smoke Tests** | **PASS** | Two successful runs |
| **Quality Tests** | **N/A (pre-merge)** | Expected on **`main`** after merge |

**Merge posture (program PR gates):** Required checks **green** at current head.

---

## Duplicate checks (expected)

GitHub registered **six** check rows on PR #43: **two** each of ruff, eslint, and smoke — **push** and **`pull_request`** on the branch.

### Latest wave (head `a184e66b` — docs plan commit)

| Event | Linter run ID | Smoke run ID |
|--------|---------------|----------------|
| `push` | `23395414175` | `23395414165` |
| `pull_request` | `23395414702` | `23395414700` |

All concluded **success**.

### Earlier wave (implementation commit `482b12c1`)

| Event | Linter run ID | Smoke run ID |
|--------|---------------|----------------|
| `push` | `23395342959` | `23395342950` |
| `pull_request` | `23395344432` | `23395344428` |

All concluded **success**.

---

## Latest Linter workflow — job detail

### Run `23395414175` (`push`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| ruff | success | 7s | https://github.com/m-cahill/serena/actions/runs/23395414175/job/68057447337 |
| eslint | success | 12s | https://github.com/m-cahill/serena/actions/runs/23395414175/job/68057447334 |

### Run `23395414702` (`pull_request`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| ruff | success | 9s | https://github.com/m-cahill/serena/actions/runs/23395414702/job/68057448740 |
| eslint | success | 12s | https://github.com/m-cahill/serena/actions/runs/23395414702/job/68057448739 |

**Workflow URLs:**  
https://github.com/m-cahill/serena/actions/runs/23395414175 · https://github.com/m-cahill/serena/actions/runs/23395414702

---

## Latest Smoke Tests — job detail

### Run `23395414165` (`push`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| smoke tests | success | 3m2s | https://github.com/m-cahill/serena/actions/runs/23395414165/job/68057447336 |

### Run `23395414700` (`pull_request`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| smoke tests | success | 2m50s | https://github.com/m-cahill/serena/actions/runs/23395414700/job/68057448759 |

**Workflow URLs:**  
https://github.com/m-cahill/serena/actions/runs/23395414165 · https://github.com/m-cahill/serena/actions/runs/23395414700

---

## Quality / post-merge

- Capture **Quality** workflow run ID and coverage on **`main`** after squash-merge for ledger closeout.

---

## Raw `gh pr checks 43` snapshot (latest head)

```
eslint  pass  12s  …/runs/23395414175/job/68057447334
eslint  pass  12s  …/runs/23395414702/job/68057448739
ruff    pass   7s  …/runs/23395414175/job/68057447337
ruff    pass   9s  …/runs/23395414702/job/68057448740
smoke tests  pass  3m2s   …/runs/23395414165/job/68057447336
smoke tests  pass  2m50s  …/runs/23395414700/job/68057448759
```
