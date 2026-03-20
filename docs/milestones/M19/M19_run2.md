# M19 Run 2 — Post-Merge Quality Tests (PASS)

**Milestone:** M19 — Model provider interface  
**Phase:** Phase IV — Runtime Extraction  
**Run type:** Post-merge (push to `main`) after PR #38 (test isolation fix)  
**Run ID:** [23326003636](https://github.com/m-cahill/serena/actions/runs/23326003636)  
**Head SHA:** 8fb464e4  
**Trigger:** Merge pull request #38 from m-cahill/m19-test-fix  
**Conclusion:** SUCCESS  
**Job duration:** ~4m (workflow created 2026-03-20T02:05:03Z, completed 2026-03-20T02:09:07Z)

---

## 1. Results

| Step | Result |
|------|--------|
| Run quality tests | ✓ 83 passed in ~68s |
| Show coverage | ✓ `coverage report --fail-under=40` passed |
| Combined TOTAL | **40%** line coverage (18715 stmts, 11247 miss) |

---

## 2. Relevant tests

All passed, including:

- `test/quality/test_model_provider.py` (4 tests)
- `test/quality/test_sampler_runtime.py`
- `test/quality/test_decode_runtime.py`
- `test/quality/test_processing_runtime.py`
- Runner / queue contract tests

---

## 3. Delta vs Run 1 (PR phase)

| Metric | Run 1 (PR #37) | Run 2 (main, post #38) |
|--------|----------------|-------------------------|
| Linter | 23324037879 ✓ | (not re-listed) |
| Smoke | 23324037884 ✓ | exercised inside Quality job |
| Quality | N/A on PR | **23326003636 ✓** |
| Tests | — | 83 passed |
| Coverage | — | 40% (gate satisfied) |

**Earlier failed Quality (superseded):** Run 23324741811 (post-merge #37 only) failed on `test_model_provider` sampler tests due to `sys.modules` patch vs import cache. Fixed in PR #38 by patching `modules.sd_samplers.create_sampler`.

---

## 4. Notes

- pip-audit: informational (continue-on-error per workflow)
- Node.js 20 deprecation warnings on actions (informational)
