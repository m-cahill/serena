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
| 2026-03-26 | git push | Publish M30 branch | `git push -u origin m30-qa-evidence-publishing` |
| 2026-03-26 | gh | Open PR to `main` | `gh pr create` → **PR #82** https://github.com/m-cahill/serena/pull/82 |
| 2026-03-26 | gh | Capture PR checks (eslint, ruff, smoke) | `gh pr checks 82` — all **pass** (runs e.g. **23620057974**, **23620061075**, smoke **23620057948**, **23620061105**) |
| 2026-03-26T22:23Z | gh | Squash-merge **PR #82** to `main` | `gh pr merge 82 --squash` → merge commit **`b663f735074e63055125c390aee8fc907c49e915`** |
| 2026-03-26T22:23Z | gh | Post-merge workflow provenance on `main` | Linter **23620987714** success; Quality **23620987702** success (optional; not M30 binding) |
| 2026-03-26T22:31Z | git | Annotated tag + push | `v0.0.30-m30` — verify with `git show v0.0.30-m30` (tip of M30 closeout on `main`) |
| 2026-03-26 | git / gh | Merge closeout commits on `main` | **`9f3a6f26`** ledger fill; **`7e12fb94`** tag SHA note; **`32fb66bd`** tag narrative |
