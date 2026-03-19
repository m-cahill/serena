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
| 2026-03-20T00:00Z | git | Push m18-decode-save-separation to origin | repo | done |
| 2026-03-20T00:00Z | shell | Watch gh workflow run for M18 push; collect run id | GitHub Actions | done |
| 2026-03-19T22:50Z | gh | Open PR #36 to main (trigger Smoke + PR Linter) | GitHub | done |
| 2026-03-19T22:52Z | gh | Watch Smoke 23320478834 + PR Linter 23320478855 | GitHub Actions | done |
| 2026-03-19T23:00Z | write | M18_run1.md workflow analysis; update serena ledger | docs/milestones/M18/, docs/serena.md | done |
| 2026-03-19T23:00Z | git | Commit and push M18_run1 + ledger | repo | done |
| 2026-03-19T23:15Z | shell | Watch CI for doc tip 5c4613f5; refresh M18_run1 run IDs | GitHub Actions, docs | done |
| 2026-03-19T23:18Z | git | Amend run1 + serena for PR tip 5c4613f5 run IDs | docs | done |
| 2026-03-19T23:04Z | gh | Merge PR #36 to main (M18 approved closeout) | GitHub | done |
| 2026-03-19T23:08Z | gh | Watch Quality Tests 23321103961 on main | GitHub Actions | done |
| 2026-03-19T23:15Z | write | M18_run2, M18_summary, M18_audit; serena completed row; M19 seed | docs/ | done |
| 2026-03-19T23:20Z | git | Commit closeout on main; tag v0.0.18-m18 | repo | done |
| 2026-03-20T12:00Z | shell | Restore UTF-8 punctuation in `docs/serena.md` (post-closeout encoding drift) | docs/serena.md | done |
| 2026-03-20T12:00Z | git | Commit 4fd332bc; move `v0.0.18-m18` to include ledger fix | repo | done |

---

## Notes

* M18 follows M17: decode/save extraction behind runtime boundary
* Baseline: M17 merge (sampler_runtime)
