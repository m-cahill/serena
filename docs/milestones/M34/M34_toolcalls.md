# M34 — Tool calls log

**Milestone:** M34 — Runtime context model-identity seam

| Timestamp (UTC) | Tool | Purpose | Target |
|-----------------|------|---------|--------|
| 2026-03-27 | Read / Grep | Classify `shared.sd_model` in `processing.py`; trace `RuntimeContext` / runner | `modules/processing.py`, `modules/runtime_context.py`, `modules/runtime/runner.py` |
| 2026-03-27 | Write | Add `ModelIdentity`, `model_identity_from_model`, extend `RuntimeContext`; wire `process_images_inner` | `modules/runtime_context.py`, `modules/processing.py` |
| 2026-03-27 | Write | Regression tests in `test_runtime_mock.py` | `test/quality/test_runtime_mock.py` |
| 2026-03-27 | Write | M34/M35 milestone docs; allowed-legacy note; `docs/serena.md` | `docs/**` |
| 2026-03-27 | Shell | `ruff check`; `pytest` (where env allows) | CI / local |
