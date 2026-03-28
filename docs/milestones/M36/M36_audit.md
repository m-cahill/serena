# M36 — Audit

**Milestone:** Coverage lift and gate recalibration  
**Scope:** Phase VIII — post–v1 recovery (`docs/serenav1audit.md`)

---

## Conclusion

**Pass.** M36 adds **targeted** quality tests that strengthen proof around **ModelProvider**, **`_orchestration_model`**, **RuntimeContext / ModelIdentity**, and **ProcessingRunner** / **ExecutionQueue** behavior — aligned with **M34–M35** refactor seams. **No** intentional user-visible behavior change; **no** CI weakening; **pytest-only** coverage policy unchanged.

**Measured outcome:** Binding post-merge **Quality** **`23677054515`** on **`main`** (**`ab4c4679`**) reports **213** tests passed and **48%** TOTAL coverage — in the **same band** as M35 (**203** / **48%**). The **Quality floor remains `42%`**; raising **`--fail-under`** was **not** justified by a jump into the mid/high 50s with comfortable margin.

**CI:** PR final head **`c410771f`** — Linter **`23676919831`**, Smoke **`23676919933`** (success). **Post-merge `main`** — Linter **`23677054517`**, Quality **`23677054515`** (success).

---

## What was strengthened (most to least)

1. **M35 orchestration seam** — **`_orchestration_model`**, **`SharedModelProvider`**, abstract **`ModelProvider`**, compatibility **`p.sd_model`**.
2. **M34 identity seam** — **`ModelIdentity`** equality/hash, **`RuntimeContext`** field contract.
3. **Runner / queue** — **`ProcessingRequest`**, **`runtime_metrics`** normalization, **`ExecutionQueue.submit`**.

---

## Risks / follow-ups

- **M37** — security deferral closure and final 5/5 re-audit per ledger (`docs/milestones/M37/`).
