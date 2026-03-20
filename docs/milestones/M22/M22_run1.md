# M22 — CI monitoring report (run 1)

**Generated:** 2026-03-20 (UTC, agent poll)  
**Subject:** [PR #41](https://github.com/m-cahill/serena/pull/41) — M22 txt2img/img2img tab modularization  
**Head:** `m22-tab-modularization` (tip includes docs commit `e66d1b18` after this report was first written)  
**Base:** `main` @ `4aa69e8af7ad16dccc729ab07f5a722b8cc9e350`

### Errata (same monitoring pass, after pushing this file)

- Additional **Linter** run on push: **`23362979869`** (success) for commit `docs(M22): CI monitoring report run1 (PR #41)`.
- Latest branch tip at confirmation: **`9a974abd`** — Linter workflow run **`23363001050`** (ruff + eslint success).

---

## Smoke — authoritative confirmation (GitHub Checks API)

This is **not** a CLI visibility gap. The REST API that backs the PR **Checks** tab was queried:

`GET /repos/m-cahill/serena/commits/9a974abd698e1f99849af4c20a3bbe086de07203/check-runs`

| Field | Value |
|--------|--------|
| `total_count` | **2** |
| Check run names | **`ruff`**, **`eslint`** only |
| Smoke / `smoke tests` check | **Absent** |

PR metadata (`gh pr view 41 --json`): **`baseRefName` = `main`**, **`headRefName` = `m22-tab-modularization`** — target branch is correct for `.github/workflows/run_smoke_tests.yaml`.

**Conclusion:** **Smoke Tests did not run** (no check run registered) for PR #41 at the current head. Historical **Smoke Tests** workflow runs in the API still end with M21; none reference `m22-tab-modularization`. Treat as **repository / Actions delivery issue** (Serena governance path: document and fix outside M22 code scope unless you fold a workflow repair into this PR).

---

## Executive summary

| Gate | Status | Evidence |
|------|--------|----------|
| **ruff** | **PASS** | e.g. job on run **23363001050** (head `9a974abd`) |
| **eslint** | **PASS** | same |
| **Smoke Tests** | **Did not run** | Checks API: only 2 runs on PR head; no Smoke workflow run for M22 in Actions history |
| **Quality Tests** | N/A (pre-merge) | Expected on **`main`** after merge per program rules |

**Merge posture (program gates):** Linter is **green**; **Smoke is a blocker** until a green Smoke run exists or delivery is repaired and re-run.

---

## Workflow inventory (from API)

Repo **m-cahill/serena** has four active workflows:

| Workflow | Path | PR trigger |
|----------|------|--------------|
| **Linter** | `.github/workflows/on_pull_request.yaml` | `push` **and** `pull_request` |
| **Smoke Tests** | `.github/workflows/run_smoke_tests.yaml` | `pull_request` → `main` only |
| **Quality Tests** | `.github/workflows/run_quality_tests.yaml` | (not analyzed in this pass; historically `main` push) |
| **Nightly Tests** | `.github/workflows/run_nightly_tests.yaml` | Scheduled / manual |

---

## Observed runs for M22

### Linter (GitHub Actions) — **completed / success**

- **Workflow run ID:** `23362825071`
- **Event:** `push` (branch `m22-tab-modularization`)
- **URL:** https://github.com/m-cahill/serena/actions/runs/23362825071
- **Jobs (per `gh pr checks` / API):**

| Job | Conclusion | Job URL |
|-----|------------|---------|
| **ruff** | success | https://github.com/m-cahill/serena/actions/runs/23362825071/job/67970078543 |
| **eslint** | success | https://github.com/m-cahill/serena/actions/runs/23362825071/job/67970078515 |

**PR checks rollup** (`gh pr view 41 --json statusCheckRollup`) currently lists only these two jobs — consistent with a **push-triggered** Linter run being associated with the PR’s head SHA.

### Smoke Tests — **no run ID found**

- `gh run list --workflow "Smoke Tests"` shows recent PR smoke runs for **M20/M21** branches, **none** titled M22 / `m22-tab-modularization`.
- `gh run list --event pull_request` **does not include** any row for PR #41 / M22.
- **Implication:** The **Smoke Tests** workflow (PR-only) does not appear to have executed for #41 yet, or runs are not visible under the polled filters.

**Recommended actions (maintainer):**

1. Open **PR #41 → Checks** tab and confirm whether Smoke is queued, skipped, or failed to schedule.
2. If absent, trigger CI by an empty commit on `m22-tab-modularization` **after** PR exists, or use **Update branch** / close-reopen PR if policy allows — Smoke listens to `pull_request` and should start a new run.
3. Confirm **Actions** permissions for the repo (no organization policy blocking PR workflows).

---

## Third-party check suites (informational)

GitHub API `check-suites` on `f8505102` includes additional apps (e.g. Netlify, Cursor, Render, Railway) in **queued** or neutral states — **not** Serena merge gates. Merge decisions should rely on **Linter** + **Smoke** + post-merge **Quality**.

---

## Coverage / Quality (post-merge)

- Not evaluated in this report.
- After merge to `main`, record **Quality Tests** run ID and confirm **coverage ≥ 40%** per Phase I guardrails.

---

## Resolution (2026-03-20)

### Empty commit (`5afe79c6`)

`git commit --allow-empty -m "ci: retrigger smoke"` **did not** produce a Smoke run: Checks API on `5afe79c6` still showed **only** `ruff` + `eslint` (Linter workflow **`23365663313`**). **`pull_request` was still not scheduling Smoke** for this PR.

### Workflow repair (commit `9ea22641`)

Updated `.github/workflows/run_smoke_tests.yaml`:

- Added **`push`** with `branches-ignore: [main]` so feature-branch pushes run Smoke (aligned with how Linter already gets signal from `push`).
- Kept **`pull_request` → `branches: [main]`** for when that delivery works.
- **`Verify base branch`** step runs only when `github.event_name == 'pull_request'` (`GITHUB_BASE_REF` is unset on `push`).

### Smoke green (push-triggered)

| Workflow | Run ID | Event | Conclusion |
|----------|--------|-------|------------|
| **Smoke Tests** | **23365701378** | `push` | **success** (~2m59s) |
| **Linter** | **23365701379** | `push` | **success** |

### Checks API — head `9ea226417d473bbfcdb6c0c33c41703c9d5e3b49`

```http
GET /repos/m-cahill/serena/commits/9ea226417d473bbfcdb6c0c33c41703c9d5e3b49/check-runs
```

- `total_count`: **3**
- Names: **`smoke tests`**, **`ruff`**, **`eslint`** — all **`success`**

`gh pr checks 41` matches the above (job URLs under runs **23365701378** / **23365701379**).

---

## Conclusion (superseded)

- **PR #41** at head **`9ea22641`:** **ruff**, **eslint**, and **smoke tests** are **green** per Checks API.
- Root cause of the earlier gap: **`pull_request` did not run Smoke** for this PR; **not** M22 UI code. Mitigation: **push trigger** on non-`main` branches (documented in workflow comments).
- **Post-merge:** still require **Quality Tests** on `main` (≥40% coverage) before M22 closeout.

---

## Post-merge Quality (closeout)

| Field | Value |
|--------|--------|
| **Workflow** | Quality Tests |
| **Run ID** | **23365924953** |
| **Conclusion** | **success** |
| **Coverage** | Gate satisfied (**≥ 40%**, per program) |
| **Merge commit (authoritative)** | `99b5f0c43806c3b521cbb6d8ef561fa87ef2c75d` |

M22 formal closeout: ledger row **Completed**, milestone summary/audit, annotated tag **`v0.0.22-m22`** on the squash merge commit above (not on doc-only follow-ups).
