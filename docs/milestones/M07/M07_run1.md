# M07 CI Run 1 — Opts Snapshot Introduction

**Date:** 2026-03-10  
**Branch:** m07-opts-snapshot  
**PR:** #22  
**Trigger:** pull_request (PR to main)

---

## 1. Workflow Identity

| Workflow | Run ID | Trigger | Branch | Commit | Status |
|----------|--------|---------|--------|--------|--------|
| Smoke Tests | 22920401686 | pull_request | m07-opts-snapshot | 87c8fe86 | ✓ success |
| Linter | 22920401661 | pull_request | m07-opts-snapshot | 87c8fe86 | ✓ success |

**Quality Tests:** Not yet run (triggered on push to main; will run post-merge).

---

## 2. Change Context

| Item | Value |
|------|-------|
| Milestone | M07 — Opts snapshot introduction |
| Phase | Phase II — Runtime Seam Preparation |
| Posture | Behavior-preserving |
| Refactor target | `modules/opts_snapshot.py` (new), `modules/processing.py` (modified) |
| Run type | First CI verification of M07 implementation |

---

## 3. Step 1 — Workflow Inventory

### Smoke Tests (22920401686)

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

**Duration:** 2m44s

### Linter (22920401661)

| Job | Required? | Purpose | Pass/Fail |
|-----|-----------|---------|-----------|
| ruff | Yes | Python lint | ✓ |
| eslint | Yes | JS lint | ✓ |

---

## 4. Step 2 — Refactor Signal Integrity

### A) Tests

- **Tier:** Smoke only (test/smoke)
- **Coverage of refactor target:** Smoke tests exercise txt2img and img2img API endpoints, which call `process_images()` → `process_images_inner()` → `prepare_prompt_seed_state(p)` → `create_opts_snapshot(shared.opts)`. The opts snapshot is captured on the critical path before sampling.
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
| Generation behavior unchanged | Smoke tests pass; snapshot is write-only | ✓ |
| Override logic unchanged | temporary_opts() unchanged; snapshot captured after overrides | ✓ |
| Extension compatibility | shared.opts reads unchanged; p.opts_snapshot not yet read by runtime | ✓ |
| API compatibility | txt2img/img2img smoke tests pass | ✓ |
| No opts reads replaced | All opts. / shared.opts reads remain; M08 will thread snapshot | ✓ |

---

## 6. Blast Radius

**Files changed:**
- `modules/opts_snapshot.py` (new)
- `modules/processing.py` (modified)
- `docs/milestones/M07/*`

**No other modules changed.** Invariant registry surfaces (CLI, API, file formats, extension API, generation semantics) preserved.

---

## 7. Verdict

**CI Status:** Green (Linter ✓, Smoke Tests ✓)

**Refactor posture:** Behavior-preserving infrastructure preparation. Snapshot is write-only; no runtime reads replaced.

**Next step:** Await merge permission. Post-merge Quality Tests will run (coverage, pip-audit, verify_pinned_deps). M07 run analysis complete; ready for M07 audit and summary generation after closeout.
