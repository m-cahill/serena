# M36 — Coverage lift and gate recalibration

**Phase VIII** · **Status:** Planned (stub — kickoff after M35 closeout)

**Depends on:** M35 complete; binding Quality on `main` as program proof surface.

---

## Intent / target

**Targeted** test/coverage improvements and **truthful** alignment of the Quality coverage gate with measured pytest-only coverage — per program roadmap (`docs/serena.md`) and Phase VIII scope. **No** unrelated refactors, **no** CI weakening, **no** broad global-state cleanup.

---

## Scope boundaries

**In scope**

- Increase meaningful coverage where gaps are honest and low-risk.
- Recalibrate gate only with evidence (measurement governance per `ci_environment_contract.md`).
- Milestone docs: `M36_run1.md`, summary, audit.

**Out of scope**

- M35-style orchestration work; runtime boundary changes; security deferral closure (M37); arbitrary threshold drops.

---

## Authority

- `docs/serena.md`
- `docs/architecture/ci_environment_contract.md`
- `docs/serenav1audit.md` (coverage as remaining gap)

---

## Deliverables (at kickoff)

- Plan refinement from this stub  
- `M36_toolcalls.md` log  
- Code/tests only as scoped by the refined plan
