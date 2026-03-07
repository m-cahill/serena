# M00 CI Inventory

**Date:** 2025-03-06  
**Branch:** m00-kickoff-baseline-e2e

---

## 1. Workflow Files

| File | Purpose |
|------|---------|
| `.github/workflows/on_pull_request.yaml` | Linter (ruff, eslint) |
| `.github/workflows/run_tests.yaml` | Full pytest suite against live server |
| `.github/workflows/warns_merge_master.yml` | Fails PRs that target `master` |

---

## 2. Linter Workflow (`on_pull_request.yaml`)

**Name:** Linter  
**Triggers:** push, pull_request  
**Condition:** Runs only when `head.repo.full_name != base.repo.full_name` (fork PRs)

| Job | What it proves | Blocking |
|-----|----------------|----------|
| **lint-python** | Ruff passes on repo root | Yes |
| **lint-js** | eslint passes after `npm i --ci` | Yes |

**Steps:**
- Checkout (actions/checkout@v4)
- setup-python 3.11 (actions/setup-python@v5)
- `pip install ruff==0.3.3`
- `ruff .`
- setup-node 18 (actions/setup-node@v4)
- `npm i --ci`
- `npm run lint`

**Gaps:** Actions use tags (@v4, @v5); no SHA pinning. `npm i --ci` used; package-lock.json gitignored.

---

## 3. Tests Workflow (`run_tests.yaml`)

**Name:** Tests  
**Triggers:** push, pull_request  
**Condition:** Same fork-PR condition

| Job | What it proves | Blocking |
|-----|----------------|----------|
| **test** | App starts, pytest passes, coverage collected | Yes |

**Steps:**
1. Checkout
2. setup-python 3.10.6, cache pip
3. Cache models (key: 2023-12-30)
4. `pip install wait-for-it -r requirements-test.txt`
5. `python launch.py --skip-torch-cuda-test --exit` (env setup)
6. Start server in background: `coverage run launch.py --test-server ... --use-cpu all`
7. `wait-for-it --service 127.0.0.1:7860 -t 20`
8. `pytest -vv --junitxml=test/results.xml --cov . --cov-report=xml --verify-base-url test`
9. Kill server via `/sdapi/v1/server-stop`
10. `coverage combine`, `coverage report -i`, `coverage html -i`
11. Upload artifacts (output.txt, htmlcov) if: always()

**Gaps:**
- No `--cov-fail-under`
- Single job (no smoke vs quality vs nightly)
- Actions use @v4
- No pip-audit or npm audit

---

## 4. warns_merge_master

**Triggers:** pull_request to `master`  
**Effect:** `exit 1` — PRs targeting master fail (normally dev is used)

---

## 5. Fork vs Same-Repo Behavior

**Critical:** Lint and Tests jobs have:
```yaml
if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name != github.event.pull_request.base.repo.full_name
```

- **Fork PR:** head.repo ≠ base.repo → jobs run
- **Same-repo PR:** head.repo = base.repo → jobs **skip**

For m-cahill/serena: PRs from a branch in the same repo will **not** run Linter or Tests. Only fork PRs (e.g., from a contributor's fork) trigger them. Pushes to branches do run (event_name = push).

**Verification:** Push to m00-kickoff-baseline-e2e will trigger workflows. PR from m00-kickoff-baseline-e2e → master in same repo will skip Linter/Tests unless the condition is different for same-repo.

*Correction:* For `pull_request`, the condition is true when it's a fork PR. For same-repo PR, the condition is false, so the job is skipped. For `push`, `event_name != 'pull_request'` is true, so jobs run. So:
- **Push to branch:** Linter and Tests run
- **PR from fork:** Linter and Tests run
- **PR from same-repo branch:** Linter and Tests **skip**

This is a significant gap for a refactor program that does most work in-branch. M01 may need to address this.

---

## 6. Gaps Summary

| Gap | Severity | Notes |
|-----|----------|-------|
| Same-repo PRs skip lint/tests | High | Blocks CI on typical workflow |
| No coverage threshold | Medium | Coverage can regress silently |
| No test tiers | Medium | No fast smoke gate |
| Actions use tags | Medium | Supply-chain risk |
| No pip-audit | Medium | Dependency vuln risk |
| package-lock gitignored | Low | npm ci not possible |
