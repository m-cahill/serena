# M04 Audit — Coverage / Security / Reproducibility Guardrails

**Milestone:** M04  
**Title:** Coverage / security / reproducibility guardrails  
**Branch:** m04-coverage-guardrails  
**Audit date:** 2026-03-09  
**Mode:** DELTA AUDIT  
**Range:** 975dda4b (M03)…47439cac (M04 closeout)  
**CI Status:** Green (Quality 22871471473)  
**Refactor Posture:** Behavior-Preserving  
**Audit Verdict:** 🟢 Milestone objectives met. No runtime behavior change. Proceed.

---

## 1. Executive Summary

M04 successfully added coverage, security, and reproducibility guardrails to CI without changing runtime behavior.

**Wins:**
* Coverage gate raised to 40% (Quality Tests)
* pip-audit integrated (informational; remediation deferred to M27)
* Reproducibility check: verify_pinned_deps.sh
* CI artifact capture: coverage.xml, ci_environment.txt
* Coverage omit config for core modules (extensions, repos, scripts, deepbooru excluded)
* Quality unit tests: prompt_parser, API endpoints

**Risks:** None identified.

**Next action:** Proceed to M05 (Override isolation / temporary opts seam).

---

## 2. CI Evidence

| Check | Result |
|-------|--------|
| Workflow | Quality Tests |
| Run ID | 22871471473 |
| Coverage | 40% (18624 stmts, 11202 missing) |
| pip-audit | Executed (informational; vulns deferred to M27) |
| verify_pinned_deps | ✓ Passed |
| Artifacts | coverage.xml ✓, ci_environment.txt ✓ |

---

## 3. Delta Map & Blast Radius

| Changed | Impact |
|---------|--------|
| run_quality_tests.yaml | pip-audit, verify_pinned_deps, coverage 40%, artifacts |
| run_smoke_tests.yaml | pip-audit removed |
| scripts/ci/verify_pinned_deps.sh | New reproducibility script |
| pyproject.toml | [tool.coverage.run] omit |
| test/quality/test_util_modules.py | prompt_parser unit tests |
| test/quality/test_api_extended.py | Extended API endpoint tests |

**Blast radius:** CI and test layout only. No application code behavior changed.

---

## 4. Category Scores

| Category | Score | Notes |
|----------|-------|-------|
| Coverage gate | 5 | 40% enforced; omit config documented |
| Security | 5 | pip-audit integrated; remediation deferred |
| Reproducibility | 5 | verify_pinned_deps, ci_environment.txt |
| CI artifact capture | 5 | coverage.xml, ci_environment.txt |
| **Overall** | **5.0** | |

---

## 5. pip-audit Note

pip-audit runs with `continue-on-error: true`. Vulnerabilities found are reported as warnings. Full remediation is deferred to M27 (Security/supply-chain evidence). See M04_plan.md, M04_summary.md for scope.
