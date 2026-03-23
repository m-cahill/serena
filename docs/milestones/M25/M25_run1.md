# M25 — CI monitoring report (run 1)

**Generated:** 2026-03-23 (UTC, `gh` poll after smoke completion)  
**Subject:** [PR #44](https://github.com/m-cahill/serena/pull/44) — M25 Deprecation & compatibility scaffolding  
**Head:** `m25-deprecation-compat-scaffolding` @ `821c61e06a59541c9f51d7eec1ba06a5788c3d2c`  
**Base:** `main` @ `e46b51ac1a288a33a9f83f2b6f97c7e6a95c3a2c`  
**PR state:** OPEN, **MERGEABLE** (`mergeStateStatus`: CLEAN)

**CI snapshot SHA:** The workflow run IDs below correspond to PR head **`821c61e0`** (last code change). Commit **`8856a25b`** (this report + toolcalls log only) was pushed afterward and will schedule another CI wave; expect equivalent gates.

---

## Executive summary

| Gate | Status | Notes |
|------|--------|--------|
| **ruff** | **PASS** | Two successful runs (`push` + `pull_request`) |
| **eslint** | **PASS** | Jobs on same **Linter** workflow runs as ruff |
| **Smoke Tests** | **PASS** | Two successful runs |
| **Quality Tests** | **N/A (pre-merge)** | Expected on **`main`** after merge |

**Merge posture (program PR gates):** Required checks **green** at current head.

---

## Duplicate checks (expected)

GitHub registered **six** check rows on PR #44: **two** each of ruff, eslint, and smoke — **`push`** and **`pull_request`** on the branch.

### Wave at head `821c61e0` (signature default commit)

| Event | Linter run ID | Smoke run ID |
|--------|---------------|--------------|
| `push` | `23417599328` | `23417599322` |
| `pull_request` | `23417606838` | `23417606843` |

All concluded **success**.

---

## Latest Linter workflow — job detail

### Run `23417599328` (`push`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| ruff | success | 7s | https://github.com/m-cahill/serena/actions/runs/23417599328/job/68116022534 |
| eslint | success | 14s | https://github.com/m-cahill/serena/actions/runs/23417599328/job/68116022523 |

### Run `23417606838` (`pull_request`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| ruff | success | 9s | https://github.com/m-cahill/serena/actions/runs/23417606838/job/68116044221 |
| eslint | success | 14s | https://github.com/m-cahill/serena/actions/runs/23417606838/job/68116044196 |

**Workflow URLs:**  
https://github.com/m-cahill/serena/actions/runs/23417599328 · https://github.com/m-cahill/serena/actions/runs/23417606838

---

## Latest Smoke Tests — job detail

### Run `23417599322` (`push`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| smoke tests | success | 2m48s | https://github.com/m-cahill/serena/actions/runs/23417599322/job/68116022493 |

**Note:** Step **Verify base branch** reported **skipped** on this `push` event (workflow-defined); job still **success**.

### Run `23417606843` (`pull_request`)

| Job | Conclusion | Duration (approx.) | Job URL |
|-----|------------|--------------------|---------|
| smoke tests | success | 2m52s | https://github.com/m-cahill/serena/actions/runs/23417606843/job/68116044224 |

**Workflow URLs:**  
https://github.com/m-cahill/serena/actions/runs/23417599322 · https://github.com/m-cahill/serena/actions/runs/23417606843

---

## Quality / post-merge

- Capture **Quality** workflow run ID and coverage on **`main`** after squash-merge for ledger closeout (expect ≥ 40% combined coverage gate).

---

## Raw `gh pr checks 44` snapshot (head `821c61e0`)

```
eslint      pass  14s  https://github.com/m-cahill/serena/actions/runs/23417599328/job/68116022523
eslint      pass  14s  https://github.com/m-cahill/serena/actions/runs/23417606838/job/68116044196
ruff        pass   7s  https://github.com/m-cahill/serena/actions/runs/23417599328/job/68116022534
ruff        pass   9s  https://github.com/m-cahill/serena/actions/runs/23417606838/job/68116044221
smoke tests pass 2m48s https://github.com/m-cahill/serena/actions/runs/23417599322/job/68116022493
smoke tests pass 2m52s https://github.com/m-cahill/serena/actions/runs/23417606843/job/68116044224
```
