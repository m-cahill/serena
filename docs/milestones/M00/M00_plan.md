# M00 Plan — Program Kickoff, Baseline Freeze, Phase Map, and E2E Verification

**Milestone:** M00  
**Title:** Program Kickoff, Baseline Freeze, Phase Map, and E2E Verification  
**Branch:** m00-kickoff-baseline-e2e  
**Status:** Active

---

## 1. Primary Objective

Establish Serena as a governed refactor program, update `docs/serena.md` with the proposed phase/milestone roadmap, freeze the audited baseline, and verify as much truthful end-to-end behavior as possible before any architectural changes.

---

## 2. Scope Boundaries

**In scope:**
- docs/serena.md creation/update
- Milestone governance files under docs/milestones/M00/
- Baseline freeze metadata
- Local and CI E2E verification using existing paths
- Inventory of workflows, tests, runtime surfaces, and constraints
- Thin helper scripts for repeatable verification (only if they faithfully wrap existing commands)

**Out of scope:**
- Architectural extraction
- Runtime/service layer changes
- opts snapshot work
- Runner abstraction work
- UI modularization
- Extension API contract changes
- Dependency upgrades for cleanup's sake
- Changing build backend or packaging model
- Changing test behavior or coverage thresholds in M00

---

## 3. M00 Invariants (Must Not Change)

| Invariant | Description |
|-----------|-------------|
| **Startup** | Existing application startup behavior must not change |
| **API/UI** | Existing API routes and UI entry behavior must not change |
| **Extensions** | Existing extension discovery/load behavior must not change |
| **Tests** | Existing test semantics must not change |
| **CI** | Existing workflow truthfulness must not be weakened |
| **Deps** | No new runtime dependencies in hot paths |
| **Structure** | No structural refactor yet |
| **Docs/helpers** | docs-only or verification-helper changes must remain behavior-preserving |

---

## 4. Implementation Steps

1. **Preflight** — Inspect repo layout, workflows, tests, runtime surfaces, constraints → M00_preflight.md ✓
2. **Baseline freeze** — Record HEAD SHA, audited SHA, create baseline tag → baseline-pre-refactor ✓
3. **serena.md** — Create/update with project identity, phase map, invariants, ledger seed row ✓
4. **Local E2E verification** — Run real baseline verification path → M00_e2e_baseline.md
5. **CI inventory** — Document workflows and jobs → M00_ci_inventory.md ✓
6. **Optional helper scripts** — Add only if useful and behavior-preserving
7. **Commit, push, PR** — Open PR, record workflow run IDs, do not close until evidence gathered

---

## 5. Acceptance Criteria

M00 is complete only if:

- [x] docs/serena.md exists and clearly acts as the living source of truth
- [x] docs/serena.md contains a proposed multi-phase milestone roadmap
- [x] Baseline SHA/tag is documented
- [x] Detected surfaces and constraints are documented
- [ ] Local baseline verification is documented with real commands and observed outcomes
- [ ] As much practical E2E verification as possible has been run and recorded
- [ ] Existing CI behavior on the fork has been exercised and documented truthfully
- [x] No runtime behavior has been intentionally changed
- [x] No CI checks have been weakened
- [ ] All M00 artifacts are present and internally consistent
