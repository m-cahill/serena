# M03 Plan — Test Architecture (Smoke / Quality / Nightly)

**Milestone:** M03  
**Title:** Test architecture (smoke / quality / nightly)  
**Branch:** `m03-test-architecture`  
**Status:** In progress  
**Depends on:** M02 (complete)

---

## 1. Intent / Target

Introduce a structured test tier architecture without changing runtime behavior. The purpose is to:

1. Separate fast verification tests from heavy tests
2. Enable deterministic CI runs with smoke-only on every PR
3. Prepare the repo for large refactors starting in Phase II

This milestone must not change runtime behavior or break API contracts.

---

## 2. Scope Boundaries

### In scope

* Test tiers: smoke, quality, nightly
* Pytest markers and config
* Separate CI workflows (smoke on PR, quality on push to main, nightly scheduled)
* CI guardrails: repo check, base-branch check
* Pre-push hook template to prevent upstream push
* Milestone docs and ledger update

### Explicitly out of scope

* Runtime behavior changes
* API contract changes
* New test logic (only structural migration)

---

## 3. Test Architecture

```
test/
  conftest.py          # shared fixtures (unchanged)
  smoke/               # fast verification (< 60 sec)
    test_txt2img.py
    test_img2img.py
    test_extras.py
    test_utils.py
    test_face_restorers.py
    test_torch_utils.py
  quality/             # deeper unit tests (< 5 min)
    .gitkeep
  nightly/             # heavy/slow tests
    .gitkeep
```

---

## 4. CI Workflow Layout

| Workflow | File | Trigger | Coverage gate |
|----------|------|---------|---------------|
| Smoke Tests | run_smoke_tests.yaml | pull_request (target main) | No |
| Quality Tests | run_quality_tests.yaml | push to main | Yes (33%) |
| Nightly Tests | run_nightly_tests.yaml | schedule, workflow_dispatch | Optional |

---

## 5. Guardrails

### CI

* Repo guard: `GITHUB_REPOSITORY == m-cahill/serena`
* PR smoke: `GITHUB_BASE_REF == main`
* Push quality: `GITHUB_REF == refs/heads/main`
* Nightly: repo guard only

### Pre-push hook

* `scripts/dev/prevent_upstream_push.sh`
* Abort if push target remote URL does not contain `m-cahill/serena`
* Clear message if target looks like AUTOMATIC1111/upstream

---

## 6. Invariants Preserved

| Invariant | Verification |
|-----------|---------------|
| API response schemas | API tests unchanged |
| CLI behavior | Smoke tests unchanged |
| Extension loading | Unchanged |
| Generation semantics | Unchanged |
| CI truthfulness | Smoke deterministic, quality enforces coverage |

---

## 7. Definition of Done

* [ ] test/smoke populated with migrated tests
* [ ] test/quality, test/nightly scaffolded
* [ ] pytest.ini with markers
* [ ] run_smoke_tests.yaml (PR only)
* [ ] run_quality_tests.yaml (push to main)
* [ ] run_nightly_tests.yaml (schedule + dispatch)
* [ ] run_tests.yaml removed
* [ ] prevent_upstream_push.sh created
* [ ] CONTRIBUTING.md updated
* [ ] CI green (smoke)
* [ ] Ledger updated
