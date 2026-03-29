# Serena ? Refactor Program Ledger

**Program name:** Serena  
**Source repo:** AUTOMATIC1111/stable-diffusion-webui  
**Fork workspace:** m-cahill/serena (origin)  
**Source of truth:** This document  
**Posture:** Behavior-preserving by default, audit-first, milestone-governed

---

## 1. Project Identity

Serena is a governed refactor program for AUTOMATIC1111/stable-diffusion-webui. The goal is to transform the codebase from its current state (audit score ~2.4?2.6/5) to a 5/5 architecture with clear separation of concerns, testable runtime, and stable extension API.

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

**Source-of-truth hierarchy (post–M37):**
1. `docs/serena.md` — Program ledger (phases, milestones, invariants)
2. `docs/architecture/serena_architecture_lock.md` — Approved steady-state architecture and locked boundaries (structural questions)
3. `docs/architecture/serena_evidence_bundle.md` — Phase I–VI proof narrative (see also `serena_case_study_summary.md`, `serena_evidence_matrix.md`)
4. Milestone docs under `docs/milestones/MNN/`, run records, milestone audits/summaries
5. `docs/serenav1audit.md` — Post-v1 audit (authoritative input for Phase VIII scope and targets)
6. `docs/serenam37audit.md` — Post-Phase VIII audit (authoritative input for Phase IX scope and targets)

**Historical baseline (pre-refactor audits):** `docs/sdwebuirefactoraudit.md`, `docs/sdwebuiaudit.md` — baseline scores and strategy; subordinate to the ledger and architecture lock for *current* approved shape.

**Allowed legacy glue (companion):** `docs/architecture/serena_allowed_legacy_surfaces.md` — tolerated seams vs locked architecture; not a second source of truth above the lock.

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

### Phase I ? Baseline & Guardrails (M00?M04)
| Milestone | Title |
|-----------|-------|
| M00 | Program kickoff, baseline freeze, phase map, E2E verification |
| M01 | CI truthfulness, SHA pinning, smoke path |
| M02 | Local dev guardrails, CONTRIBUTING, repeatable verification |
| M03 | Test architecture (smoke / quality / nightly) |
| M04 | Coverage/security/reproducibility guardrails |

### Phase II ? Runtime Seam Preparation (M05?M09)
| Milestone | Title |
|-----------|-------|
| M05 | Override isolation / temporary opts seam |
| M06 | Prompt/seed prep extraction |
| M07 | Opts snapshot introduction |
| M08 | process_images_inner snapshot threading |
| M09 | Execution context/state seam |

### Phase III ? Runner & Service Boundary (M10?M15)
| Milestone | Title |
|-----------|-------|
| M10 | ProcessingRunner skeleton |
| M11 | Runner lifecycle surface (prepare / execute / finalize) |
| M12 | Runtime instrumentation hooks |
| M13 | txt2img path through runner |
| M14 | API integration |
| M15 | background/queue runner preparation |

### Phase IV ? Runtime Extraction (M16?M20)
| Milestone | Title |
|-----------|-------|
| M16 | Runtime module extraction |
| M17 | Sampler runner extraction |
| M18 | Decode/save separation |
| M19 | Model provider interface |
| M20 | Runtime tests with mockable boundaries |

### Phase V ? UI & Extension Stabilization (M21?M25)
| Milestone | Title |
|-----------|-------|
| M21 | UI tab registry |
| M22 | txt2img/img2img tab modularization |
| M23 | Settings/extensions modularization |
| M24 | Extension API version/contract |
| M25 | Deprecation/compatibility scaffolding |

**Progress (Phase V):** **Phase V complete ? M21?M25 finished.**

### Phase VI ? Hardening & Reproducibility (M26?M30)
| Milestone | Title |
|-----------|-------|
| M26 | Locked manifests / npm ci / CI env stabilization |
| M27 | Coverage and complexity gates |
| M28 | Security/supply-chain evidence |
| M29 | Health/perf verification |
| M30 | QA/evidence publishing |

**Progress (Phase VI):** **M26–M30 complete.** **M29** closeout: binding **Quality** **`23618918747`** on **`main`** (**199** pass, **~48%** cov, **`performance_snapshot.txt`** artifact); recovery **PR #79** (M29.1), **PR #80** / **#81** (M29.2); tag **`v0.0.29-m29`** @ **`1b2e2f692d35365de584b7468e8bd9122617358a`**. **M30** closeout: **PR #82** → merge **`b663f735`**; evidence bundle **`docs/architecture/serena_evidence_bundle.md`**, **`serena_case_study_summary.md`**, **`serena_evidence_matrix.md`**; **`M30_run1.md`** (incl. **M28** / **`main`** / **PR #64** note); tag **`v0.0.30-m30`**. **M30** is **documentation / evidence only** — no runtime gate.

**Progress (Phase VII):** **Complete.** **M31** (architecture lock) — **`docs/architecture/serena_architecture_lock.md`**, **`serena_allowed_legacy_surfaces.md`**; documentation only. **M32** (evidence/audit closure) — **`docs/milestones/M32/`** (`M32_run1.md`); documentation only. **M33** (release-ready 5/5 close) — **`docs/milestones/M33/`** (`M33_run1.md`); program/governance closeout for **Phase VII**; documentation only. **M33** is the **final milestone** of **Phase VII**; **Phase VIII** (M34–M37) is **complete** (post–M37 closeout — see **`docs/serenav1audit.md`**, **`docs/milestones/M37/`**).

### Phase VII ? Release Lock / 5.0 Closure (M31?M33)
| Milestone | Title |
|-----------|-------|
| M31 | Architecture lock |
| M32 | Evidence/audit closure |
| M33 | Release-ready 5/5 close |

### Phase VIII ? Final 5/5 Closure (M34–M37)
| Milestone | Title | Status |
|-----------|-------|--------|
| M34 | Runtime context model-identity seam | **Complete** (2026-03-27 ~23:10 UTC) |
| M35 | Remove tolerated `shared.sd_model` orchestration coupling | **Complete** (2026-03-28 ~01:00 UTC) |
| M36 | Coverage lift and gate recalibration | **Complete** (2026-03-28 ~04:15 UTC) |
| M37 | Security deferral closure and final 5/5 re-audit | **Complete** (2026-03-28 UTC) |

