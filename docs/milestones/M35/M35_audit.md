# M35 — Audit

**Milestone:** Remove tolerated `shared.sd_model` orchestration coupling  
**Scope:** Phase VIII — post–v1 recovery (`docs/serenav1audit.md`)

---

## Conclusion

**Pass.** M35 removes **supported-path** **direct** **`shared.sd_model`** orchestration reads from **`modules/processing.py`** by routing through **`_orchestration_model(p)`** → **`p.model_provider.get_model(p)`** after **`ProcessingRunner.prepare`**. **`StableDiffusionProcessing.sd_model`** remains **compatibility-only** residue (extensions / legacy callers), **not** orchestration authority. **`_orchestration_model`** still falls back to **`shared.sd_model`** when **`model_provider`** is absent.

**Runtime modules** (`processing_runtime`, `sampler_runtime`, `decode_runtime`) were **not** altered; they remain **provider-driven** only. **No** broad globals cleanup was attempted. **No** intentional user-visible behavior change; **no** CI policy or coverage-threshold change.

**CI:** PR gate on approved head **`564ebd27`** — Linter **`23673315409`**, Smoke **`23673315420`** (success). **Post-merge `main`** — Linter **`23673838902`**, Quality **`23673838908`** (success; **203** passed, **48%** TOTAL coverage in log). **`docs/architecture/serena_allowed_legacy_surfaces.md`** truthfully narrows the tolerated seam to compatibility / fallback surfaces.

---

## Risks / follow-ups

- **M36** — coverage lift and gate recalibration (program scope); **M37** — security deferrals / re-audit per ledger.
