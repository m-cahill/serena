# M18 Run 2 — Post-Merge CI Analysis

**Milestone:** M18 — Decode/save separation  
**Merge commit:** 84ea94e7  
**PR:** [#36](https://github.com/m-cahill/serena/pull/36) (merged)

---

## 1. Post-Merge Workflows

| Workflow | Run ID | Trigger | Result | Duration |
|----------|--------|---------|--------|----------|
| Linter | [23321103971](https://github.com/m-cahill/serena/actions/runs/23321103971) | push to `main` | ✓ success | — |
| Quality Tests | [23321103961](https://github.com/m-cahill/serena/actions/runs/23321103961) | push to `main` | ✓ success | ~4m16s wall (job ~4m12s) |

---

## 2. Quality Tests Job Details

| Step | Result |
|------|--------|
| Verify repository, ref | ✓ |
| Checkout Code | ✓ |
| Set up Python 3.10 | ✓ |
| Install dependencies | ✓ |
| Dependency vulnerability scan | ✓ |
| Verify pinned dependencies | ✓ |
| Setup environment | ✓ |
| Start test server | ✓ |
| **Run quality tests** | ✓ **79 passed** (19 warnings) in ~68.7s |
| **Show coverage** | ✓ **40%** total (combined report); `--fail-under=40` satisfied |
| Upload artifacts | ✓ |

**Suite notes:** Includes `test/quality/test_decode_runtime.py` (4 tests), existing runner/sampler/processing_runtime contract tests, and the rest of the quality tier.

**Annotations (informational):** Node.js 20 deprecation notice; pip-audit remediation deferred to M27 (unchanged policy).

---

## 3. Delta vs Run 1

| Check | Run 1 (PR / branch) | Run 2 (Post-merge) |
|-------|---------------------|----------------------|
| Linter | ✓ (push + PR) | ✓ on `main` @ merge SHA |
| Smoke Tests | ✓ (PR #36) | Exercised via Quality environment / server startup path |
| Quality Tests | Pending (workflow is `main` push only) | ✓ Run 23321103961 |
| Coverage report | — | ✓ 40% gate |
| `test_decode_runtime` | — | ✓ in Quality tier |
| Runner + sampler contracts | — | ✓ unchanged, still passing |
| Quality job duration (reference) | — | ~4m12s job vs M17 run2 ~3m54s (dependency/install variance; no regression signal) |

---

## 4. Evidence Summary

| Check | Expected | Actual |
|-------|----------|--------|
| Linter (PR) | ✓ | ✓ Run 1 |
| Smoke Tests (PR) | ✓ | ✓ Run 1 |
| Quality Tests (`main`) | ✓ | ✓ Run 2 |
| Coverage | ≥ 40% | ✓ |
| M18 delegation / order tests | ✓ | ✓ `test_decode_runtime.py` |

---

## 5. Verdict

Post-merge CI green. No fixes required. M18 closeout evidence complete.
