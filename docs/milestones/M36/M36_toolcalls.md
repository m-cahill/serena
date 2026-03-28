# M36 — Tool calls log

**Milestone:** M36 — Coverage lift and gate recalibration

| Timestamp (UTC) | Tool | Purpose | Target |
|-----------------|------|---------|--------|
| 2026-03-28 | — | Stub seeded at M35 closeout | `M36_plan.md`, this file |
| 2026-03-28T14:00:00Z | Write/StrReplace | M36 Wave A: provider/orchestration + runtime context unit tests; toolcalls header | `test_model_provider.py`, `test_runner_queue_mode.py`, `test_processing_runner.py`, `M36_toolcalls.md` |
| 2026-03-28T14:00:00Z | Shell | Create branch `m36-coverage-lift-gate-recalibration`, run pytest coverage slice | git, pytest |
| 2026-03-28T14:30:00Z | Write | M36 plan/run1, M37 stubs; gate policy documented (measure before bump) | `M36_plan.md`, `M36_run1.md`, `M37_plan.md`, `M37_toolcalls.md` |
| 2026-03-28T14:30:00Z | Git | Stage M36 tests + docs | working tree |
| 2026-03-28T04:15Z | Shell / Write | Merge PR #92; poll Quality `23677054515`; closeout `serena.md`, `M36_*`, `M37_*` | `gh`, milestone docs |
