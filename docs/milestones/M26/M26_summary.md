# M26 Summary — Locked manifests & CI environment stabilization

**Milestone:** M26  
**Phase:** Phase VI — Hardening & Reproducibility  
**Audit score:** 5.0 / 5  
**Closed:** 2026-03-23 (UTC)

---

## What changed

- **`requirements-ci.txt` / `requirements-ci.in`:** Single committed Python manifest for Quality CI (`uv pip compile` lock).
- **Quality workflow:** Install from lockfile; **OpenAI CLIP** from **pinned GitHub archive** + `pip install --no-build-isolation` (documented exception).
- **npm determinism:** Committed **`package-lock.json`**, **`.gitignore`** fix; Linter uses **`npm ci`** and uploads **`npm_ls`** / dependency listing artifact.
- **`verify_pinned_deps.sh`:** Extended for lockfile + **`dependency_snapshot.txt`**; runs **before** `pip-audit` in the workflow order.
- **Reproducibility artifacts:** **`pip_freeze.txt`**, **`dependency_snapshot.txt`**, **`ci_environment.txt`**, **`pip_audit_report.txt`**, coverage uploads.
- **Governance docs:** **`docs/architecture/ci_environment_contract.md`**, **`docs/PR_guardrail_checklist.md`** updates.
- **Key decision — `pip-audit`:** **Informational** for **M26–M27** (warning + artifact, non-blocking); **strict enforcement deferred to M28** so visibility and policy stay explicit without silent gate weakening.

**Not changed:** Runtime modules, extension API surface, invocation order, **`fail-under=40`** coverage gate, or product behavior.

---

## Why it mattered

- **Deterministic Quality installs** from a committed lock reduce “works on runner” drift.
- **Artifact-level evidence** makes the CI environment **auditable and reproducible** on paper.
- **Explicit pip-audit policy** preserves **CI truthfulness**: findings are visible; enforcement is governed, not accidentally relaxed.

---

## What remains

- **M27:** Coverage and complexity gates (planning).
- **M28:** Supply-chain enforcement (`pip-audit` blocking) and controlled upgrades.

---

## Evidence

- PRs [#45](https://github.com/m-cahill/serena/pull/45)–[#53](https://github.com/m-cahill/serena/pull/53) (range per ledger; includes fix chain).
- Binding Quality: [23467772232](https://github.com/m-cahill/serena/actions/runs/23467772232) — **success**, **112 passed**, **40%** combined coverage (gate).
- Linter: [23421937195](https://github.com/m-cahill/serena/actions/runs/23421937195); Smoke: [23421937182](https://github.com/m-cahill/serena/actions/runs/23421937182).
- Implementation merge reference: **`676924349c3a296e8ef07ef09a588b472498e7fd`** (`67692434`).
- Tag **`v0.0.26-m26`** (annotated) on **`main` tip** after this closeout merges — Quality binding merge **`676924349c3a296e8ef07ef09a588b472498e7fd`** (`67692434`); see ledger **Commit** column.
