# M03 Summary — Test Architecture

**Project:** Serena  
**Phase:** Phase I — Baseline & Guardrails  
**Milestone:** M03 — Test architecture (smoke / quality / nightly)  
**Status:** In progress  
**Branch:** m03-test-architecture

---

## Accomplished

| Item | Status |
|------|--------|
| test/smoke structure | ✓ Migrated 6 test files |
| test/quality, test/nightly | ✓ Scaffolded with .gitkeep |
| pytest.ini | ✓ Markers (smoke, quality, nightly) |
| Path-based marker application | ✓ conftest.py pytest_collection_modifyitems |
| run_smoke_tests.yaml | ✓ PR only, no coverage gate |
| run_quality_tests.yaml | ✓ Push to main, coverage gate 33% |
| run_nightly_tests.yaml | ✓ Schedule + workflow_dispatch |
| run_tests.yaml | ✓ Removed |
| prevent_upstream_push.sh | ✓ Created |
| CONTRIBUTING.md | ✓ Pre-push hook, test tiers |
| test/__init__.py | ✓ Package for test.conftest import |

---

## Test Architecture

```
test/
  conftest.py
  smoke/           # 33 tests, < 60 sec
  quality/         # scaffolded
  nightly/         # scaffolded
```

---

## CI Workflow Layout

| Workflow | Trigger | Coverage |
|----------|---------|----------|
| Smoke Tests | pull_request (main) | No gate |
| Quality Tests | push to main | 33% gate |
| Nightly Tests | cron + dispatch | Informational |

---

## Guardrails

* Repo: `GITHUB_REPOSITORY == m-cahill/serena`
* PR smoke: `GITHUB_BASE_REF == main`
* Push quality: `GITHUB_REF == refs/heads/main`
* Pre-push hook: validates push target URL

---

## Invariants Preserved

* API response schemas
* CLI behavior
* Extension loading
* Generation semantics
* CI truthfulness
