# M04 Tool Calls Log

**Milestone:** M04 — Coverage / Security / Reproducibility Guardrails  
**Branch:** m04-coverage-guardrails

---

| Timestamp | Tool | Purpose | Files/Target | Status |
|-----------|------|---------|--------------|--------|
| 2026-03-08 | write | Create M04_plan.md from prompt | docs/milestones/M04/M04_plan.md | done |
| 2026-03-08 | write | Create M04_toolcalls.md header | docs/milestones/M04/M04_toolcalls.md | done |
| 2026-03-08 | write | Create verify_pinned_deps.sh | scripts/ci/verify_pinned_deps.sh | done |
| 2026-03-08 | search_replace | Remove pip-audit from Smoke | .github/workflows/run_smoke_tests.yaml | done |
| 2026-03-08 | search_replace | Add pip-audit, verify deps, env capture, coverage 40%, artifacts | .github/workflows/run_quality_tests.yaml | done |
