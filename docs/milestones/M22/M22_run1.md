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

## Conclusion

- **Linter (ruff + eslint):** **Green** — run **`23362825071`**.
- **Smoke:** **Not confirmed** — **blocker for “PR fully green”** until a Smoke run completes successfully or absence is explained.
- **Next report (run 2):** Re-poll after Smoke appears; append run ID and pass/fail.
