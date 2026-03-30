# Performance baseline (M29)

## Purpose

Serena records **lightweight timing** for the processing runner and logs API handler wall time at **DEBUG** — measurement only, not optimization targets.

## Runner metrics

`ProcessingRunner` sets on the processing object `p`:

| Key            | Meaning                                      |
| -------------- | -------------------------------------------- |
| `execute_time` | Seconds in the `execute` phase (`perf_counter`) |
| `total_time`   | Seconds for full `run()` (prepare through finalize) |

Values are **non-deterministic** across machines (CPU vs GPU, load, thermal throttling, CI virtualization).

## API timing

`text2imgapi` / `img2imgapi` log handler wall time at **DEBUG** when not using the CI fake inference path. JSON responses and schemas are **unchanged**; contract tests are unaffected.

## CI artifact

Quality workflow generates **`performance_snapshot.txt`** (not committed) and uploads it as an artifact. Example shape:

```text
# Serena performance_snapshot (M29)
generated_utc=...
python=3.10.x
platform=...
sample_runner_execute_time_s=...
sample_runner_total_time_s=...
```

Use snapshots to compare **trends** on the same runner class, not as absolute SLAs.

## Non-deterministic factors

- Hardware (GPU memory bandwidth, CPU cores)
- Concurrent jobs on shared CI hosts
- Torch / CUDA / driver versions (see `ci_environment_contract.md` for the Quality manifest)

M29 does **not** fail CI on performance by itself; **M41** adds a **warn-first** regression check (see below).

## M41 — Regression warnings (Quality)

After **`performance_snapshot.txt`** is written, **`scripts/ci/check_performance_regression.py`** compares **`sample_runner_execute_time_s`** and **`sample_runner_total_time_s`** to committed anchors in **`scripts/ci/performance_snapshot_baseline.txt`**. If either metric exceeds the baseline by more than **20%** (configurable ratio in the script), the workflow prints a **`::warning`** annotation. The job **still succeeds**; this is **not** a blocking SLO.

**Updating the baseline:** Change **`performance_snapshot_baseline.txt`** only when the probe (`write_performance_snapshot.py`) or runner timing semantics change intentionally—not to silence noise from CI load variance without cause.
