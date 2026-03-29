# M38 tool calls

| Timestamp (UTC) | Tool | Purpose | Files |
|-----------------|------|---------|-------|
| 2026-03-28 | branch | Start M38 | `m38-processing-class-helper-decomposition` |
| 2026-03-28 | write | Milestone plan + toolcalls | `M38_plan.md`, `M38_toolcalls.md` |
| 2026-03-28 | refactor | Extract classes/helpers | `modules/processing_types.py`, `processing_helpers.py`, `processing_infotext.py`, slim `processing.py` |
| 2026-03-28 | write | M38 import-surface tests | `test/quality/test_processing_m38_import_surface.py` |
| 2026-03-28 | write | M39 milestone stubs | `docs/milestones/M39/M39_plan.md`, `M39_toolcalls.md` |
| 2026-03-28 | config | Ruff per-file-ignores for split | `pyproject.toml` |
| 2026-03-29 | merge | PR **#94** → `main` **`17c21be6`** (merge commit); post-merge CI | GitHub Actions |
| 2026-03-29 | write | M38 closeout: `M38_run1.md`, `M38_summary.md`, `M38_audit.md`; `M38_plan.md` status; `serena.md`; M39 stubs | `docs/milestones/M38/`, `docs/milestones/M39/`, `docs/serena.md` |
