# M05 CI Run 1 — Override Isolation / Temporary Opts Seam

**Date:** 2026-03-09  
**Branch:** m05-override-isolation  
**PR:** #18  
**Trigger:** pull_request (PR to main)

---

## 1. Workflow Identity

| Workflow | Run ID | Trigger | Branch | Commit | Status |
|----------|--------|---------|--------|--------|--------|
| Smoke Tests | 22876253113 | pull_request | m05-override-isolation | 5fe82459 | ✓ success |
| Linter | 22876253091 | pull_request | m05-override-isolation | 5fe82459 | ✓ success |

**Quality Tests:** Not yet run (triggered on push to main; will run post-merge).

---

## 2. Change Context

| Item | Value |
|------|-------|
| Milestone | M05 — Override isolation / temporary opts seam |
| Phase | Phase II — Runtime Seam Preparation |
| Posture | Behavior-preserving |
| Refactor target | `modules/processing.py` (override apply/restore), new `modules/runtime_utils.py` |
| Run type | Corrective (first CI verification of M05 implementation) |

---

## 3. Step 1 — Workflow Inventory

### Smoke Tests (22876253113)

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

**Duration:** 2m48s (Run smoke tests ~45s)

### Linter (22876253091)

| Job | Required? | Purpose | Pass/Fail |
|-----|-----------|---------|-----------|
| ruff | Yes | Python lint | ✓ |
| eslint | Yes | JS lint | ✓ |

---

## 4. Step 2 — Refactor Signal Integrity

### A) Tests

- **Tier:** Smoke only (test/smoke)
- **Coverage of refactor target:** Smoke tests exercise txt2img and img2img API endpoints, which call `process_images()` → `temporary_opts` → `process_images_inner`. The override seam is on the critical path.
- **Failures:** None
- **Golden/snapshot:** Smoke tests use CI fake inference (deterministic 1×1 PNG); no golden image comparison. API contract (response schema) is exercised.
- **Missing:** `test_opts_override.py` (quality tier) did not run; it will run on push to main.

### B) Coverage

- Smoke run does not enforce a coverage gate (Quality Tests do, on push to main).
- Coverage gate: ≥40% (M04 baseline).
- Post-merge Quality run will report coverage and run `test_opts_override.py`.

### C) Static / Policy Gates

- Ruff and eslint passed on new and modified files.
- No import boundary breaks, circular deps, or layering violations observed.

### D) Security / Supply Chain

- Not run in Smoke (Quality runs pip-audit).

### E) Performance

- No benchmarks. Smoke tests complete in expected time (~45s for pytest).

---

## 5. Step 3 — Delta Analysis

### Change inventory

| File | Change |
|------|--------|
| modules/runtime_utils.py | New (temporary_opts context manager) |
| modules/processing.py | Modified (use temporary_opts, preserve model/VAE reload, token merging) |
| test/quality/test_opts_override.py | New (unit tests for seam) |
| docs/milestones/M05/* | Plan, toolcalls |

**Public surfaces:** None. API endpoints, CLI, schemas unchanged.

### Expected vs observed

- **Expected:** Override logic relocated to context manager; behavior identical.
- **Observed:** Smoke tests pass; txt2img/img2img path exercises the new seam without regression.

### Refactor-specific drift

- **Signal drift:** None. All required checks ran and passed.
- **Coupling revealed:** None.
- **Hidden dependencies:** None observed.

---

## 6. Step 4 — Failure Analysis

No failures. All jobs passed.

---

## 7. Step 5 — Invariants & Guardrails Check

| Invariant | Status |
|-----------|--------|
| Required checks enforced | ✓ Smoke, Linter both required and passed |
| No scope creep | ✓ Only override seam; no feature work |
| Public surfaces compatible | ✓ API/CLI/schemas unchanged |
| Schema/contract outputs valid | ✓ Smoke exercises API responses |
| Determinism preserved | ✓ CI fake inference; no golden drift |
| No green-but-misleading path | ✓ No skips, continues, or muted gates |

---

## 8. Step 6 — Verdict

**Verdict:** Smoke Tests and Linter both passed. The refactor target (`process_images` → `temporary_opts`) is on the critical path exercised by smoke tests (txt2img, img2img). No behavioral drift observed. Quality Tests (including `test_opts_override.py` and coverage) will run post-merge on push to main.

**Recommended outcome:** ✅ **Merge approved**

---

## 9. Step 7 — Next Actions

| Action | Owner | Scope | Milestone |
|--------|-------|-------|-----------|
| Merge PR #18 | Human | m05-override-isolation → main | M05 |
| Verify Quality run post-merge | Human/Cursor | Run ID, coverage ≥40%, test_opts_override pass | M05 |
| Generate M05_summary, M05_audit, ledger update | Cursor | After Quality green | M05 closeout |

---

## 10. Summary Table

| Check | Run ID | Result |
|-------|--------|--------|
| Smoke Tests | 22876253113 | ✓ success |
| Linter | 22876253091 | ✓ success |
| Quality Tests | 22877674534 | ✗ failed (test_opts_override) |

---

## 11. Quality Run 1 — Post-Merge (22877674534)

**Status:** Failed  
**Cause:** `test_opts_override.py` — 2 failures

### Failure

When `opts.load()` gets `FileNotFoundError` (no config.json), it sets `opts.data = {}`.  
`temporary_opts` only applies overrides for keys in `opts.data`, so no overrides are applied and `samples_save` stays at its default (True).

### Fix

Ensure a minimal config exists before loading webui so `opts.data` is populated.  
Updated `test/conftest.py` `initialize` fixture to create `config.json` with `{"samples_save": True}` when missing.
