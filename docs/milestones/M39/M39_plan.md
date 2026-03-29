# M39 — Remaining legacy surface narrowing

**Status:** Planned (stub — no implementation yet)  
**Branch:** TBD  

## Intent

Continue **Phase IX** internal score-lift by **narrowing remaining tolerated legacy surfaces** called out in **`docs/architecture/serena_allowed_legacy_surfaces.md`** and **`docs/serenam37audit.md`**, in **small, behavior-preserving** steps.

## Scope (planned)

- **In:** Targeted reductions of direct `shared.*` / global hub reads at seams already bounded by architecture lock; optional follow-on after M38 processing split.
- **Out:** Broad globals cleanup, new public APIs, CI weakening, deprecation of extension-facing imports without version policy.

## Invariants

- **No** change to **`ProcessingRunner`** contract without explicit milestone scope.
- **No** CI policy rollback; Quality / Linter / coverage gates unchanged unless a milestone explicitly recalibrates (not M39 default).

## Verification (when executed)

- PR: Linter + Smoke green on topic branch.
- Post-merge `main`: Linter + Quality green.

## Deliverables (when executed)

- Code changes per scoped plan; `M39_run1.md`, `M39_summary.md`, `M39_audit.md` at closeout.
