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

### Phase III — Runner & Service Boundary (M10–M15)
| Milestone | Title |
|-----------|-------|
| M10 | ProcessingRunner skeleton |
| M11 | Runner lifecycle surface (prepare / execute / finalize) |
| M12 | Runtime instrumentation hooks |
| M13 | txt2img path through runner |
| M14 | API integration |
| M15 | background/queue runner preparation |

### Phase IV — Runtime Extraction (M16–M20)
| Milestone | Title |
|-----------|-------|
| M16 | Runtime module extraction |
| M17 | Sampler runner extraction |
| M18 | Decode/save separation |
| M19 | Model provider interface |
| M20 | Runtime tests with mockable boundaries |

### Phase V — UI & Extension Stabilization (M21–M25)
| Milestone | Title |
|-----------|-------|
| M21 | UI tab registry |
| M22 | txt2img/img2img tab modularization |
| M23 | Settings/extensions modularization |
| M24 | Extension API version/contract |
| M25 | Deprecation/compatibility scaffolding |

### Phase VI — Hardening & Reproducibility (M26–M30)
| Milestone | Title |
|-----------|-------|
| M26 | Locked manifests / npm ci / CI env stabilization |
| M27 | Coverage and complexity gates |
| M28 | Security/supply-chain evidence |
| M29 | Health/perf verification |
| M30 | QA/evidence publishing |

### Phase VII — Release Lock / 5.0 Closure (M31–M33)
| Milestone | Title |
|-----------|-------|
| M31 | Architecture lock |
| M32 | Evidence/audit closure |
| M33 | Release-ready 5/5 close |

---

## 4. Milestone Ledger

