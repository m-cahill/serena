# Serena — Refactor Program Ledger

**Program name:** Serena  
**Source repo:** AUTOMATIC1111/stable-diffusion-webui  
**Fork workspace:** m-cahill/serena (origin)  
**Source of truth:** This document  
**Posture:** Behavior-preserving by default, audit-first, milestone-governed

---

## 1. Project Identity

Serena is a governed refactor program for AUTOMATIC1111/stable-diffusion-webui. The goal is to transform the codebase from its current state (audit score ~2.4–2.6/5) to a 5/5 architecture with clear separation of concerns, testable runtime, and stable extension API.

### Serena Refactor Principles

This refactor program follows strict **behavior-preserving governance**.

Core principles:

1. **Behavior preservation by default**
   Existing runtime behavior must remain stable unless explicitly changed.

2. **Small milestones**
   Each milestone introduces minimal surface change.

3. **Runtime seams before architecture changes**
   Isolation is introduced before structural refactors.

4. **Extension compatibility**
   The extension ecosystem must remain functional unless explicitly versioned.

5. **Evidence-based closeout**
   Each milestone must end with verifiable CI evidence.

**Source-of-truth hierarchy:**
1. `docs/serena.md` — This ledger (phases, milestones, invariants)
2. `docs/sdwebuirefactoraudit.md` — Baseline audit (architecture, modularity, refactor strategy)
3. `docs/sdwebuiaudit.md` — Supplementary audit (DX, phased plan)
4. Milestone docs under `docs/milestones/MNN/`

---

## 2. Current Baseline

| Item | Value |
|------|-------|
| **Audited baseline SHA** | `82a973c04367123ae98bd9abdf80d9eda9b910e2` |
| **Baseline tag** | `baseline-pre-refactor` (annotated, immutable) |
| **Initial audit score** | 2.4 / 5 (sdwebuirefactoraudit) |
| **Upstream** | https://github.com/AUTOMATIC1111/stable-diffusion-webui.git |

**Top architectural problems (from audit):**
- Global state hub: `shared.opts`, `shared.state`, `shared.sd_model` used by dozens of modules
- No test tiers or coverage gate
- God modules: `processing.py` (~1793 LOC), `ui.py` (~984 LOC), `api/api.py` (~750 LOC)
- Dependency and CI hygiene: mixed pinning, lockfile gitignored, actions use tags not SHA

---

## 3. Proposed Phase Map (Provisional)

*Can evolve after M00 evidence.*

### Phase I — Baseline & Guardrails (M00–M04)
| Milestone | Title |
|-----------|-------|
| M00 | Program kickoff, baseline freeze, phase map, E2E verification |
| M01 | CI truthfulness, SHA pinning, smoke path |
| M02 | Local dev guardrails, CONTRIBUTING, repeatable verification |
| M03 | Test architecture (smoke / quality / nightly) |
| M04 | Coverage/security/reproducibility guardrails |

### Phase II — Runtime Seam Preparation (M05–M09)
| Milestone | Title |
|-----------|-------|
| M05 | Override isolation / temporary opts seam |
| M06 | Prompt/seed prep extraction |
| M07 | Opts snapshot introduction |
| M08 | process_images_inner snapshot threading |
| M09 | Execution context/state seam |

### Phase III — Runner & Service Boundary (M10–M14)
| Milestone | Title |
|-----------|-------|
| M10 | ProcessingRunner skeleton |
| M11 | txt2img via runner |
| M12 | img2img via runner |
| M13 | API adoption of runner |
| M14 | UI adoption of runner |

### Phase IV — Runtime Extraction (M15–M19)
| Milestone | Title |
|-----------|-------|
| M15 | Runtime module extraction |
| M16 | Sampler runner extraction |
| M17 | Decode/save separation |
| M18 | Model provider interface |
| M19 | Runtime tests with mockable boundaries |

### Phase V — UI & Extension Stabilization (M20–M24)
| Milestone | Title |
|-----------|-------|
| M20 | UI tab registry |
| M21 | txt2img/img2img tab modularization |
| M22 | Settings/extensions modularization |
| M23 | Extension API version/contract |
| M24 | Deprecation/compatibility scaffolding |

### Phase VI — Hardening & Reproducibility (M25–M29)
| Milestone | Title |
|-----------|-------|
| M25 | Locked manifests / npm ci / CI env stabilization |
| M26 | Coverage and complexity gates |
| M27 | Security/supply-chain evidence |
| M28 | Health/perf verification |
| M29 | QA/evidence publishing |

### Phase VII — Release Lock / 5.0 Closure (M30–M32)
| Milestone | Title |
|-----------|-------|
| M30 | Architecture lock |
| M31 | Evidence/audit closure |
| M32 | Release-ready 5/5 close |

---

## 4. Milestone Ledger

| Milestone | Title | Status | Branch | PR | Commit | CI Run(s) | Audit Score / Notes | Completed At |
|-----------|-------|--------|--------|-----|--------|-----------|---------------------|--------------|
| M00 | Program kickoff, baseline freeze, phase map, E2E verification | Completed | m00-kickoff-baseline-e2e | — | cdfe1285 | Linter 22794525690 ✓; Tests 22794525698 ✗ (pre-existing CLIP/pkg_resources) | Baseline 2.4/5 | 2025-03-07 |
| M01 | CI truthfulness, SHA pinning, smoke path | Completed | m01-ci-truthfulness | — | 2f664049 | Linter 22814396752 ✓; Tests 22814850488 (server ✓, 17 pass, img2img/txt2img 500) | 4.7 / 5 | 2026-03-08 |
| M02 | API CI truthfulness, local dev guardrails | Completed | m02-api-ci-truthfulness | — | 7484170d | Linter 22831756517 ✓; Tests 22831756504 ✓ (33/33 pass) | 4.9 / 5 | 2026-03-08 |
| M03 | Test architecture (smoke / quality / nightly) | Completed | m03-test-architecture | #2 | eee04b57 | Linter ✓; Smoke 22834384359 ✓ (33/33) | — | 2026-03-09 |

---

## 5. Standing Invariants

Repo-wide non-negotiables for this program:

- **No silent behavior drift** — All changes must preserve or explicitly document behavior
- **No CI weakening** — Do not relax checks, thresholds, or truthfulness
- **Preserve extension behavior** — Unless intentionally versioned in a milestone
- **Preserve API/UI semantics** — Unless milestone explicitly approves change
- **Evidence-first closeout** — Every milestone closes with documented evidence

---

## 6. Invariant Registry

These invariants must remain stable throughout the Serena refactor program unless explicitly revised by a milestone.

This registry provides **cross-milestone contract stability**.

| Surface              | Description                                             | Verification                |
| -------------------- | ------------------------------------------------------- | --------------------------- |
| CLI                  | Command flags and output behavior remain stable         | Snapshot tests              |
| API                  | JSON response schemas remain compatible                 | Contract tests              |
| File formats         | Serialized artifacts and saved images remain compatible | Schema validation           |
| Public modules       | Import surfaces remain available unless versioned       | API compatibility tests     |
| Extension API        | Extension loading behavior and hooks remain stable      | Extension integration tests |
| Generation semantics | txt2img / img2img parameter behavior preserved          | E2E smoke tests             |

Notes:

* Any invariant modification must be documented in the milestone plan.
* Regression verification must be automated where possible.
