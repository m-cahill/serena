# M35 — Tool calls log

**Milestone:** M35 — Remove tolerated `shared.sd_model` orchestration coupling

| Timestamp (UTC) | Tool | Purpose | Target |
|-----------------|------|---------|--------|
| 2026-03-27 | — | Stub seeded at M34 implementation | `M35_plan.md`, this file |
| 2026-03-27 | Write | M34 closeout — narrow M35 plan scope (orchestration coupling only) | `M35_plan.md` |
| 2026-03-28T00:00:00Z | Shell | Record authoritative base SHA for M35 branch; verify main tip | `5e7cc6656152940771e4b91af8eb8f334be078dc` |
| 2026-03-28T00:00:01Z | Grep/Read | Inventory `shared.sd_model` and orchestration sites in `processing.py` | `modules/processing.py` |
| 2026-03-28T00:30:00Z | StrReplace | Add `_orchestration_model`, replace direct `shared.sd_model` reads; document `sd_model` property | `modules/processing.py` |
| 2026-03-28T00:30:01Z | StrReplace | M35 regression test: identity from provider when `shared.sd_model` mismatched | `test/quality/test_runtime_mock.py`, `test/fixtures/fake_model.py` |
| 2026-03-28T00:30:02Z | Write | Allowed-legacy + M35 plan + run1 stub | `docs/architecture/serena_allowed_legacy_surfaces.md`, `docs/milestones/M35/M35_plan.md`, `M35_run1.md` |
| 2026-03-28T00:30:03Z | StrReplace | Cross-reference M35 on `ModelProvider` | `modules/runtime/model_provider.py` |
