# M29 — Summary: Health & performance verification

## Delivered (merged)

1. **Runner metrics** — `ProcessingRunner` records on `p.runtime_metrics`:
   - `execute_time` — `execute` phase (`perf_counter`)
   - `total_time` — full `run()` (prepare → finalize)
2. **API** — `text2imgapi` / `img2imgapi` wall time logged at **DEBUG** only; **no** JSON/schema changes.
3. **Quality test** — `test/quality/test_performance_baseline.py` (metrics present; no strict thresholds).
4. **CI** — `scripts/ci/write_performance_snapshot.py` + workflow step + artifact upload intent; `performance_snapshot.txt` **gitignored**.
5. **Docs** — `docs/architecture/performance_baseline.md`, milestone plan/toolcalls.

## Follow-up dependency / CI fixes (post–#64)

To restore **pip-audit** and **import/runtime** consistency on Quality, `main` also picked up:

- **requests** 2.33.0 (CVE-2026-25645)
- **torch** 2.2.2+cpu / **torchvision** 0.17.2+cpu (needed for **transformers** 4.57 + `torch.utils._pytree` APIs)
- **scikit-image** 0.25.x (NumPy 2 wheel ABI)
- **Gradio 6** compatibility shims: `gr.deprecation` guard in `ui.py`; **Button** `tooltip` handling in `gradio_extensons.py`

## Outstanding

- **Binding Quality green** and **`performance_snapshot.txt` artifact** from a **successful** run are **pending** until **Gradio 6** **`.click(_js=...)`** (and any further 6.x API gaps) are addressed **without** dropping **Pillow ≥12**.

## Behavior drift

- **Intent:** measurement-only for M29 metrics; **no** user-facing API response changes.
- **CI stack:** torch / torchvision / scikit-image / requests changes affect **CI install tree**, not application JSON contracts.
