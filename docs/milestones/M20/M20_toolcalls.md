# M20 Toolcalls

## Context

Milestone: M20 — Runtime tests with mockable boundaries  
Phase: Phase IV — Runtime Extraction

## Actions

| Timestamp | Purpose | Files | Status |
|-----------|---------|-------|--------|
| (init) | Milestone folder seeded at M19 closeout | docs/milestones/M20/ | done |
| 2026-03-19 (session) | M20 implementation: canonical plan, fixtures, quality tests, branch | docs/milestones/M20/, test/fixtures/, test/quality/test_runtime_mock.py | done (await CI) |
| 2026-03-20 | Push branch + open PR #39 to main | origin/m20-runtime-mock-tests | done |

---

## Notes

* Follows M19: runtime model access via `ModelProvider`; next focus is mockable boundaries and tests.  
* Baseline: M19 merge on `main` (PR #37 + #38).
