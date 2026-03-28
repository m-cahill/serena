# M36 — Coverage lift and gate recalibration

**Phase VIII** · **Status:** **Complete** (2026-03-28 UTC)

**Depends on:** M35 complete; binding Quality on `main` run **`23673838908`** (post-merge **`45e6f4fb`**).

---

## Intent / target

Raise **pytest-only** coverage with **targeted, behavior-locking** tests on high-value refactor seams (M34–M35 runtime/provider/orchestration), then **recalibrate** the Quality `--fail-under` threshold **only** when post-merge measured coverage shows a **safe margin** (≥~2 points above the new floor). **No** CI weakening; **no** launch-time coverage inflation (`ci_environment_contract.md`).

---

## Baseline (authoritative “before”)

| Item | Value |
|------|--------|
| Binding Quality run | **`23673838908`** |
| Tests passed | **203** |
| Reported TOTAL coverage | **~48%** |
| Enforced floor | **42%** (`run_quality_tests.yaml` → `coverage report --fail-under=42`) |

Local reproduction of the 48% figure is **not** required for planning; M35 post-merge Quality is the ledger baseline.

---

## Scope boundaries

**In scope**

- Tests for **`ModelProvider` / `SharedModelProvider`**, **`_orchestration_model`**, **`RuntimeContext` / `ModelIdentity`**, runner/queue edges aligned with locked boundaries.
- Reuse **`test_runtime_mock.py`** patterns and **`initialize`** where imports require the full stack.
- One **PR** (`m36-coverage-lift-gate-recalibration`); internal **waves** (Wave A provider/orchestration; Wave B runtime identity + runner metrics/queue; optional Wave C only if needed).
- **`M36_run1.md`**, **`M36_toolcalls.md`**, plan updates; closeout docs after merge and green Quality.

**Out of scope**

- Runtime redesign, `ProcessingRunner` ownership changes, M37 security deferrals.
- Broad rewrites, synthetic coverage, or lowering gates.

---

## Priority order (locked)

1. **ModelProvider** behavior and **`_orchestration_model`** fallback vs provider path (M35).
2. **`RuntimeContext` / `ModelIdentity`** invariants (M34).
3. **Selective** deterministic helpers / runner edges only if high-yield (e.g. `ExecutionQueue`, `runtime_metrics` normalization).

---

## Gate policy

- **Do not** raise `--fail-under` ahead of measured CI totals.
- If post-merge TOTAL remains in the low 50s with thin margin over 42%, **leave the gate at 42%** and record the rationale in **`M36_summary.md` / `M36_run1.md`**.
- If measured coverage is **mid–high 50s+** with comfortable margin, raise the gate in the **smallest** justified step (e.g. toward **48–52%**), consistent with program buffer rules.

---

## Deliverables

- [x] Branch **`m36-coverage-lift-gate-recalibration`** merged via **PR #92** (Linter + Smoke green on merge tip **`c410771f`**).
- [x] Post-merge Quality on **`main`** green (**`23677054515`**); **`M36_run1.md`** records before/after; **gate unchanged** at **42%**.
- [x] **`M36_summary.md`**, **`M36_audit.md`**; **`docs/serena.md`** updated.
- [x] **`docs/milestones/M37/`** plan + toolcalls (M37 not implemented in M36).

---

## Authority

- `docs/serena.md`
- `docs/architecture/ci_environment_contract.md`
- `docs/architecture/serena_architecture_lock.md`, `serena_allowed_legacy_surfaces.md`
