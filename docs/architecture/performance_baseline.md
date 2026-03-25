# Performance baseline (M29)

**Purpose:** Make generation and API latency **observable** without changing behavior or adding blocking performance gates.

## What is measured

| Location | Metric | Storage |
|----------|--------|---------|
| **`ProcessingRunner`** | Wall time inside **`execute()`** (`process_images_inner`) | **`ProcessingRequest.runtime_metrics["execute_time"]`** (seconds) |
| **`ProcessingRunner`** | Wall time for full **`run()`** (prepare → execute → finalize) | **`ProcessingRequest.runtime_metrics["runtime_total_time"]`** |
| **`StableDiffusionProcessing`** | Same dict (reference) | **`p.runtime_metrics`** after **`process_images()`** |
| **REST API** (`/sdapi/v1/txt2img`, `/sdapi/v1/img2img`) | Full handler wall time | **`logging.debug`**; last value in **`modules.api.api._m29_last_request_seconds`** (`txt2img` / `img2img` keys) |

No user-facing API or response schema changes are introduced for timing.

## CI artifact: `performance_snapshot.txt`

Quality tests write **`performance_snapshot.txt`** at the repository root when **`test_performance_baseline.py`** runs successfully. It contains sample **`execute_time`** / **`runtime_total_time`** and environment hints (Python version, platform).

- **Non-blocking:** CI does **not** fail on slow runs.
- **Variability:** Numbers depend on **CPU vs GPU**, **load**, **torch build**, and **cache** state. Treat snapshots as **ordinal** comparisons over time, not absolute SLAs.

## Non-deterministic factors

- Hardware (GPU memory, CPU cores, thermal throttling)
- First-run vs warm cache (model load, CUDA kernels)
- CI `ubuntu-latest` vs developer machines
- Concurrent jobs on shared runners

## Follow-up (later milestones)

- M30+: optional **trend** reporting or **regression alerts** when baselines drift **significantly** (still **non-blocking** until explicitly adopted).
