# M30 — QA / evidence publishing (seed)

**Status:** Planned (not started). **Depends on:** M29 complete (binding Quality + `performance_snapshot.txt`).

## Intent

Publish QA artifacts and milestone evidence in a repeatable way: consolidate CI run references, audit links, and optional public-facing summaries without changing runtime behavior.

## Scope (initial)

- Define what gets published (ledger excerpts, milestone summaries, CI badge links).
- Keep source of truth in-repo (`docs/serena.md`, `docs/milestones/`).
- No dependency or workflow weakening; no API contract drift.

## Out of scope (until planned)

- Implementation work — tracked only in **`M30_toolcalls.md`** after kickoff.

## References

- Phase VI map: `docs/serena.md`
- M29 binding evidence: `docs/milestones/M29/M29_run1.md`
