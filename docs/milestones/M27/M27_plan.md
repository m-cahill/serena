# M27 — Coverage & complexity gates

**Status:** Completed  
**Branch:** `m27-coverage-complexity-gates` → `main`; measurement fix **`m27-coverage-measurement-fix`** (**PR #63**)

## 1. Intent

Strengthen quality guarantees by:

- Incrementally raising the **coverage floor** (Quality CI only).
- Adding **cyclomatic complexity visibility** via **Radon** on `modules/` (warn-only for D/E/F).
- Preserving **no runtime / API / UI behavior change**.

## 2. Scope

### In scope

- Quality workflow only: **`.github/workflows/run_quality_tests.yaml`**
- `--fail-under=42` (was 40)
- Coverage: keep `coverage report`, `coverage.xml`, `htmlcov/` uploads
- `pip install radon` → `radon cc modules -s -a > radon_report.txt` → upload artifact
- If report contains complexity grade **D, E, or F**: emit `::warning` (do **not** fail job)
- Docs: `docs/architecture/ci_environment_contract.md`, `docs/PR_guardrail_checklist.md`
- **If** coverage &lt; 42%: add **minimal** tests (contract / runner / API seams only); **do not** lower gate

### Out of scope

- Smoke, Linter, Nightly workflows
- GitHub Actions **job summary** / markdown summaries (deferred, e.g. M30)
- CI failure on complexity; refactors to reduce complexity
- Dependency upgrades (M28)
- Runtime, extension API, or UI changes

## 3. Locked decisions

| Topic | Decision |
|--------|----------|
| Plan / toolcalls | Canonical under `docs/milestones/M27/` |
| Radon warn rule | **≥ D only** (warn on **D, E, F**; not A/B/C) |
| Radon path | **`modules/`** only |
| Workflow edits | **`run_quality_tests.yaml` only** |
| Branch | `m27-coverage-complexity-gates` |
| Toolcalls | **Strict:** log before significant tool use |

## 4. Verification

- Quality CI green on PR
- Coverage ≥ **42%**
- Test count baseline **~112+** (no accidental drop)
- Artifact **`radon_report.txt`** present
- No CI weakening (no `continue-on-error` on gates, no lowered thresholds)

## 5. Definition of done

- [x] `M27_plan.md` / `M27_toolcalls.md` present
- [x] Workflow updated (42% gate + Radon + warning + artifact; **PR #63** pytest-only measurement)
- [x] Docs updated (`ci_environment_contract.md`, `M27_run1.md`, `M27_summary.md`, `M27_audit.md`, ledger)
- [x] Quality CI green on **`main`**; evidence in `M27_run1.md` (**run 23513449859**)
- [x] Tag **`v0.0.27-m27`** on M27 closeout commit (includes summary/audit/ledger; **PR #63** merge is **`e3c0d554`**)

## 6. Rollback

- Revert `--fail-under` to 40 and remove Radon steps if needed
