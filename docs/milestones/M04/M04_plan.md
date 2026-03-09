# M04 Plan — Coverage / Security / Reproducibility Guardrails

**Milestone:** M04  
**Title:** Coverage / security / reproducibility guardrails  
**Branch:** `m04-coverage-guardrails`  
**Status:** Completed  
**Depends on:** M03 (complete)

---

## 1. Intent / Target

Strengthen CI guardrails before structural refactors begin in Phase II. M04 introduces:

- Stronger coverage enforcement (33% → 40%)
- Security / dependency scanning (pip-audit, fail on high/critical)
- Reproducible dependency verification (pinned deps match installed)
- CI environment determinism capture (ci_environment.txt artifact)
- CI artifact retention (coverage.xml, ci_environment.txt)

No runtime behavior changes are allowed.

---

## 2. Scope Boundaries

### In scope

- Coverage gate raise: 33% → 40% (Quality Tests only)
- pip-audit in Quality Tests (fail on vulnerability)
- Remove pip-audit from Smoke (keep Smoke fast)
- Reproducibility: verify requirements_versions.txt matches installed versions
- CI environment artifact: python --version, pip --version, pip freeze → ci_environment.txt
- Artifact uploads: coverage.xml, ci_environment.txt
- Milestone docs and ledger update

### Explicitly out of scope

- Full pip freeze diff (deferred to Phase VI M25–M29)
- pip-audit in Smoke or Nightly
- Runtime behavior changes
- API contract changes

---

## 3. CI Layout After M04

| Workflow | Trigger     | Coverage | Security   |
|----------|-------------|----------|------------|
| Smoke    | PR → main   | none     | none       |
| Quality  | push → main | ≥40%     | pip-audit  |
| Nightly  | schedule    | optional | optional   |

---

## 4. Implementation Details

### Coverage

- Raise `--fail-under=33` → `--fail-under=40` in Quality Tests
- Add `--cov-report=term` to pytest for visibility
- Upload `coverage.xml` as artifact

### Security

- Add step in Quality Tests (after install):
  ```bash
  pip install pip-audit
  pip-audit
  ```
- Fail CI if high/critical vulnerabilities detected
- Do not run pip-audit in Smoke

### Reproducibility

- Verify every pinned package in `requirements_versions.txt` matches installed version
- Skip unversioned packages (e.g. `torch`)
- Script: `scripts/ci/verify_pinned_deps.sh`

### CI Environment Artifact

- Capture after install:
  ```bash
  python --version
  pip --version
  pip freeze
  ```
- Output to `ci_environment.txt`, upload as artifact

---

## 5. Guardrails

- Repo: `GITHUB_REPOSITORY == m-cahill/serena`
- PR smoke: `GITHUB_BASE_REF == main`
- Push quality: `GITHUB_REF == refs/heads/main`

---

## 6. Invariants Preserved

| Invariant           | Verification              |
|---------------------|---------------------------|
| CLI                 | Smoke tests unchanged     |
| API schemas         | API tests unchanged       |
| Extension loading   | Unchanged                 |
| Generation semantics| Unchanged                 |
| CI truthfulness     | Coverage, security, deps  |

---

## 7. Definition of Done

- [ ] Smoke: pip-audit removed
- [ ] Quality: pip-audit added (fail on vuln)
- [ ] Quality: coverage gate 40%
- [ ] Quality: reproducibility check
- [ ] Quality: ci_environment.txt artifact
- [ ] Quality: coverage.xml artifact
- [ ] CI green (Smoke, Quality)
- [ ] Milestone docs complete
- [ ] Ledger updated