| Milestone | Title | Status | Branch | PR | Commit | CI Run(s) | Audit Score / Notes | Completed At |
|-----------|-------|--------|--------|-----|--------|-----------|---------------------|--------------|
| M00 | Program kickoff, baseline freeze, phase map, E2E verification | Completed | m00-kickoff-baseline-e2e | — | cdfe1285 | Linter 22794525690 ✓; Tests 22794525698 ✗ (pre-existing CLIP/pkg_resources) | Baseline 2.4/5 | 2025-03-07 |
| M01 | CI truthfulness, SHA pinning, smoke path | Completed | m01-ci-truthfulness | — | 2f664049 | Linter 22814396752 ✓; Tests 22814850488 (server ✓, 17 pass, img2img/txt2img 500) | 4.7 / 5 | 2026-03-08 |
| M02 | API CI truthfulness, local dev guardrails | Completed | m02-api-ci-truthfulness | — | 7484170d | Linter 22831756517 ✓; Tests 22831756504 ✓ (33/33 pass) | 4.9 / 5 | 2026-03-08 |
| M03 | Test architecture (smoke / quality / nightly) | Completed | m03-test-architecture | #2 | 975dda4b | Linter ✓; Smoke 22834384359 ✓; Quality 22834861040 ✓ | 5.0 / 5 | 2026-03-09 |
| M04 | Coverage/security/reproducibility guardrails | Completed | m04-coverage-guardrails | #4 | 47439cac | Quality 22871471473 ✓ (coverage 40%, pip-audit, verify_pinned_deps) | 5.0 / 5 | 2026-03-09 |
| M05 | Override isolation / temporary opts seam | Completed | m05-override-isolation | #18 (+ #19 fix) | ae161cbb | Quality 22888808682 ✓ | 5.0 / 5 | 2026-03-10 |
| M06 | Prompt/seed prep extraction | Completed | m06-prompt-seed-prep | #20 | 6744152a | Quality 22890285319 ✓ | 5.0 / 5 | 2026-03-10 |
| M07 | Opts snapshot introduction | Completed | m07-opts-snapshot | #22 | 8ea50d35 | Quality 22983583947 ✓ | 5.0 / 5 | 2026-03-12 |
| M08 | Opts snapshot threading | Completed | m08-snapshot-threading | #24 | 710a0abd | Quality 22984445599 ✓ | 5.0 / 5 | 2026-03-12 |
| M09 | Execution context introduction | Completed | m09-execution-context | #26 | 2c6a2510 | Quality 22986731960 ✓ | 5.0 / 5 | 2026-03-12 |
| M10 | ProcessingRunner skeleton | Completed | m10-processing-runner | #27 (+ #28 fix) | 0d11b587 | Quality 22988627838 ✓ | 5.0 / 5 | 2026-03-12 |
| M11 | Runner lifecycle surface | Completed | m11-runner-lifecycle | #30 | 08ac1c0e | Quality 22989978348 ✓ | 5.0 / 5 | 2026-03-12 |
| M12 | Runtime instrumentation hooks | Completed | m12-runner-instrumentation | — | 46cf6d1c | Quality 23037656379 ✓ | 5.0 / 5 | 2026-03-13 |
| M13 | txt2img path through runner | Completed | m13-txt2img-runner | #31 | 4dd04999 | Smoke 23038170275 ✓; Linter 23072709504 ✓; Quality 23072709479 ✓ | 5.0 / 5 | 2026-03-13 |
| M14 | API integration | Completed | m14-api-runner-contract | #32 | 5b7de065 | Smoke 23182483297 ✓; Linter 23182849899 ✓; Quality 23182849888 ✓ | 5.0 / 5 | 2026-03-17 |
| M15 | Queue runner preparation | Completed | m15-queue-runner-prep | #33 | a4b9a622 | Smoke 23227154919 ✓; Linter 23227154926 ✓; Quality 23232040072 ✓ | 5.0 / 5 | 2026-03-18 |
| M16 | Runtime module extraction | Completed | m16-runtime-extraction | #34 | 912f33da | Linter 23276080886 ✓; Smoke 23276080894 ✓; Quality 23283000106 ✓ | 5.0 / 5 | 2026-03-19 06:40 UTC |
| M17 | Sampler runner extraction | Completed | m17-sampler-runner-extraction | #35 | 16bd28ce | Linter 23284575241 ✓; Smoke 23284575264 ✓ (PR); Linter 23318593862 ✓; Quality 23318593847 ✓ | 5.0 / 5 | 2026-03-19 21:54 UTC |
| M18 | Decode/save separation | PR open � Linter + Smoke green; Quality on merge | m18-decode-save-separation | #36 | c22dd9dc | Linter 23320583095 ✓ (push @5c4613f5); Linter 23320584761 ✓; Smoke 23320584759 ✓ (PR @5c4613f5); Quality pending `main` push | — | — |

**M05:** Introduced `temporary_opts()` context manager — first Phase II runtime seam. Isolates override_settings mutation from global `shared.opts`; preserves behavior (opts.set, setattr restore, k in opts.data). Model/VAE reload and token merging remain in process_images. Enables future opts snapshot injection (M07).

**M06:** Extracted `prepare_prompt_seed_state(p)` into `modules/prompt_seed_prep.py`. Second Phase II runtime seam. Populates p.all_seeds and p.all_subseeds; setup_prompts and fill_fields_from_opts unchanged. Enables M07 opts snapshot and M09 execution context.

**M07:** Introduced `create_opts_snapshot(opts)` in `modules/opts_snapshot.py`. Third Phase II runtime seam. Captures deterministic snapshot of opts.data in process_images_inner after prepare_prompt_seed_state; stored on p.opts_snapshot. Write-only in M07; enables M08 snapshot threading.

**M08:** Threaded p.opts_snapshot into process_images_inner for save-related reads. Fourth Phase II runtime seam. Migrated 12 opts (save_images_before_face_restoration, samples_format, grid_save, etc.) from shared.opts to p.opts_snapshot. save_samples(), sample_hr_pass(), metadata unchanged. Enables M09 execution context.

**M09:** Introduced RuntimeContext in modules/runtime_context.py. Fifth Phase II runtime seam. Attached p.runtime_context in process_images_inner() after opts_snapshot (model, opts_snapshot, device, state, cmd_opts). Write-only in M09; no migration of shared.* reads yet. Completes Phase II — Runtime Seam Preparation. Enables Phase III ProcessingRunner.

