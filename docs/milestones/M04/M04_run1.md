# M04 Run 1 — CI Analysis

**Milestone:** M04  
**Branch:** m04-coverage-guardrails  
**PR:** #4  
**Report generated:** 2026-03-09

---

## 1. CI Status

| Workflow | Run ID | Status |
|----------|--------|--------|
| Linter (ruff, eslint) | 22835795245 | ✓ PASS |
| Smoke Tests | (pending) | Runs on pull_request |

**Note:** Smoke Tests only triggers on `pull_request` events. Linter runs on both push and pull_request. Quality Tests runs on push to main (not triggered until merge).

---

## 2. Changes Implemented

1. **Smoke:** Removed pip-audit step (keep fast, deterministic)
2. **Quality:** Added pip-audit after install (fail on vuln)
3. **Quality:** Added verify_pinned_deps.sh (requirements_versions.txt vs installed)
4. **Quality:** Added ci_environment.txt capture and upload
5. **Quality:** Coverage gate 33% → 40%
6. **Quality:** Added --cov-report=term, coverage.xml and ci_environment.txt artifacts

---

## 3. Verification Checklist

- [x] Smoke: pip-audit removed
- [x] Quality: pip-audit added (fail on vuln)
- [x] Quality: reproducibility check script
- [x] Quality: coverage gate 40%
- [x] Quality: artifact uploads
- [ ] Smoke Tests: pass (after PR merge or workflow trigger)
- [ ] Quality Tests: pass (after merge to main)

---

## 4. Next Steps

1. Merge PR #4 to main
2. Quality Tests will run on push to main
3. Verify: pip-audit, verify_pinned_deps, coverage ≥40%, artifacts
4. If CI fails, address per Phase 4 of milestone workflow