**Progress (Phase VIII):** **Complete** (M34–M37). **M34** — **`ModelIdentity`** / **`RuntimeContext.model_identity`**; merge **PR #90**; binding **Quality** **`23671154433`**. **M35** — **`_orchestration_model(p)`**; **PR #91**; **Quality** **`23673838908`**. **M36** — coverage lift tests; **PR #92**; **Quality** **`23677054515`** (**213** pass, **48%** cov); gate **42%** unchanged. **M37** — deferral re-audit; **no** PyPI-installable fixes for **diskcache** / **pygments** at closeout; governed **`pip-audit`** ignores **unchanged**; final docs — **`docs/milestones/M37/`**. Authoritative scope: **`docs/serenav1audit.md`**.

### Phase IX — Internal Score-Lift (M38–M41)
| Milestone | Title | Status |
|-----------|-------|--------|
| M38 | `processing.py` class and helper decomposition | **Complete** (2026-03-29 UTC) |
| M39 | Remaining legacy surface narrowing | **PR [#95](https://github.com/m-cahill/serena/pull/95)** (Linter + Smoke green; merge + post-merge Quality pending) |
| M40 | Coverage wave on legacy/high-value modules | **Planned** |
| M41 | Performance SLOs and regression guardrails | **Planned** |

**Progress (Phase IX):** **M38** — **`processing_types` / `processing_helpers` / `processing_infotext`** split; **`processing.py`** orchestration + re-exports; **PR [#94](https://github.com/m-cahill/serena/pull/94)** merge **`17c21be669942518ab4683ba504c87c1ad58900e`** (**2026-03-29T03:45:35Z**); approval tip **`3654f8a3`** (`pull_request` Linter **`23700334490`**, Smoke **`23700334489`**); **main:** Linter **`23700723142`**, Quality **`23700723134`** (**217** pass, **48%** cov). **`docs/milestones/M38/`** closeout. **M39** — **`_eff_opts(p)`** opts snapshot preference on supported paths; **PR [#95](https://github.com/m-cahill/serena/pull/95)** head **`eee9af2a`** — `pull_request` Linter **`23719147857`**, Smoke **`23719147871`**; post-merge **`main`** Quality — **`M39_run1.md`** §B; **`docs/milestones/M39/`** + **`M40_plan.md`** stub.

**Program intent:** Tightly scoped post-Phase VIII internal score-lift. Goal is to improve the M37 audit score (4.6/5) by addressing remaining internal structural drag — `processing.py` concentration, residual allowed-legacy surfaces, coverage plateau at ~48%, and lack of enforced performance SLO thresholds — **without** weakening CI, changing behavior silently, destabilizing extension compatibility, or reopening broad speculative architecture work. Authoritative input: **`docs/serenam37audit.md`**.

**Conditional future milestone:**
| Milestone | Title | Status |
|-----------|-------|--------|
| M42 | Conditional upstream deferral removal | **Conditional** — open only if PyPI ships installable fixes for **CVE-2025-69872** (diskcache) and/or **CVE-2026-4539** (pygments) |

---

## 4. Milestone Ledger

| Milestone | Title | Status | Branch | PR | Commit | CI Run(s) | Audit Score / Notes | Completed At |
|-----------|-------|--------|--------|-----|--------|-----------|---------------------|--------------|
| M00 | Program kickoff, baseline freeze, phase map, E2E verification | Completed | m00-kickoff-baseline-e2e | ? | cdfe1285 | Linter 22794525690 ?; Tests 22794525698 ? (pre-existing CLIP/pkg_resources) | Baseline 2.4/5 | 2025-03-07 |
| M01 | CI truthfulness, SHA pinning, smoke path | Completed | m01-ci-truthfulness | ? | 2f664049 | Linter 22814396752 ?; Tests 22814850488 (server ?, 17 pass, img2img/txt2img 500) | 4.7 / 5 | 2026-03-08 |
| M02 | API CI truthfulness, local dev guardrails | Completed | m02-api-ci-truthfulness | ? | 7484170d | Linter 22831756517 ?; Tests 22831756504 ? (33/33 pass) | 4.9 / 5 | 2026-03-08 |
| M03 | Test architecture (smoke / quality / nightly) | Completed | m03-test-architecture | #2 | 975dda4b | Linter ?; Smoke 22834384359 ?; Quality 22834861040 ? | 5.0 / 5 | 2026-03-09 |
| M04 | Coverage/security/reproducibility guardrails | Completed | m04-coverage-guardrails | #4 | 47439cac | Quality 22871471473 ? (coverage 40%, pip-audit, verify_pinned_deps) | 5.0 / 5 | 2026-03-09 |
| M05 | Override isolation / temporary opts seam | Completed | m05-override-isolation | #18 (+ #19 fix) | ae161cbb | Quality 22888808682 ? | 5.0 / 5 | 2026-03-10 |
| M06 | Prompt/seed prep extraction | Completed | m06-prompt-seed-prep | #20 | 6744152a | Quality 22890285319 ? | 5.0 / 5 | 2026-03-10 |
| M07 | Opts snapshot introduction | Completed | m07-opts-snapshot | #22 | 8ea50d35 | Quality 22983583947 ? | 5.0 / 5 | 2026-03-12 |
| M08 | Opts snapshot threading | Completed | m08-snapshot-threading | #24 | 710a0abd | Quality 22984445599 ? | 5.0 / 5 | 2026-03-12 |
| M09 | Execution context introduction | Completed | m09-execution-context | #26 | 2c6a2510 | Quality 22986731960 ? | 5.0 / 5 | 2026-03-12 |
| M10 | ProcessingRunner skeleton | Completed | m10-processing-runner | #27 (+ #28 fix) | 0d11b587 | Quality 22988627838 ? | 5.0 / 5 | 2026-03-12 |
| M11 | Runner lifecycle surface | Completed | m11-runner-lifecycle | #30 | 08ac1c0e | Quality 22989978348 ? | 5.0 / 5 | 2026-03-12 |
| M12 | Runtime instrumentation hooks | Completed | m12-runner-instrumentation | ? | 46cf6d1c | Quality 23037656379 ? | 5.0 / 5 | 2026-03-13 |
| M13 | txt2img path through runner | Completed | m13-txt2img-runner | #31 | 4dd04999 | Smoke 23038170275 ?; Linter 23072709504 ?; Quality 23072709479 ? | 5.0 / 5 | 2026-03-13 |
| M14 | API integration | Completed | m14-api-runner-contract | #32 | 5b7de065 | Smoke 23182483297 ?; Linter 23182849899 ?; Quality 23182849888 ? | 5.0 / 5 | 2026-03-17 |
| M15 | Queue runner preparation | Completed | m15-queue-runner-prep | #33 | a4b9a622 | Smoke 23227154919 ?; Linter 23227154926 ?; Quality 23232040072 ? | 5.0 / 5 | 2026-03-18 |
| M16 | Runtime module extraction | Completed | m16-runtime-extraction | #34 | 912f33da | Linter 23276080886 ?; Smoke 23276080894 ?; Quality 23283000106 ? | 5.0 / 5 | 2026-03-19 06:40 UTC |
| M17 | Sampler runner extraction | Completed | m17-sampler-runner-extraction | #35 | 16bd28ce | Linter 23284575241 ?; Smoke 23284575264 ? (PR); Linter 23318593862 ?; Quality 23318593847 ? | 5.0 / 5 | 2026-03-19 21:54 UTC |
| M18 | Decode/save separation | Completed | m18-decode-save-separation | #36 | 84ea94e7 | Linter 23320584761 ?; Smoke 23320584759 ? (PR); Linter 23321103971 ?; Quality 23321103961 ? (79 pass, 40% cov) | 5.0 / 5 | 2026-03-19 23:08 UTC |
| M19 | Model provider interface | Completed | m19-model-provider | #37, #38 | 8fb464e4 | Linter 23324037879 ?; Smoke 23324037884 ? (PR #37); Quality 23326003636 ? (83 pass, 40% cov) | 5.0 / 5 | 2026-03-20 02:09 UTC |
| M20 | Runtime tests with mockable boundaries | Completed | m20-runtime-mock-tests | #39 | 9c7e693a | PR Linter 23331851493 ?; Smoke 23331851499 ?; Quality 23333740069 ? (87 pass, 40% cov) | 5.0 / 5 | 2026-03-20 07:51 UTC |
| M21 | UI tab registry | Completed | m21-ui-tab-registry | #40 | 081de7e7 | Linter 23360537402; Smoke 23360545341; Quality 23361011739 (92 pass, 40% cov) | 5.0 / 5 | 2026-03-20 |
| M22 | txt2img/img2img tab modularization | Completed | m22-tab-modularization | #41 | 99b5f0c4 | Smoke 23365701378; Linter 23365701379; Quality 23365924953 (success, ?40% cov) | 5.0 / 5 | 2026-03-20 |
| M23 | Settings/extensions modularization | Completed | m23-settings-extensions-modularization | #42 | 64c232c3 | Linter 23370424058 (PR); Smoke 23370424057 (PR); Quality 23370952185 (102 pass, ~44% cov) | 5.0 / 5 | 2026-03-21 |
| M24 | Extension API version/contract | Completed | m24-extension-api-contract | #43 | 2c8bc5b7 | Linter 23395414702 (PR); Smoke 23395414700 (PR); Quality 23395515966 (105 pass, 40% cov) | 5.0 / 5 | 2026-03-22 |
| M25 | Deprecation/compatibility scaffolding | Completed | m25-deprecation-compat-scaffolding | #44 | 46891797 | Linter 23417606838 (PR); Smoke 23417606843 (PR); Quality 23421440167 (112 pass, 40% cov) | 5.0 / 5 | 2026-03-23 |
| M26 | Locked manifests & CI environment stabilization | Completed | m26-locked-manifests-ci-env | #45–#53 | 67692434 | Linter 23421937195 (pass); Smoke 23421937182 (pass); Quality 23467772232 (pass, 112 pass, 40% cov) | 5.0 / 5 | 2026-03-23 (UTC) |
| M27 | Coverage and complexity gates | Completed | m27-coverage-complexity-gates; m27-coverage-measurement-fix | #54–#63 | e3c0d554 | Linter 23512022787 (PR, fail); Smoke 23512022741 (PR, pass); Quality **23513449859** (pass, 198 pass, **47%** cov pytest-only) | 5.0 / 5 | 2026-03-24 ~21:43 UTC |
| M28 | Security / supply-chain hardening | Completed | m28-security-supply-chain | **#64** (M28+M29 squash to `main` **f18b73f2**; topic finalize **f88e1e9c**) | f88e1e9c | No isolated green Quality on **`main`** for M28 alone; first post-**#64** run **23566817312** failed; stack + **`pip-audit`** proof **23618918747**; **2** deferrals — see **`M30_run1.md`** §3, `M28_run1.md` | 5.0 / 5 | 2026-03-26 |
| M29 | Health / performance verification | Completed | `main`; m29.2-quality-recovery; m29.2-flags-argparse-types | #64–#71; **#79**; **#80**; **#81** | `1b2e2f69` | Quality **23618918747** (pass, **199** pass, **~48%** cov); **`performance_snapshot.txt`** | **5.0 / 5** — binding CI + artifact | 2026-03-26 |
| M30 | QA / evidence publishing (documentation / evidence) | Completed | m30-qa-evidence-publishing | **#82** | **b663f735** | **Doc-only:** no binding runtime gate; post-merge **optional** provenance on **`b663f735`**: Linter **23620987714** pass; Quality **23620987702** pass; PR **#82** hygiene checks in `M30_run1.md` §6 | 5.0 / 5 | 2026-03-26 ~22:24 UTC |
| M31 | Architecture lock (documentation) | Completed | m31-architecture-lock | **#83** (+ closeout **#84**) | **09f1d785** | **Doc-only:** lock merge **#83**; PR checks + post-merge Linter **23621856813** / Quality **23621856875** — **provenance only** (`M31_run1.md` §6–§7); closeout **#84** adds **`M31_run1.md`**, **`M31_summary.md`**, **`M31_audit.md`**, ledger fill (**merge `3b2af43f`**) | 5.0 / 5 | 2026-03-26 ~23:55 UTC |
| M32 | Evidence/audit closure (documentation) | Completed | m32-evidence-audit-closure | **[#86](https://github.com/m-cahill/serena/pull/86)** | **`3f6f6a2e`** | **Doc-only:** no binding runtime gate; ledger + lock + bundle + matrix synthesis (`M32_run1.md`); post-merge on **`3f6f6a2e`**: Linter **23624248870** / Quality **23624248875** — **provenance only** (`M32_run1.md` §8) | 5.0 / 5 | 2026-03-27 ~00:06 UTC |
| M33 | Release-ready 5/5 close (documentation) | Completed | m33-release-ready-close | **[#88](https://github.com/m-cahill/serena/pull/88)** | **`ebb44177`** | **Doc-only:** no binding runtime gate; program closeout (`M33_run1.md`); PR **#88** checks: Linter **23626330336** / **23626332648**, Smoke **23626330338** / **23626332665** — **provenance only**; post-merge on **`ebb44177`**: Linter **23626413453** / Quality **23626413493** — **provenance only** (`M33_run1.md` §9); tag **`v0.0.33-m33`** @ **`ebb44177`** | 5.0 / 5 | 2026-03-27 ~01:22 UTC |
| M34 | Runtime context model-identity seam | **Completed** | m34-runtime-context-model-identity | **[#90](https://github.com/m-cahill/serena/pull/90)** | merge **`b94c93d38e521437a18bb1660d35b31c90220be0`**; binding CI tip **`1bc04394`** | PR: Linter **`23669814419`**, Smoke **`23669814433`** (head **`8e209ed2`**); **main:** Linter **`23671154431`**, **Quality** **`23671154433`** (**202** pass, **~48%** cov) | **`ModelIdentity`** on **`RuntimeContext`**; **`M34_run1.md`**, **`M34_summary.md`**, **`M34_audit.md`** | **2026-03-27 ~23:10 UTC** |
| M35 | Remove tolerated `shared.sd_model` orchestration coupling | **Completed** | `m35-remove-shared-sd-model-orchestration` | **[#91](https://github.com/m-cahill/serena/pull/91)** | merge **`45e6f4fbfb8f6ed2dfc336423d1f414f66c77549`**; binding CI tip **`45e6f4fb`** | PR approval: Linter **`23673315409`**, Smoke **`23673315420`** (head **`564ebd27`**); **main:** Linter **`23673838902`**, **Quality** **`23673838908`** (**203** pass, **48%** cov) | **`_orchestration_model`**, allowed-legacy update; **`M35_run1.md`**, **`M35_summary.md`**, **`M35_audit.md`** | **2026-03-28 ~01:00 UTC** |
| M36 | Coverage lift and gate recalibration | **Completed** | `m36-coverage-lift-gate-recalibration` | **[#92](https://github.com/m-cahill/serena/pull/92)** | merge **`ab4c4679397091ef8de2d46db3afadf3113a6979`** | PR tip **`c410771f`**: Linter **`23676919831`**, Smoke **`23676919933`**; **main:** Linter **`23677054517`**, **Quality** **`23677054515`** (**213** pass, **48%** cov); gate **42%** unchanged | **`M36_run1.md`**, **`M36_summary.md`**, **`M36_audit.md`** | **2026-03-28 ~04:15 UTC** |
| M37 | Security deferral closure and final 5/5 re-audit | **Completed** | `m37-security-deferral-final-audit` | **[#93](https://github.com/m-cahill/serena/pull/93)** | merge **`18c13a59b73de16f85c7dacd57162ac55713b1aa`** | PR head **`b9166a0d`**: Linter **`23677809650`**, Smoke **`23677809662`**; **main:** Linter **`23677884602`**, **Quality** **`23677884594`** (**213** pass, **48%** cov); **pip-audit** **2 ignored** (unchanged CVEs) | **M37** run1/summary/audit; **Phase VIII** closed; deferrals **retained** (no PyPI fixes) | **2026-03-28 UTC** |
| M38 | `processing.py` class and helper decomposition | **Completed** | `m38-processing-class-helper-decomposition` | **[#94](https://github.com/m-cahill/serena/pull/94)** | merge **`17c21be669942518ab4683ba504c87c1ad58900e`** | Approval tip **`3654f8a3`**: Linter **`23700334490`**, Smoke **`23700334489`**; **main:** Linter **`23700723142`**, Quality **`23700723134`** (**217** pass, **48%** cov) | **`processing_types` / helpers / infotext**; **`processing.py`** re-exports; hooks in **`processing.py`**; **`M38_run1.md`** §B lag note — approval used **`3654f8a3`**; **`M38_summary.md`**, **`M38_audit.md`** | **2026-03-29 UTC** |
| M39 | Remaining legacy surface narrowing | **PR open** | `m39-remaining-legacy-surface-narrowing` | **[#95](https://github.com/m-cahill/serena/pull/95)** | **`eee9af2a`** | PR: Linter **`23719147857`**, Smoke **`23719147871`**; post-merge Quality — **`M39_run1.md`** | **`_eff_opts`**, allowed-legacy §2.2 | — |
| M40 | Coverage wave on legacy/high-value modules | **Planned** | — | — | — | — | — | — |
| M41 | Performance SLOs and regression guardrails | **Planned** | — | — | — | — | — | — |

**M05:** Introduced `temporary_opts()` context manager ? first Phase II runtime seam. Isolates override_settings mutation from global `shared.opts`; preserves behavior (opts.set, setattr restore, k in opts.data). Model/VAE reload and token merging remain in process_images. Enables future opts snapshot injection (M07).

**M06:** Extracted `prepare_prompt_seed_state(p)` into `modules/prompt_seed_prep.py`. Second Phase II runtime seam. Populates p.all_seeds and p.all_subseeds; setup_prompts and fill_fields_from_opts unchanged. Enables M07 opts snapshot and M09 execution context.

**M07:** Introduced `create_opts_snapshot(opts)` in `modules/opts_snapshot.py`. Third Phase II runtime seam. Captures deterministic snapshot of opts.data in process_images_inner after prepare_prompt_seed_state; stored on p.opts_snapshot. Write-only in M07; enables M08 snapshot threading.

**M08:** Threaded p.opts_snapshot into process_images_inner for save-related reads. Fourth Phase II runtime seam. Migrated 12 opts (save_images_before_face_restoration, samples_format, grid_save, etc.) from shared.opts to p.opts_snapshot. save_samples(), sample_hr_pass(), metadata unchanged. Enables M09 execution context.

**M09:** Introduced RuntimeContext in modules/runtime_context.py. Fifth Phase II runtime seam. Attached p.runtime_context in process_images_inner() after opts_snapshot (model, opts_snapshot, device, state, cmd_opts). Write-only in M09; no migration of shared.* reads yet. Completes Phase II ? Runtime Seam Preparation. Enables Phase III ProcessingRunner.

**M10:** Introduced ProcessingRunner in modules/runtime/runner.py. First Phase III execution boundary. process_images delegates through runner; ProcessingRequest wraps StableDiffusionProcessing. Zero blast radius; all callers unchanged. Phase III roadmap updated (M11 lifecycle, M12 instrumentation, M13 txt2img, M14 API, M15 queue). Enables M11 Runner lifecycle surface.

**M11:** Introduced lifecycle surface on ProcessingRunner: prepare ? execute ? finalize. run() delegates through stages; pass-through behavior; identical outputs. test_runner_lifecycle_order verifies lifecycle structure. Stable execution surface enables M12 instrumentation, progress hooks, cancellation, queue runners.

**M12:** Introduced optional instrumentation hooks on ProcessingRunner: on_prepare, on_execute, on_finalize. Hooks no-op by default; lifecycle order prepare ? on_prepare ? execute ? on_execute ? finalize ? on_finalize. test_runner_hooks_called verifies hook invocation. Enables M13+ progress, cancellation, queue runners.

**M13:** Verification milestone. Confirmed txt2img path flows through process_images ? ProcessingRunner (no routing changes; M10 already delegates). Added test_txt2img_path_uses_runner contract test. Runner boundary proven with real consumer. Enables M14 API integration.

**M14:** Verification milestone. Confirmed API path flows through process_images ? ProcessingRunner (no routing changes). Added test_api_txt2img_uses_runner contract test. API + UI now both contract-proven. CODEOWNERS updated for fork (@m-cahill). Enables M15 queue/background runner.

**M15:** Introduced ExecutionQueue (pass-through) and queue seam in ProcessingRunner. Optional queue wraps execute only; use_queue=False by default. Constructor injection; _execute(state) hook for future orchestration. test_runner_queue_mode verifies queue used, lifecycle preserved, default unchanged. Completes Phase III ? Runner & Service Boundary. Enables M16 runtime extraction.

**M16:** Extracted execution-phase batch orchestration into `modules/runtime/processing_runtime.py`. `run_generation_batches(p)` generator handles torch context, init, batch loop, sampler call; yields (n, samples_ddim) per batch. process_images_inner delegates; decode/save/postprocess remain in processing.py. First Phase IV extraction; proves runtime logic can move safely behind runner boundary. Enables M17 sampler runner extraction.

**M17:** Extracted sampler creation and invocation into `modules/runtime/sampler_runtime.py`. `run_sampler_txt2img` and `run_sampler_img2img` delegate from Txt2Img.sample, sample_hr_pass, and Img2Img.sample; script hooks and decode/save remain in processing.py. Img2Img keeps `create_sampler` in `init()` (invocation-only extraction). Second Phase IV extraction; runtime layer now owns batch orchestration (M16) and sampler execution (M17). Enables M18 decode/save separation.

**M18:** Extracted VAE decode stack/normalize, face restoration and color/overlay postprocess, per-row saves (including masks), and grid save from `process_images_inner` into `modules/runtime/decode_runtime.py`. `decode_latent_batch` / `DecodedSamples` moved to decode_runtime to avoid import cycles; HR paths import `decode_runtime.decode_latent_batch` only. Script hooks (`postprocess_batch`, `postprocess_image`, mask overlay, after composite) remain in `processing.py` with unchanged order. Third Phase IV extraction; full txt2img/img2img output pipeline for the inner loop now lives in the runtime module. Enables M19 model provider abstraction.

**M19:** Introduced `ModelProvider` / `SharedModelProvider` in `modules/runtime/model_provider.py` and injected `model_provider` via `ProcessingRunner.prepare()` onto `processing`. Runtime modules (`processing_runtime`, `sampler_runtime`, `decode_runtime`) obtain the model only through `p.model_provider.get_model(p)`; no direct `shared.sd_model` or `p.sd_model` in those modules. First dependency-inversion milestone for the inner loop. PR #38 corrected Quality CI: sampler contract tests patch `modules.sd_samplers.create_sampler` (not `sys.modules`) for deterministic import order. Enables M20 mockable runtime.

**M20:** Added `FakeModel` / `FakeModelProvider` in `test/fixtures/fake_model.py` and `test/quality/test_runtime_mock.py` ? Quality integration tests run `ProcessingRunner` + `process_images_inner` without a real model (test-only stubs: fake sampler / `DecodedSamples`, minimal `setup_conds`, CPU-safe autocast, opts snapshot backfill for sparse CI `opts.data`). No runtime module edits. PR #39 merged; follow-up test fixes on `main` to satisfy dataclass init, TI reload skip, and CI CPU torch. Quality **23333740069** @ **9c7e693a**: 87 pass, 40% coverage. Tag **`v0.0.20-m20`** on `9c7e693a`. **Phase IV complete.**

**M21:** Introduced `modules/ui_tab_registry.py` (`TabSpec`, `core_tab_specs`, merge of `ui_tabs_callback()` rows, Settings/Extensions append) and refactored `create_ui()` top-level `interfaces` assembly only. Preserved `script_callbacks.ui_tabs_callback()` then `ui_extensions.create_ui()` side-effect order, `shared.tab_names` pre-sort semantics, and existing `sorted_interfaces` / `hidden_tabs` logic. Quality **`test/quality/test_ui_tab_registry.py`** (five contract tests). PR **#40** squash-merged; Quality **23361011739** @ **081de7e7**: 92 pass, 40% coverage. Tag **`v0.0.21-m21`** on **`081de7e7`**. **First Phase V UI seam.**

**M22:** Extracted txt2img and img2img top-level `gr.Blocks` bodies to `modules/ui_txt2img_tab.py` and `modules/ui_img2img_tab.py` with `TabBuildResult` (`dummy_component`, `txt2img_preview_params`, `image_cfg_scale` for remaining `create_ui()` wiring). Registry public API unchanged (`build_top_level_interface_tuples` still takes six interfaces). Dummy bridge: `ui_img2img_tab.img2img_dummy_component` set from txt2img before img2img build. Import-light entry points; lazy imports inside builders. CI: `.github/workflows/run_smoke_tests.yaml` ? `push` on non-`main` branches + PR to `main`; base-branch verify gated to `pull_request` (Smoke delivery fix). Quality **`test/quality/test_ui_tab_modularization.py`**. PR **#41** squash-merged; Quality **23365924953** @ **99b5f0c4**: coverage gate satisfied. Tag **`v0.0.22-m22`** on **`99b5f0c43806c3b521cbb6d8ef561fa87ef2c75d`**.

**M23:** Added `modules/ui_settings_tab.py` (`create_settings_tab(settings, loadsave, dummy_component)` delegating to `UiSettings.create_ui`) and `modules/ui_extensions_tab.py` (`create_extensions_tab()` with lazy `ui_extensions` import). `UiSettings` lifecycle (`register_settings`, `add_quicksettings`, `add_functionality`, etc.) unchanged in `create_ui()`. Registry API unchanged (nine parameters, `ui_tabs_rows` before settings/extensions). Loadsave guard `ifid not in ["extensions", "settings"]` preserved. Quality **`test/quality/test_ui_settings_extensions_modularization.py`**. PR **#42** squash-merged; Quality **23370952185** @ **64c232c3**: 102 pass, combined coverage ~44%. Tag **`v0.0.23-m23`** on **`64c232c38e0483782126cf8c88f6e287a4de28ef`**. **Top-level tab bodies modularized; `ui.py` orchestration-only for all main tabs.**

**M24:** Introduced `modules/extension_api.py` (`EXTENSION_API_VERSION`, `SUPPORTED_CALLBACKS` category strings), **`docs/architecture/extension_api_contract_v1.md`**, policy block above `callback_map` in `script_callbacks.py`, and **`test/quality/test_extension_api_contract.py`** (exact set equality vs `callback_map` via `removeprefix("callbacks_")`). No invocation or loading changes. PR **#43** squash-merged; Quality **23395515966** @ **2c8bc5b7**: 105 pass, coverage gate satisfied (40% combined report). Tag **`v0.0.24-m24`** on **`2c8bc5b7b5f504597a41a00604f3e7119c22aba6`**. **Extension callback surface versioned and contract-tested.**

**M25:** Added **`modules/deprecation.py`** (`warn_deprecated`, `@deprecated`, `format_extension_api_deprecation`), **`script_callbacks.deprecate_callback`**, separate M25 comment block below **`callback_map`**, **`docs/architecture/extension_api_deprecation_policy.md`**, and **`test/quality/test_deprecation_scaffolding.py`**. No change to **`callback_map`** contents, invocation order, **`ordered_callbacks`**, **`SUPPORTED_CALLBACKS`**, or runtime modules. PR **#44** squash-merged; Quality **23421440167** @ **46891797**: 112 pass, 40% combined coverage (gate). Tag **`v0.0.25-m25`** on **`468917974f9379ec1c514f995ab703c821078e45`**. **Deprecation channel and compatibility policy in place.**

**M26:** Introduced **`requirements-ci.txt`** / **`requirements-ci.in`** (uv-compiled lock) as the **single Quality Python install manifest**; **OpenAI CLIP** installed via **pinned GitHub archive** + workflow **`curl` / `unzip` / `pip install --no-build-isolation`**. Committed **`package-lock.json`**, **`.gitignore`** fix, Linter **`npm ci`** + **`npm ls`** artifact. Extended **`verify_pinned_deps.sh`** (lockfile + **`dependency_snapshot.txt`**). Artifacts: **`pip_freeze.txt`**, **`pip_audit_report.txt`**, **`ci_environment.txt`**, coverage uploads. **`docs/architecture/ci_environment_contract.md`**, **`docs/PR_guardrail_checklist.md`**. **`pip-audit`:** informational **M26–M27** (warning + artifact); **strict enforcement deferred to M28** (governance). Fix chain **#46–#52** (CLIP/PEP517, verify order vs `pip-audit`). PRs **#45–#53**; binding Quality **23467772232** @ **`676924349c3a296e8ef07ef09a588b472498e7fd`**: 112 pass, **40%** coverage. Tag **`v0.0.26-m26`** peels **`25ebe51c3711cc379d1f50962dd78e9f20272bf7`** (`25ebe51c`, closeout merge); Quality binding merge **`676924349c3a296e8ef07ef09a588b472498e7fd`** (`67692434`). **No runtime, extension API, or coverage-threshold change.**

**M27:** Raised Quality coverage floor to **42%**; added **Radon** on **`modules/`** (warn-first **D/E/F**, artifact). **Measurement governance:** **PR #63** — pytest-only coverage (no **`coverage run launch.py`**, no **`coverage combine`**), documented in **`ci_environment_contract.md`** (**Coverage policy (M27)**). PRs **#54–#63** (tests + diagnosis + fix). Binding Quality **23513449859** @ **`e3c0d554fda4bcf24074e85bf43f3fc52bca8c61`**: **198** pass, **47%** TOTAL (pytest-only). **`docs/milestones/M27/M27_summary.md`**, **`M27_audit.md`**. Closeout documentation and annotated tag **`v0.0.27-m27`** (same commit as this closeout). **No runtime or API change;** threshold **42%** unchanged; **pip-audit** / Radon non-blocking per contract.

**M28:** **Blocking `pip-audit`** on Quality (**M28a**); **M28b** small-batch dependency upgrades (HTTP, API, tooling, Pillow 12 / Gradio 6 / NumPy 2, ML stack: **protobuf**, **pytorch-lightning**, **transformers**, **safetensors**, **gradio** security line). **Governed deferrals** for **CVE-2025-69872** (**diskcache**) and **CVE-2026-4539** (**pygments**) — **no PyPI fix** at closeout; workflow **`--ignore-vuln`** only for those IDs; **`ci_environment_contract.md`** **pip-audit deferrals (M28)**. **`docs/milestones/M28/M28_summary.md`**, **`M28_audit.md`**, **`M28_run1.md`**. Commit **`896677d5a516da0b9fa7a50ec0a7a7268e55f0f0`** — deferral workflow + contract; **finalization** (summary, audit, ledger) in **`m28: finalize M28 (deferrals, docs, ledger)`**; annotated tag **`v0.0.28-m28`**. **Delivery to `main`:** squashed with M29 in **PR #64** (**`f18b73f2`**); topic-branch finalize **`f88e1e9c`** is not a first-parent commit on **`main`** — **Quality** clarification in **`M30_run1.md`** §3. Coverage floor **≥42%** unchanged; **no** audit disable.

**M29:** **`ProcessingRunner`** sets **`p.runtime_metrics`** with **`execute_time`** and **`total_time`** (`perf_counter`). **API** **`text2imgapi` / `img2imgapi`**: wall time logged at **DEBUG** only (no JSON change). **`scripts/ci/write_performance_snapshot.py`** + Quality artifact step; **`docs/architecture/performance_baseline.md`**; **`test/quality/test_performance_baseline.py`**. Merged via **#64**; CI follow-ups **#65–#71**; **M29.1** **PR #79** (Gradio / Pydantic dual-stack); **M29.2** **PR #80** / **#81** (`get_cmd_flags`, runner test, **`FlagsModel`** argparse types). Binding **Quality `23618918747`**: **199** pass, **`performance_snapshot.txt`** (**`sample_runner_execute_time_s`** / **`sample_runner_total_time_s`**). Annotated tag **`v0.0.29-m29`** @ **`1b2e2f692d35365de584b7468e8bd9122617358a`**. See **`M29_run1.md`**, **`M29_audit.md`**.

**M30:** **QA / evidence publishing** — **PR #82** squash-merge **`b663f735074e63055125c390aee8fc907c49e915`**; **`docs/architecture/serena_evidence_bundle.md`**, **`serena_case_study_summary.md`**, **`serena_evidence_matrix.md`**; **`docs/milestones/M30/M30_run1.md`**, **`M30_summary.md`**, **`M30_audit.md`**. **Documentation / evidence milestone only** — no workflow or module edits; **no** binding M30 runtime gate. Cross-check **M26–M29**; **M28** / **`main`** / **PR #64** **Quality** history documented (no fabricated run ID). Annotated tag **`v0.0.30-m30`** (final M30 closeout on `main` after merge **`b663f735`**).

**M31:** **Architecture lock** — **PR [#83](https://github.com/m-cahill/serena/pull/83)** squash-merge **`09f1d785677df7400ed21d45ebb7bf3c96c7c979`** (**2026-03-26T22:49:34Z**); **`docs/architecture/serena_architecture_lock.md`** (authority order, locked boundaries, change-control, proof references); **`docs/architecture/serena_allowed_legacy_surfaces.md`** (tolerated `shared.sd_model` / `processing.py` glue vs M19 runtime modules); **`docs/milestones/M31/M31_plan.md`**, **`M31_run1.md`**, **`M31_summary.md`**, **`M31_audit.md`**; M32 stubs. **Documentation only** — no application code, workflow YAML, lockfiles, or dependency changes; PR checks and post-merge CI are hygiene/provenance only (`M31_run1.md`). Completes formal steady-state baseline for **M32** evidence/audit closure.

**M32:** **Evidence/audit closure** — **PR [#86](https://github.com/m-cahill/serena/pull/86)** squash-merge to **`main`** **`3f6f6a2eadd5b2aa0e79a635af0c98c7e7ee6fd9`** (**2026-03-27T00:06:13Z**); **`docs/milestones/M32/M32_plan.md`**, **`M32_run1.md`**, **`M32_summary.md`**, **`M32_audit.md`**; alignment updates to **`serena_evidence_bundle.md`**, **`serena_evidence_matrix.md`**; **`docs/milestones/M33/*`** stubs (expanded in M33). **Documentation only** — no application code, workflow YAML, lockfiles, or dependency changes; **no** new binding runtime gate (same posture as M30/M31). Post-merge CI on **`3f6f6a2e`**: **`M32_run1.md`** §8.

**M33:** **Release-ready 5/5 close** — **PR [#88](https://github.com/m-cahill/serena/pull/88)** squash-merge to **`main`** **`ebb44177ba02839fc25d0baa548eeabdea888560`** (**2026-03-27T01:21:55Z**); branch was **`m33-release-ready-close`**; **`docs/milestones/M33/M33_plan.md`**, **`M33_run1.md`**, **`M33_summary.md`**, **`M33_audit.md`**, **`M33_toolcalls.md`**; ledger **Phase VII** complete; **M33** = **final** milestone of **Phase VII**. **Documentation only** — no application code, workflow YAML, lockfiles, or dependency changes; **no** new binding runtime gate. **Release-ready** = **program/governance** closeout — **not** blanket production certification of the upstream web UI. **Deferrals:** M28 **`pip-audit`** only — **CVE-2025-69872** (**diskcache**), **CVE-2026-4539** (**pygments**). **Annotated tag `v0.0.33-m33`** @ **`ebb44177`**. PR/post-merge CI: **`M33_run1.md`** §9 (**provenance only**). At **M33**, **Phase VIII** (M34–M37) was **planned**; **Phase VIII** was **later completed** in M34–M37 — see **`docs/serenav1audit.md`**, **`docs/milestones/M37/`**.

**M34:** **Runtime context model-identity seam** — **PR [#90](https://github.com/m-cahill/serena/pull/90)** merge commit **`b94c93d38e521437a18bb1660d35b31c90220be0`** (**2026-03-27T22:47:02Z** UTC); branch **`m34-runtime-context-model-identity`**. **`ModelIdentity`** + **`model_identity_from_model()`** in **`modules/runtime_context.py`**; **`p.runtime_context.model_identity`** in **`process_images_inner`**; **`p.sd_model_name`** / **`p.sd_model_hash`** from **`model_identity`**. **Additive-first**; **no** full removal of tolerated **`processing.py` ↔ `shared.sd_model`** orchestration coupling — **deferred to M35**. **Binding post-merge Quality** **`23671154433`** on **`main`** **`1bc04394b3844b4b9c7fda6448567e735d8ec0cc`** (**202** pass, **~48%** cov); merge-first Quality failed on test stub only — **`test/quality/test_runtime_mock.py`** fixed on **`main`**. **`docs/milestones/M34/M34_run1.md`**, **`M34_summary.md`**, **`M34_audit.md`**. **`docs/architecture/serena_allowed_legacy_surfaces.md`** M34 note.

**M35:** **Remove tolerated `shared.sd_model` orchestration coupling** — **PR [#91](https://github.com/m-cahill/serena/pull/91)** merge commit **`45e6f4fbfb8f6ed2dfc336423d1f414f66c77549`** (**2026-03-28T00:59:00Z** UTC); branch **`m35-remove-shared-sd-model-orchestration`**. Supported-path orchestration in **`modules/processing.py`** uses **`_orchestration_model(p)`** → **`p.model_provider.get_model(p)`** when **`ProcessingRunner.prepare`** has run; **remaining** direct **`shared.sd_model`** touchpoints: **`StableDiffusionProcessing.sd_model`** compatibility property and **`_orchestration_model`** fallback when **`model_provider`** is absent. **`docs/architecture/serena_allowed_legacy_surfaces.md`** narrowed accordingly. **No** CI policy change. **PR approval** head **`564ebd27`** — Linter **`23673315409`**, Smoke **`23673315420`**. **Binding post-merge** on **`main`**: Linter **`23673838902`**, Quality **`23673838908`** (**203** pass, **48%** cov). **`docs/milestones/M35/M35_run1.md`**, **`M35_summary.md`**, **`M35_audit.md`**.

**M36:** **Coverage lift and gate recalibration** — **PR [#92](https://github.com/m-cahill/serena/pull/92)** merge commit **`ab4c4679397091ef8de2d46db3afadf3113a6979`** (**2026-03-28T04:02:44Z** UTC); branch **`m36-coverage-lift-gate-recalibration`**. Targeted **`test/quality`** additions for **`ModelProvider`** / **`_orchestration_model`**, **`RuntimeContext`** / **`ModelIdentity`**, **`ProcessingRunner`** / **`ExecutionQueue`**, M35 **`p.sd_model`** compatibility — **no** runtime behavior change intended. **PR merge tip** **`c410771f`** — Linter **`23676919831`**, Smoke **`23676919933`**. **Binding post-merge** on **`main`**: Linter **`23677054517`**, Quality **`23677054515`** (**213** pass, **48%** TOTAL); **Quality** **`--fail-under`** remains **42%** (no threshold increase — measured TOTAL unchanged vs M35 band). **`docs/milestones/M36/M36_run1.md`**, **`M36_summary.md`**, **`M36_audit.md`**.

**M37:** **Security deferral closure and final 5/5 re-audit** — **PR [#93](https://github.com/m-cahill/serena/pull/93)** → merge **`18c13a59b73de16f85c7dacd57162ac55713b1aa`**; branch **`m37-security-deferral-final-audit`**. Re-checked **M28** **`pip-audit`** deferrals: **CVE-2025-69872** (**diskcache**), **CVE-2026-4539** (**pygments**). **PyPI** did not offer **installable** fixed versions at closeout (**`pygments 2.19.3`** absent; **`diskcache`** still **5.6.3** latest). **No** workflow or lockfile change; **blocking** **`pip-audit`** unchanged. **Phase VIII** program objectives **complete**; **residual** advisory posture **externally** bounded. **`docs/milestones/M37/M37_run1.md`**, **`M37_summary.md`**, **`M37_audit.md`**; **`ci_environment_contract.md`** M37 note.

---

### Phase V ? UI & Extension Stabilization (Complete)

Phase V ? UI & Extension Stabilization **complete**. Top-level UI modularized, extension API versioned, deprecation channel established.

> **M21?M23:** Tab registry and modularized txt2img, img2img, settings, extensions. **M24:** Extension API v1 contract. **M25:** Deprecation scaffolding without registry drift.

### Phase VI ? Hardening & Reproducibility (M26–M30)

**M26 ? Locked manifests & CI environment stabilization** **complete.** Quality CI installs from a **committed lockfile**; npm uses **`npm ci`**; **artifact-level** reproducibility and **`ci_environment_contract.md`** encode the environment.

**M27 ? Coverage and complexity gates** **complete** — coverage enforced (**≥42%**, pytest-only gate post-**#63**), **Radon** visibility (warn-first), **measurement corrected** via explicit governance.

**M28 ? Security & supply-chain hardening** **complete** — **blocking `pip-audit`** on Quality; **M28b** dependency remediation; **two** explicit **PyPI-unfixable** deferrals (**diskcache**, **pygments**) via **`--ignore-vuln`** + documentation; any new advisory **fails** until fixed or governed.

**M29 ? Health & performance verification** **complete** — runner **`runtime_metrics`**, DEBUG API timing, **`performance_snapshot.txt`** on binding **Quality `23618918747`** (**M29.1**/**M29.2** recovery: **PR #79**, **#80**, **#81**).

**M30 ? QA / evidence publishing** **complete** — **PR #82** merge **`b663f735`**; **`serena_evidence_bundle.md`**, **`serena_case_study_summary.md`**, **`serena_evidence_matrix.md`**; **`M30_run1.md`** (**M28**/`main`/`PR #64` note); tag **`v0.0.30-m30`**. **Doc-only** milestone.

**M31 ? Architecture lock** **complete** — **PR #83** → merge **`09f1d785`**; **`serena_architecture_lock.md`**, **`serena_allowed_legacy_surfaces.md`**, **`M31_run1.md`**; ledger hierarchy updated; **doc-only** (2026-03-26 ~23:55 UTC).

**M32 ? Evidence/audit closure** **complete** — **PR #86** → merge **`3f6f6a2e`** (2026-03-27 ~00:06 UTC); **`M32_run1.md`**, **`M32_summary.md`**, **`M32_audit.md`**; bundle/matrix index updates; **doc-only**.

**M33 ? Release-ready 5/5 close** **complete** — **PR #88** → merge **`ebb44177`**; **`docs/milestones/M33/`**; **Phase VII** **closed** at **M33**; **doc-only**; tag **`v0.0.33-m33`** @ **`ebb44177`**; provenance **`M33_run1.md`** §9. **Phase VIII** **complete** — **M34**–**M37** finished; final deferral posture documented in **`docs/milestones/M37/`** — **`docs/serenav1audit.md`**.

---

### Phase IV ? Runtime Extraction (Complete)

Orchestration (M16), **sampler execution (M17)**, **decode/postprocess/save for process_images_inner (M18)**, **model provider injection (M19)**, and **mockable runtime proof (M20)** are complete.

> **Inner-loop decode, postprocess, and save run through `decode_runtime`; script hook call sites stay in processing.py.**

> **Runtime decoupled from global model state via ModelProvider** (M19); **end-to-end inner pipeline executable without a real model in tests** (M20).

> **Runtime validated as fully mockable; end-to-end pipeline executes without real model. Phase IV complete.**

---

## 5. Standing Invariants

Repo-wide non-negotiables for this program:

- **No silent behavior drift** ? All changes must preserve or explicitly document behavior
- **No CI weakening** ? Do not relax checks, thresholds, or truthfulness
- **Preserve extension behavior** ? Unless intentionally versioned in a milestone
- **Preserve API/UI semantics** ? Unless milestone explicitly approves change
- **Evidence-first closeout** ? Every milestone closes with documented evidence

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
