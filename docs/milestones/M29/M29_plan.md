# M29 — Health & Performance Verification

## Objective

Make Serena **observable and regression-resistant** via lightweight timing instrumentation (measurement only, no optimization).

## Locked decisions

- **Milestone folder:** `docs/milestones/M29/` with plan + toolcalls (`.cursorrules`).
- **`performance_snapshot.txt`:** CI artifact only; not committed; optional sample text in docs.
- **API exposure:** DEBUG logging / internal timing only; JSON responses unchanged (byte-for-byte contract).
- **Runner metrics:** `p.runtime_metrics = { "execute_time", "total_time" }` on existing processing object `p`.
- **Branch:** `m29-health-performance-verification` → PR to `m-cahill/serena:main`.

## Constraints

- No CI failure on performance; no profiling frameworks; `time.perf_counter()` / `time.time()` only.
- Coverage floor **≥42%** unchanged; no API/extension semantic changes.
- No dependency changes for M29 scope.

## Definition of done

- [x] `ProcessingRunner` records `execute_time` and `total_time` on `p.runtime_metrics`.
- [x] API txt2img/img2img handlers log wall time at DEBUG (non–user-facing).
- [x] Quality test asserts metrics exist (no strict thresholds).
- [ ] CI generates and uploads `performance_snapshot.txt` — **pending green Quality** (see `M29_run1.md`).
- [x] `docs/architecture/performance_baseline.md` documents baselines and caveats.
