# M39 — Audit

**Milestone:** Remaining legacy surface narrowing  
**Scope:** Phase IX — internal score-lift (opts snapshot seam narrowing)

---

## Conclusion

**Pass (PR gate).** M39 is a **behavior-preserving** narrowing of direct **`shared.opts`** reads on **Serena-managed execution paths** that run after **`p.opts_snapshot`** is established in **`process_images_inner`**, using **`_eff_opts(p)`** as the single routing seam.

- **`StableDiffusionProcessing.sd_model`** was **not** removed; **`_orchestration_model`** fallback semantics **unchanged**.
- **Runtime modules** still take the model only via **`ModelProvider`** inside **`processing_runtime`** / **`sampler_runtime`** / **`decode_runtime`** (M19); M39 only adjusted **opts** reads at the **`processing_runtime`** preview gate to use **`_eff_opts(p)`**, not model globals.
- **CI policy** unchanged (no gate relaxation).

**Binding PR CI:** head **`eee9af2a927208b78173252fdcfd6fd56313e13e`** — **`pull_request`** Linter **`23719147857`**, Smoke **`23719147871`** — **success**.

**Post-merge `main` Quality:** fill in **`M39_run1.md`** §B after merge (expected: **≥217** tests, **≥42%** gate, **~48%** TOTAL band).

---

## Eliminated vs remaining (allowed legacy)

| Item | After M39 |
|------|-----------|
| Direct **`shared.opts`** in **`processing_types.py`** / listed **`processing_infotext`** / **`processing.py`** overlay / **`processing_runtime`** preview condition | **Removed** (routed via **`_eff_opts`**) |
| **`create_opts_snapshot(shared.opts)`** in **`process_images_inner`** | **Remains** — snapshot capture |
| **`_eff_opts`** fallback when no snapshot | **`shared.opts`** — documented |
| **`StableDiffusionProcessing.sd_model`** property | **Compatibility residue** — unchanged |
| Broad **`opts.`** alias reads across **`processing_types`** | **Out of scope** — not a second **`shared.opts`** string |

---

## Risks / follow-ups

- **M40** — coverage wave on legacy/high-value modules — see **`docs/milestones/M40/M40_plan.md`**.
