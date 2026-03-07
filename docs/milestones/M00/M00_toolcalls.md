# M00 Tool Calls Log

| Timestamp | Tool | Purpose | Files/Target | Status |
|-----------|------|---------|--------------|--------|
| 2025-03-06 | read_file | Read .cursorrules, serena.md, audits | docs/*.md, .cursorrules | done |
| 2025-03-06 | run_terminal_cmd | git tag baseline-pre-refactor | - | done |
| 2025-03-06 | run_terminal_cmd | git checkout -b m00-kickoff-baseline-e2e | - | done |
| 2025-03-06 | write | Create M00_preflight.md | docs/milestones/M00/M00_preflight.md | done |
| 2025-03-06 | write | Create M00_plan.md | docs/milestones/M00/M00_plan.md | done |
| 2025-03-06 | write | Update docs/serena.md | docs/serena.md | done |
| 2025-03-06 | write | Create M00_e2e_baseline.md | docs/milestones/M00/M00_e2e_baseline.md | done |
| 2025-03-06 | write | Create M00_ci_inventory.md | docs/milestones/M00/M00_ci_inventory.md | done |
| 2025-03-06 | run_terminal_cmd | ruff . (ruff==0.3.3) | Python lint | done (PASS) |
| 2025-03-06 | run_terminal_cmd | npm run lint | JS lint | done (FAIL on Windows CRLF; CI passes) |
| 2025-03-06 | run_terminal_cmd | pytest test/ | Full test suite | skipped (requires server) |
| 2025-03-06 | write | Helper scripts | scripts/dev/run_m00_baseline_e2e.ps1, .sh | done |
