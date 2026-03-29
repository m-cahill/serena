# M40 — Coverage wave on legacy/high-value modules

**Status:** Stub (seeded at M39 closeout)  
**Branch:** TBD

## Intent

Phase IX internal score-lift: targeted **coverage** increases on legacy or high-value modules per **`docs/serena.md`** and **`docs/serenam37audit.md`**, without turning the milestone into arbitrary threshold chasing.

## Scope (planned)

- **In:** Additional **`test/quality`** (or agreed tier) tests for agreed targets; gate **42%** unchanged unless a milestone explicitly recalibrates.
- **Out:** Performance SLO enforcement (**M41**), security deferral work (**M42** conditional), broad refactors.

## Verification (when executed)

- PR: Linter + Smoke; post-merge **`main`**: Linter + Quality.
