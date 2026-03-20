# M20 Summary — Runtime tests with mockable boundaries

**Milestone:** M20  
**Phase:** Phase IV — Runtime Extraction (complete)  
**Audit score:** 5.0 / 5  
**Closed:** 2026-03-20 (UTC)

---

## What changed

- **`test/fixtures/fake_model.py`:** `FakeModel` and `FakeModelProvider` — minimal stand-ins for `shared.sd_model` metadata and `p.model_provider.get_model(p)` in the inner loop.
- **`test/quality/test_runtime_mock.py`:** Four integration tests driving **`ProcessingRunner.run(ProcessingRequest(p))`** → `process_images_inner` with test-only stubs (no real UNet/VAE/CLIP path): fake sampler returning `DecodedSamples`, no-op reload, minimal `setup_conds`, CPU-safe autocast/randn, optional `create_opts_snapshot` backfill for sparse CI `opts.data`, `do_not_reload_embeddings`, etc.
- **`docs/milestones/M20/`:** Canonical plan, tool log, CI run reports (run1 PR phase, run2 Quality).

**Production runtime modules** (`processing_runtime`, `sampler_runtime`, `decode_runtime`, `model_provider`, `runner`) were **not** modified for M20.

---

## Why it mattered

- Proves the **M16–M19 runtime stack** can execute end-to-end **without a real checkpoint or GPU**, using **injected `ModelProvider`** and deterministic test doubles.
- Validates **dependency inversion** in CI, not only by inspection.

---

## What remains

- **Phase V — UI & extension modularization** (M21+): shift focus from runtime extraction to UI tab registry, settings/extensions structure, and extension API contracts.

---

## Evidence

- Quality (M20 test fixes): [23333740069](https://github.com/m-cahill/serena/actions/runs/23333740069) @ `9c7e693a` — 87 passed, 40% coverage.  
- Quality (docs closeout): [23334408261](https://github.com/m-cahill/serena/actions/runs/23334408261) @ `fe5b794f` — 87 passed, 40% coverage.  
- Quality (ledger tip): [23334543220](https://github.com/m-cahill/serena/actions/runs/23334543220) @ `5f5fd8c0` — 87 passed, 40% coverage.  
- Tag **`v0.0.20-m20`** on **`9c7e693a`** (M20 test-fix tip; matches Quality **23333740069**).  
- PR: [#39](https://github.com/m-cahill/serena/pull/39) merged to `main`.
