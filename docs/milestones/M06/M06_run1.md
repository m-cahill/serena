# M06 CI Run 1 — Prompt / Seed Preparation Extraction

**Date:** 2026-03-10  
**Branch:** m06-prompt-seed-prep  
**PR:** #20  
**Trigger:** pull_request (PR to main)

---

## 1. Workflow Identity

| Workflow | Run ID | Trigger | Branch | Commit | Status |
|----------|--------|---------|--------|--------|--------|
| Smoke Tests | 22889778495 | pull_request | m06-prompt-seed-prep | 92fbf623 | ✓ success |
| Linter | 22889778518 | pull_request | m06-prompt-seed-prep | 92fbf623 | ✓ success |

**Quality Tests:** Not yet run (triggered on push to main; will run post-merge).

---

## 2. Change Context

| Item | Value |
|------|-------|
| Milestone | M06 — Prompt / seed prep extraction |
| Phase | Phase II — Runtime Seam Preparation |
| Posture | Behavior-preserving |
| Refactor target | `modules/processing.py`, new `modules/prompt_seed_prep.py` |
| Run type | First CI verification of M06 implementation |

---

## 3. Step 1 — Workflow Inventory

### Smoke Tests (22889778495)

| Job / Step | Required? | Purpose | Pass/Fail |
|------------|-----------|---------|-----------|
| Verify repository | Yes | Guardrail: m-cahill/serena only | ✓ |
| Verify base branch | Yes | Guardrail: PR targets main | ✓ |
| Checkout Code | Yes | Fetch PR branch | ✓ |
| Set up Python 3.10 | Yes | Runtime | ✓ |
| Cache models | Yes | Deterministic model path | ✓ |
| Install test dependencies | Yes | pytest, coverage | ✓ |
| Install runtime dependencies | Yes | torch, CLIP, open_clip, requirements_versions | ✓ |
| Create stub repositories | Yes | CI fake inference support | ✓ |
| Setup environment | Yes | launch.py --exit | ✓ |
| Smoke startup | Yes | Verify server can start | ✓ |
| Start test server | Yes | Live server for API tests | ✓ |
| **Run smoke tests** | **Yes** | **pytest test/smoke** | **✓** |
| Kill test server | Yes | Cleanup | ✓ |
| Upload main app output | No (always) | Artifact for debugging | ✓ |

**Duration:** 2m40s

### Linter (22889778518)

| Job | Required? | Purpose | Pass/Fail |
|-----|-----------|---------|-----------|
| ruff | Yes | Python lint | ✓ |
| eslint | Yes | JS lint | ✓ |

---

## 4. Step 2 — Refactor Signal Integrity

### A) Tests

- **Tier:** Smoke only (test/smoke)
- **Coverage of refactor target:** Smoke tests exercise txt2img and img2img API endpoints, which call `process_images()` → `process_images_inner()` → `prepare_prompt_seed_state(p)`. The prompt/seed prep seam is on the critical path.
- **Failures:** None
- **Golden/snapshot:** Smoke tests use CI fake inference (deterministic 1×1 PNG); no golden image comparison. API contract (response schema) is exercised.
- **Missing:** Quality tier tests will run on push to main (coverage ≥40%, pip-audit, verify_pinned_deps).

### B) Coverage

- Smoke run does not enforce a coverage gate (Quality Tests do, on push to main).
- Coverage gate: ≥40% (M04 baseline).
- Post-merge Quality run will report coverage.

---

## 5. Step 3 — Invariant Verification

| Invariant | Verification | Status |
|-----------|--------------|--------|
| Prompt lists identical | setup_prompts() unchanged; prepare_prompt_seed_state assumes it ran | ✓ |
| Seed lists identical | Logic moved verbatim; p.all_seeds, p.all_subseeds written to p | ✓ |
| Extension compatibility | p fields unchanged; extensions read p.all_seeds, p.all_subseeds | ✓ |
| API compatibility | txt2img/img2img smoke tests pass | ✓ |
| Generation determinism | CI fake inference deterministic; no logic change | ✓ |

---

## 6. Blast Radius

**Files changed:**
- `modules/prompt_seed_prep.py` (new)
- `modules/processing.py` (modified)
- `docs/milestones/M06/*`

**No other modules changed.** Invariant registry surfaces (CLI, API, file formats, extension API, generation semantics) preserved.

---

## 7. Verdict

**CI Status:** Green (Linter ✓, Smoke Tests ✓)

**Refactor posture:** Behavior-preserving mechanical extraction.

**Next step:** Await merge permission. Post-merge Quality Tests will run (coverage, pip-audit, verify_pinned_deps). M06 run analysis complete; ready for M06 audit and summary generation after closeout.
