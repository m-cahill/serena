# 📌 Milestone Summary — M41: Performance SLOs and regression guardrails (final Phase IX)

**Project:** Serena  
**Phase:** Phase IX — Internal score-lift (M38–M41)  
**Milestone:** M41 — Performance SLOs and regression guardrails  
**Timeframe:** 2026-03-30 UTC  
**Status:** **Closed**

---

## 1. Milestone Objective

Close Phase IX by adding a **truthful, non-blocking** performance regression signal on Quality (compare `performance_snapshot.txt` to a committed baseline), harden GitHub Actions with explicit token permissions and artifact visibility, align Nightly `pip-audit` with governed Quality deferrals, improve fork discoverability (README, `opts_snapshot.py` comment), and apply a **narrow** exception-type cleanup on Serena-governed `processing.py` — **without** weakening CI gates or promoting a flaky blocking SLO.

---

## 2. Scope Definition

### In Scope

- `scripts/ci/check_performance_regression.py`, `scripts/ci/performance_snapshot_baseline.txt`
- `test/quality/test_performance_regression_guard.py`
- `.github/workflows/*.yaml` — `permissions`, Quality performance-check step, Smoke/Nightly JUnit uploads, Nightly `pip-audit` alignment
- `README.md`, `modules/opts_snapshot.py`, `modules/processing.py` (single `ValueError` change)
- `docs/architecture/ci_environment_contract.md`, `docs/architecture/performance_baseline.md`
- Milestone docs under `docs/milestones/M41/`, ledger updates in `docs/serena.md`

### Out of Scope

- Blocking performance gate; broad exception refactors; bare `except:` in upstream training code; `sd_models.py` / `sd_vae.py` generic-raise cleanup; branch-coverage gate; `processing_types.py` split

---

## 3. Work Executed

| Action | Detail |
|--------|--------|
| **PR [#103](https://github.com/m-cahill/serena/pull/103)** | Warn-first regression script + baseline; workflow permissions; Nightly/Smoke artifacts; README; docs; **`ValueError`** in **`process_images_inner`** refiner branch |
| **Tests** | **3** new Quality tests for snapshot parse / regression helper (importlib load of CI script) |
| **Mechanical vs semantic** | **Semantic (narrow):** **`ValueError`** for missing refiner checkpoint — callers catching **`Exception`** still match |

---

## 4. Validation & Evidence

| Layer | Result |
|-------|--------|
| **PR #103** | Linter **`23728560305`** **success**; Smoke **`23728560308`** **success**; head **`5efdcc83`** |
| **`main` post-merge** | Linter **`23728637287`** **success**; Quality **`23728637285`** **success** — **246 passed**, **49%** TOTAL (pytest-only), **`--fail-under=42`** **passed** |
| **Performance step** | **Check performance regression (M41 warn-first)** **success**; **warn-first** posture confirmed (no job failure on regression script) |

---

## 5. CI / Automation Impact

| Change | Effect |
|--------|--------|
| **Quality** | New step after **`write_performance_snapshot.py`** — **informational warnings only** (`::warning` on >20% vs baseline); **exit 0** |
| **Nightly** | **`pip-audit`** **blocking** with same **`--ignore-vuln`** as Quality; not a PR merge gate (schedule / manual) |
| **Permissions** | **`contents: read`** + **`actions: write`** where artifacts upload |

---

## 6. Issues & Exceptions

| Issue | Resolution |
|-------|------------|
| **None** blocking | No new issues were introduced during this milestone. |

---

## 7. Deferred Work

- **M42** (conditional): remove **`pip-audit`** ignores when PyPI ships fixes for **CVE-2025-69872** / **CVE-2026-4539** — **unchanged**; not required for program closeout
- **Blocking performance SLO** — **explicitly deferred**; warn-first is **final** M41 posture per evidence

---

## 8. Governance Outcomes

- **Provable:** Quality emits **workflow warnings** when probe metrics exceed baseline by **>20%**; baseline is **committed** and documented
- **Provable:** **Nightly** no longer masks **`pip-audit`** with **`|| true`** for the same install phase; deferrals **documented** in **`ci_environment_contract.md`**
- **Provable:** **246** Quality tests, **49%** TOTAL, **42%** gate **unchanged**

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
|-----------|-----|
| Truthful performance guardrail | **Met** — script + baseline + tests |
| No CI weakening | **Met** — gates unchanged |
| Workflow / doc polish | **Met** |
| Binding **main** Quality green | **Met** — **`23728637285`** |

---

## 10. Final Verdict

**Milestone objectives met.** Phase IX complete; **M41** is the **final** planned Serena milestone (see **`docs/serena.md`**).

---

## 11. Authorized Next Step

**No further milestone is authorized** under the Serena refactor program. Optional **M42** remains **conditional** on upstream PyPI fixes only.

---

## 12. Canonical References

- **Implementation PR:** https://github.com/m-cahill/serena/pull/103  
- **Implementation merge:** `8e7736f0b53c93fe13f0aab4e3cc7d188acc2408`  
- **Implementation commit:** `5efdcc83e76081e55194e727367fd7ddf37d7216`  
- **Binding Quality (implementation):** run **`23728637285`**  
- **Doc closeout PR:** https://github.com/m-cahill/serena/pull/104  
- **Doc merge / current `main` tip (ledger + M41 bundle):** `4cccde03e6714e039ca9b4470898c7d0b0df6421`  
- **Binding Quality (post–#104):** run **`23728891097`**  
- **Docs:** `M41_plan.md`, `M41_run1.md`, `M41_summary.md`, `M41_audit.md`, `docs/serena.md`
