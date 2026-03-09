# M04 Summary — Coverage / Security / Reproducibility Guardrails

**Project:** Serena  
**Phase:** Phase I — Baseline & Guardrails  
**Milestone:** M04 — Coverage / security / reproducibility guardrails  
**Status:** Closed  
**Branch:** m04-coverage-guardrails  
**PR:** #4 (initial); #5–#17 (fixes)  
**Commit:** 47439cac (closeout)  
**Quality Run:** 22871471473 ✓

---

## Accomplished

| Item | Status |
|------|--------|
| Coverage gate 33% → 40% | ✓ Quality Tests |
| pip-audit integration | ✓ Quality (informational; remediation deferred to M27) |
| Reproducibility verification | ✓ verify_pinned_deps.sh |
| CI artifact capture | ✓ coverage.xml, ci_environment.txt |
| Coverage omit (pyproject.toml) | ✓ extensions-builtin, repositories, scripts, deepbooru |
| Quality unit tests | ✓ test_util_modules (prompt_parser), test_api_extended |

---

## CI Layout After M04

| Workflow | Trigger | Coverage | Security |
|----------|---------|----------|----------|
| Smoke Tests | pull_request (main) | No gate | None |
| Quality Tests | push to main | ≥40% | pip-audit (informational) |
| Nightly Tests | cron + dispatch | Optional | Optional |

---

## Coverage Configuration

Coverage is focused on core application code via `pyproject.toml`:

```toml
[tool.coverage.run]
omit = [
    "extensions-builtin/*",
    "repositories/*",
    "scripts/*",
    "modules/deepbooru_model.py",
    "modules/deepbooru.py",
    "*/__pycache__/*",
    "config*.py",
]
```

---

## Guardrails

- Repo: `GITHUB_REPOSITORY == m-cahill/serena`
- PR smoke: `GITHUB_BASE_REF == main`
- Push quality: `GITHUB_REF == refs/heads/main`
- Coverage: combined server + pytest, fail-under=40%

---

## Invariants Preserved

- API response schemas
- CLI behavior
- Extension loading
- Generation semantics
- CI truthfulness
