# M20 Run 2 — Post-Merge Quality Tests (PASS)

**Milestone:** M20 — Runtime tests with mockable boundaries  
**Phase:** Phase IV — Runtime Extraction  
**Run type:** Post-merge (`push` to `main`)  
**Run ID:** [23333740069](https://github.com/m-cahill/serena/actions/runs/23333740069)  
**Head SHA:** `9c7e693a`  
**Trigger commit message:** `fix(M20): patch opts snapshot defaults for sparse CI opts.data`  
**Conclusion:** SUCCESS  
**Workflow duration:** ~3m51s (started 2026-03-20T07:47:15Z, completed ~07:51Z UTC)

---

## 1. Results

| Step | Result |
|------|--------|
| Run quality tests | ✓ **87 passed** in ~67s (includes 4× `test_runtime_mock.py`) |
| `coverage report --fail-under=40` | ✓ **40%** combined TOTAL (18715 stmts, 11247 miss) |
| Pytest phase coverage line | TOTAL **43%** during pytest-cov (informational) |

---

## 2. Superseded / failed runs (diagnostic only)

PR [#39](https://github.com/m-cahill/serena/pull/39) merged at `5b37c457`. First Quality on `main` (**23332146363**) failed on **`test_runtime_mock`**: `StableDiffusionProcessingTxt2Img` does not accept `scripts=` in `__init__` (`init=False` on dataclass).

**Resolution:** test-only fixes on `main` (no runtime module edits): set `p.scripts` after construction; skip TI reload; CPU-safe autocast/randn; expand `FakeModel` flags for sampler/conditioning glue; `sd_checkpoint_info.model_name`; patch `create_opts_snapshot` in tests to backfill keys missing from sparse CI `opts.data` (e.g. `grid_only_if_multiple`).

---

## 3. Relevant tests

All passed, including:

- `test/quality/test_runtime_mock.py` (4 tests) — runner + `FakeModelProvider`, full stubbed inner path
- Existing runtime / provider / decode / sampler quality tests

---

## 4. Checklist

- [x] `test_runtime_mock` passed  
- [x] No regressions in existing quality tests  
- [x] Coverage ≥ 40%  

---

## 5. Delta vs Run 1 (PR phase)

| Metric | Run 1 (PR #39) | Run 2 (main, final) |
|--------|----------------|---------------------|
| Linter | [23331851493](https://github.com/m-cahill/serena/actions/runs/23331851493) ✓ | (not re-listed) |
| Smoke | [23331851499](https://github.com/m-cahill/serena/actions/runs/23331851499) ✓ | exercised inside Quality job |
| Quality | N/A on PR | **23333740069** ✓ |

---

## 6. Notes

- pip-audit: informational (`continue-on-error` per workflow).  
- Node.js 20 deprecation warnings on actions (informational).  
- `htmlcov` artifact missing when pytest fails early (expected on failed runs only).
