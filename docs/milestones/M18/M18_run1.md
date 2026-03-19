# M18 Run 1 — CI / Workflow Analysis

**Milestone:** M18 — Decode/save separation  
**Branch:** m18-decode-save-separation  
**PR:** [#36](https://github.com/m-cahill/serena/pull/36)  
**Commit:** 2f6e3e2a  
**Baseline:** M17 on `main` (sampler extraction); pre-merge `main` at fork discretion  

---

## Inputs (workflow identity)

| Item | Value |
|------|-------|
| **Change posture** | Behavior-preserving mechanical extraction |
| **Refactor target** | `process_images_inner` decode → postprocess → save path; new `modules/runtime/decode_runtime.py` |
| **PR target** | `main` |

---

## 0. Workflow runs — actual results (this push / PR)

### Linter (push to branch)

| Item | Value |
|------|-------|
| **Workflow** | Linter |
| **Run ID** | [23320455954](https://github.com/m-cahill/serena/actions/runs/23320455954) |
| **Trigger** | `push` → `m18-decode-save-separation` |
| **Commit** | 2f6e3e2a |
| **Conclusion** | success |
| **Jobs** | ruff ✓, eslint ✓ |

### Linter (PR #36)

| Item | Value |
|------|-------|
| **Workflow** | Linter |
| **Run ID** | [23320478855](https://github.com/m-cahill/serena/actions/runs/23320478855) |
| **Trigger** | `pull_request` (#36) |
| **Commit** | 2f6e3e2a |
| **Conclusion** | success |
| **Jobs** | ruff ✓, eslint ✓ |

### Smoke Tests (PR #36)

| Item | Value |
|------|-------|
| **Workflow** | Smoke Tests |
| **Run ID** | [23320478834](https://github.com/m-cahill/serena/actions/runs/23320478834) |
| **Trigger** | `pull_request` (#36), base `main` |
| **Commit** | 2f6e3e2a |
| **Conclusion** | success |
| **Duration** | ~2m44s (smoke job) |

### Quality Tests

| Item | Value |
|------|-------|
| **Workflow** | Quality Tests |
| **Status** | **Not executed for this branch/PR** (workflow is `push` to `main` only) |
| **Note** | After merge to `main`, expect a Quality run on the merge commit; includes coverage ≥40% gate and `test/quality/test_decode_runtime.py`. |

---

## 1. Workflow inventory

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
|-------------|-----------|---------|-----------|-------|
| ruff | Merge-blocking (PR) | Python lint | ✓ | Runs 23320455954, 23320478855 |
| eslint | Merge-blocking (PR) | JS lint | ✓ | Same |
| smoke tests | Merge-blocking (PR) | E2E server + API smoke | ✓ | Run 23320478834 |
| quality tests | Post-merge on `main` | Contract + coverage + pip-audit | Pending | Triggered only on `main` push |

**Annotations (informational):** GitHub deprecation notices for Node.js 20 on several actions — no job failures; no Serena config change in M18.

---

## 2. Change context

| Item | Value |
|------|-------|
| **Intent** | Relocate VAE decode stack/normalize, face restoration, color correction + overlay, per-row and grid saves from `process_images_inner` into `decode_runtime` |
| **Public API** | `process_images` / `ProcessingRunner` unchanged |
| **Script hooks** | Call sites remain in `processing.py`; ordering preserved |

---

## 3. Refactor signal integrity

### A) Tests

* **Linter:** No violations on changed surface.
* **Smoke:** Green — exercises server startup and API paths relevant to generation pipeline wiring.
* **Quality:** Not yet run for this SHA on CI; new `test_decode_runtime` delegation/order/source checks will run on next `main` push after merge.

### B) Coverage

* Gate enforced in Quality workflow on `main` only; no regression signal from this PR run alone.

### C) Static / policy

* Ruff/eslint aligned with repo gates.
* Lazy import of `apply_color_correction` / `apply_overlay` from `processing` inside `postprocess_images_for_row` avoids load-time cycles; acceptable for M18.

### D) Security / supply chain

* No change in this run set; Quality’s `pip-audit` runs on `main` push.

### E) Performance

* Not measured; extraction is structural only.

---

## 4. Delta analysis

**Files touched (high level):**

* `modules/runtime/decode_runtime.py` (new)
* `modules/processing.py` (delegate inner loop; HR paths call `decode_runtime.decode_latent_batch`)
* `test/quality/test_decode_runtime.py` (new)
* Runtime package docstrings / `processing_runtime` comment

**Expected vs observed:**

* Expected: identical runtime behavior for decode/postprocess/save ordering; script hooks unchanged.
* Observed: PR Linter + Smoke all success; no failures.

---

## 5. Invariants & guardrails

| Invariant | Status |
|-----------|--------|
| CI gates not weakened | ✓ |
| Scope = `process_images_inner` output stage only | ✓ |
| No API/UI contract change | ✓ |
| Script hook order preserved | ✓ (call sites in `processing.py`) |
| “Green but misleading” (missing tier) | ⚠️ Quality not run until merge — **documented** |

---

## 6. Verdict

**Verdict:** For PR #36 at `2f6e3e2a`, **Linter** and **Smoke** are green. The change is a behavior-preserving relocation behind the runtime module; no CI failures. **Quality Tests** have not run on this SHA because they trigger only on `push` to `main`; milestone evidence is complete for PR gating once policy treats Linter + Smoke as the merge blockers, and **Quality must be confirmed after merge** (or via a follow-up run document).

**Recommended outcome:** ✅ **Merge approved** from a PR CI perspective (pending your explicit merge permission per program gates). After merge, record **Quality** run ID in `M18_run2.md` or amend ledger if a single run suffices.

---

## 7. Next actions

| Owner | Action | Milestone |
|-------|--------|-----------|
| Human | Merge PR #36 when ready (per permission gates) | M18 |
| Cursor / human | Capture **Quality Tests** run on merge commit; update `docs/serena.md` with final run IDs + completion timestamp | M18 closeout |
| Human | Optional: bump action versions when addressing Node 20 deprecation (separate hygiene milestone) | TBD |

---

*Analysis format aligned with `docs/prompts/RefactorWorkflowPrompt.md`.*
