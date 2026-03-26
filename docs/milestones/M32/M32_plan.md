# M32 — Evidence / audit closure

**Phase VII** (per `docs/serena.md`). Follows **M31** (architecture lock).

## Objective

Produce a **documentation-only** Phase VII closure package that **synthesizes** existing ledger, architecture lock, allowed-legacy companion, evidence bundle, and evidence matrix into an **auditable** record of what is proven, what is locked, what legacy is tolerated and visible, and what remains for **M33**. **No** application code, workflow YAML, dependency manifests, or CI threshold/policy changes.

This milestone **does not** substitute documentation for runtime proof; it **points to** where binding proof lives (M29 Quality, prior milestone CI, contract tests) and preserves the M30/M31 posture for doc-only work (PR CI = hygiene/provenance where applicable).

## Deliverables

| Artifact | Role |
|----------|------|
| `docs/milestones/M32/M32_plan.md` | This file |
| `docs/milestones/M32/M32_toolcalls.md` | Tool log |
| `docs/milestones/M32/M32_run1.md` | Authority stack, binding evidence map, tolerated legacy pointer, M33 gap, verdict; PR provenance when available |
| `docs/milestones/M32/M32_summary.md` | Short closeout summary |
| `docs/milestones/M32/M32_audit.md` | Milestone audit |
| `docs/serena.md` | M32 ledger row; Phase VII progress; **next: M33** |
| `docs/architecture/serena_evidence_bundle.md` | Minimal alignment: post–M32 “what remains” / index (if needed for consistency) |
| `docs/architecture/serena_evidence_matrix.md` | Phase VII **M32** row (synthesis closure; doc-only) |
| `docs/milestones/M33/M33_plan.md` | Minimal stub — title only: release-ready 5/5 close |
| `docs/milestones/M33/M33_toolcalls.md` | Minimal stub — header only |

## Out of scope

- Application code, tests, workflows, lockfiles, dependencies
- Reopening architecture decisions documented in `serena_architecture_lock.md`
- New technical claims not grounded in ledger, lock, bundle, matrix, or milestone evidence
- Inventing new legacy seams beyond `serena_allowed_legacy_surfaces.md` and prior audits
- Annotated release tags (unless explicitly approved at closeout)

## Definition of done

- M32 docs exist and cross-check **consistency** with authoritative sources (no unresolved contradictions found during synthesis)
- Ledger updated with M32 completion **date/time (UTC)** and **next: M33**
- M33 folder seeded minimally
- Diff review: **only** documentation under `docs/` (and no CI/code/manifest edits)

## Verification

- Internal consistency: ledger ↔ lock ↔ allowed legacy ↔ bundle ↔ matrix ↔ `M31_run1.md` / `M30_run1.md` where cited
- Truthful posture: doc-only milestones do not claim new runtime gates; binding Quality/perf references remain **23618918747** and artifacts per bundle/matrix
- PR workflow: branch → PR to `main` on `m-cahill/serena`; treat PR checks as **provenance/hygiene** for this doc-only milestone (same as M30/M31)
