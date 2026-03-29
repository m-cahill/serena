# M39 — Audit

**Milestone:** Remaining legacy surface narrowing  
**Scope:** Phase IX — allowed-legacy **`shared.opts`** narrowing on Serena-managed execution paths

---

## Conclusion

**Pass.** M39 **narrowed** the remaining **direct `shared.opts`** reads on supported paths by routing through **`_eff_opts(p)`** ( **`_EffOptsView`** + **`shared.opts`** fallback for missing snapshot keys). The work stayed **milestone-scoped**: **not** a broad global-state cleanup; **`StableDiffusionProcessing.sd_model`** remains **compatibility-only** residue; **`create_opts_snapshot(shared.opts)`** remains the **intentional** capture point. **No** intended behavior change for full **`opts.data`** snapshots; **CI policy** unchanged.

**Merge:** PR **#95** — merge commit **`d4551e6d55c31c5f6b1efd0a5d04956a19d0ea53`** (**2026-03-29T21:45:43Z**), method **merge commit**.

**PR approval basis:** head **`0aa0d93d4df894aaef841c0c0f425c75ab3ba8d6`** — Linter **`23719443302`**, Smoke **`23719443311`** — **success** (pre-merge **`M39_run1.md`** §A **lagged**; see **`M39_run1.md`** §A note).

**Post-merge:** first **`push`** on **`d4551e6d`** — Quality **`23719815660`** **failed** (sparse **`opts_snapshot`** in **`test_runtime_mock`**). **Follow-up** **`main`** tip **`1b9f304efef050b107435d526bade735bf762bcc`** — Linter **`23719932253`**, Quality **`23719932254`** — **success**; **222** passed; **48%** TOTAL coverage.

---

## Truth requirements (met)

| Statement | Status |
|-----------|--------|
| Narrowed allowed-legacy surface on Serena-managed paths | **Yes** — direct **`shared.opts`** removed from listed modules; routing via **`_eff_opts`** |
| Limited to owned seams; not broad globals cleanup | **Yes** |
| **`sd_model`** compatibility property | **Unchanged** — documented residue |
| **`create_opts_snapshot(shared.opts)`** | **Intentional** capture |
| No behavior change intended (full snapshots) | **Yes**; sparse snapshot fallback matches prior direct global reads in tests |
| CI truthful; policy unchanged | **Yes** — gates and workflows unchanged |

---

## Risks / follow-ups

- **M40** — coverage wave on legacy/high-value modules — **`docs/milestones/M40/M40_plan.md`**.