**M10:** Introduced ProcessingRunner in modules/runtime/runner.py. First Phase III execution boundary. process_images delegates through runner; ProcessingRequest wraps StableDiffusionProcessing. Zero blast radius; all callers unchanged. Phase III roadmap updated (M11 lifecycle, M12 instrumentation, M13 txt2img, M14 API, M15 queue). Enables M11 Runner lifecycle surface.

**M11:** Introduced lifecycle surface on ProcessingRunner: prepare → execute → finalize. run() delegates through stages; pass-through behavior; identical outputs. test_runner_lifecycle_order verifies lifecycle structure. Stable execution surface enables M12 instrumentation, progress hooks, cancellation, queue runners.

**M12:** Introduced optional instrumentation hooks on ProcessingRunner: on_prepare, on_execute, on_finalize. Hooks no-op by default; lifecycle order prepare → on_prepare → execute → on_execute → finalize → on_finalize. test_runner_hooks_called verifies hook invocation. Enables M13+ progress, cancellation, queue runners.

**M13:** Verification milestone. Confirmed txt2img path flows through process_images → ProcessingRunner (no routing changes; M10 already delegates). Added test_txt2img_path_uses_runner contract test. Runner boundary proven with real consumer. Enables M14 API integration.

**M14:** Verification milestone. Confirmed API path flows through process_images → ProcessingRunner (no routing changes). Added test_api_txt2img_uses_runner contract test. API + UI now both contract-proven. CODEOWNERS updated for fork (@m-cahill). Enables M15 queue/background runner.

**M15:** Introduced ExecutionQueue (pass-through) and queue seam in ProcessingRunner. Optional queue wraps execute only; use_queue=False by default. Constructor injection; _execute(state) hook for future orchestration. test_runner_queue_mode verifies queue used, lifecycle preserved, default unchanged. Completes Phase III — Runner & Service Boundary. Enables M16 runtime extraction.

**M16:** Extracted execution-phase batch orchestration into `modules/runtime/processing_runtime.py`. `run_generation_batches(p)` generator handles torch context, init, batch loop, sampler call; yields (n, samples_ddim) per batch. process_images_inner delegates; decode/save/postprocess remain in processing.py. First Phase IV extraction; proves runtime logic can move safely behind runner boundary. Enables M17 sampler runner extraction.

**M17:** Extracted sampler creation and invocation into `modules/runtime/sampler_runtime.py`. `run_sampler_txt2img` and `run_sampler_img2img` delegate from Txt2Img.sample, sample_hr_pass, and Img2Img.sample; script hooks and decode/save remain in processing.py. Img2Img keeps `create_sampler` in `init()` (invocation-only extraction). Second Phase IV extraction; runtime layer now owns batch orchestration (M16) and sampler execution (M17). Enables M18 decode/save separation.

**M18:** Extracted VAE decode stack/normalize, face restoration and color/overlay postprocess, per-row saves (including masks), and grid save from `process_images_inner` into `modules/runtime/decode_runtime.py`. `decode_latent_batch` / `DecodedSamples` moved to decode_runtime to avoid import cycles; HR paths import `decode_runtime.decode_latent_batch` only. Script hooks (`postprocess_batch`, `postprocess_image`, mask overlay, after composite) remain in `processing.py` with unchanged order. Third Phase IV extraction; full txt2img/img2img output pipeline for the inner loop now lives in the runtime module. Enables M19 model provider abstraction.

---

### Phase IV — Runtime Extraction (Started)

Runtime extraction initiated; orchestration (M16), **sampler execution (M17)**, and **decode/postprocess/save for process_images_inner (M18)** are behind the runtime layer.

> **Inner-loop decode, postprocess, and save run through `decode_runtime`; script hook call sites stay in processing.py.**

M19–M20 (model provider, mockable boundaries) follow.

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
