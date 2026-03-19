# M18 Toolcalls

## Context

Milestone: M18 — Decode / save separation  
Phase: Phase IV — Runtime Extraction

## Actions

| Timestamp | Tool | Purpose | Files | Status |
|-----------|------|---------|-------|--------|
| (init) | — | Milestone folder seeded at M17 closeout | docs/milestones/M18/ | done |
| 2026-03-19T22:10Z | git | Create/switch branch m18-decode-save-separation | repo root | done (branch existed) |
| 2026-03-19T22:10Z | write | Add decode_runtime (decode_latents, postprocess, save, moved decode_latent_batch) | modules/runtime/decode_runtime.py | done |
| 2026-03-19T22:10Z | apply_patch | Wire process_images_inner to decode_runtime; import decode_latent_batch from runtime | modules/processing.py | done |
| 2026-03-19T22:10Z | write | Add M18 quality tests (delegation, order, decode_latents passthrough) | test/quality/test_decode_runtime.py | done |
| 2026-03-19T22:15Z | shell | Run pytest on test_decode_runtime.py | test/quality | done |
| 2026-03-19T22:25Z | shell | ruff check on changed runtime/processing/test files | modules/, test/quality | done (decode_runtime clean) |
| 2026-03-19T22:42Z | git | Commit M18 (amend: drop unused save_outputs_for_row arg) | repo | done |
| 2026-03-20T00:00Z | git | Push m18-decode-save-separation to origin | repo | in progress |
| 2026-03-20T00:00Z | shell | Watch gh workflow run for M18 push; collect run id | GitHub Actions | in progress |

---

## Notes

* M18 follows M17: decode/save extraction behind runtime boundary
* Baseline: M17 merge (sampler_runtime)
