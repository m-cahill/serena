# M31 — Architecture lock

**Phase VII** (per `docs/serena.md`).

## Objective

Create a **documentation-only** milestone that locks Serena’s **approved post-refactor architecture** after Phases I–VI, without changing runtime behavior, CI policy, workflows, dependencies, API behavior, UI behavior, or extension behavior.

## Deliverables

| Artifact | Role |
|----------|------|
| `docs/architecture/serena_architecture_lock.md` | Canonical architecture lock: authority order, locked summary, boundaries table, change-control, proof refs |
| `docs/architecture/serena_allowed_legacy_surfaces.md` | Tolerated legacy glue (vs locked architecture) |
| `docs/serena.md` | Ledger: M31 row, Phase VII progress, source-of-truth hierarchy update, completion timestamp |
| `docs/milestones/M31/M31_plan.md` | This file |
| `docs/milestones/M31/M31_toolcalls.md` | Tool log |
| `docs/milestones/M31/M31_run1.md` | PR provenance, verification, CI hygiene notes |
| `docs/milestones/M31/M31_summary.md` | Milestone summary |
| `docs/milestones/M31/M31_audit.md` | Milestone audit |
| `docs/milestones/M32/M32_plan.md` | Stub for next milestone |
| `docs/milestones/M32/M32_toolcalls.md` | Stub for next milestone |

## Out of scope

- Application code, workflow YAML, lockfiles, dependencies
- CI threshold or policy changes
- Optional `docs/architecture/serena_boundary_map.md` unless clarity demands it

## Definition of done

- Lock + allowed-legacy docs exist and are evidence-backed
- Ledger updated with M31 completion **date/time (UTC)**
- M32 stubs created
- Diff review: no non-doc/runtime/CI config changes

## Verification

- Consistency with `serena_evidence_bundle.md`, `serena_evidence_matrix.md`, `serena_case_study_summary.md`, and ledger milestone rows (M20, M25, M29, M30)
- PR workflow for merge to `main`; treat PR checks as **hygiene only** for this doc-only milestone
