# M01 Plan — CI Truthfulness & Guardrails

**Milestone:** M01  
**Title:** CI truthfulness, SHA pinning, smoke path  
**Status:** In Progress

---

## Intent

CI truthfulness and guardrails.

Stabilize CI before any refactor work begins. Make CI a trustworthy signal for same-repo PRs and pushes.

---

## Scope

1. **Fix CI environment failure** — CLIP/pkg_resources: install setuptools before env setup; add `--no-build-isolation` to clip pip install in launch_utils (avoids isolated build env lacking pkg_resources)
2. **Ensure CI runs on all PRs** — Remove same-repo PR skip condition from both workflows
3. **Introduce smoke validation** — Fast startup check before full test suite
4. **Add minimal coverage gate** — `--cov-fail-under=60`
5. **Add pip-audit** — Non-blocking dependency vulnerability scan
6. **Pin GitHub Actions to SHAs** — Replace tags with commit SHAs for reproducibility
7. **Add .gitattributes** — CRLF/LF normalization for Windows dev

---

## Non-goals

- No runtime refactors
- No architecture changes
- No CI tiering (smoke vs quality vs nightly) — that is M03

---

## Definition of Done

- [ ] CI runs on push and pull_request (including same-repo PRs)
- [ ] Linter: PASS
- [ ] Tests: PASS (including smoke step)
- [ ] Coverage threshold enforced (60%)
- [ ] pip-audit runs (non-blocking)
- [ ] All actions pinned to SHAs
- [ ] .gitattributes present
- [ ] docs/serena.md updated with M01 status
