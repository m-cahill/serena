# M30 — Tool calls log

**Milestone:** M30 — QA / evidence publishing (documentation only)

| Timestamp (UTC) | Tool | Purpose | Target |
|-----------------|------|---------|--------|
| 2026-03-26 | branch | Start M30 worktree | `m30-qa-evidence-publishing` |
| 2026-03-26 | read / glob | Cross-check M26–M29 milestone docs vs ledger | `docs/milestones/M26`–`M29`, `docs/serena.md` |
| 2026-03-26 | gh | Resolve M28/M29 Quality run IDs on `m-cahill/serena` | `gh run list --repo m-cahill/serena` |
| 2026-03-26 | git | Verify tag/ancestor relationships (M28 branch vs `main`) | `git merge-base`, `git log` |
| 2026-03-26 | write | M30 deliverables + ledger + M28 doc alignment | `docs/milestones/M30/`, `docs/architecture/serena_*.md`, `docs/serena.md`, `M28_run1.md`, `M28_summary.md` |
| 2026-03-26 | write | Seed Phase VII M31 stubs | `docs/milestones/M31/` |
