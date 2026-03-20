# M20 Run 2 — Post-Merge Quality Tests

**Milestone:** M20 — Runtime tests with mockable boundaries  
**Phase:** Phase IV — Runtime Extraction  
**Run type:** Post-merge (push to `main`) — **Quality Tests** workflow only

---

## Status (as of report generation)

| Item | State |
|------|--------|
| PR [#39](https://github.com/m-cahill/serena/pull/39) | **Open** (not merged) |
| Quality workflow | **Not triggered** for M20 — runs on `push` to `main` only |

There is **no** Quality run ID yet for the M20 branch merge. Latest Quality on `main` is still from the prior merge (e.g. M19 closeout: run [23327390199](https://github.com/m-cahill/serena/actions/runs/23327390199)), which does **not** include M20 commits.

---

## After PR #39 merges — fill this section

Use:

```bash
gh run list -R m-cahill/serena --workflow "Quality Tests" --branch main --limit 3
```

Then update the table below from the **first** successful run whose commit message or SHA includes the M20 merge.

| Field | Value |
|-------|--------|
| Run ID | _TBD_ |
| URL | _TBD_ |
| Head SHA | _TBD_ |
| Conclusion | _TBD_ |
| Workflow duration | _TBD_ |

### Expected Quality contents

- `pytest test/smoke test/quality` — must include **`test/quality/test_runtime_mock.py`** (4 tests).
- `coverage report --fail-under=40` — gate **≥ 40%** (unchanged).

### Template — results (copy from Actions log)

| Step | Result |
|------|--------|
| Run quality tests | _N passed in ~Xs_ |
| Show coverage | _TOTAL line %_ |

### Confirmation checklist

- [ ] `test_runtime_mock` tests passed
- [ ] No regressions in existing runtime / provider tests
- [ ] Coverage ≥ 40%

---

## Delta vs Run 1 (PR phase)

| Metric | Run 1 (PR #39) | Run 2 (main, post-merge) |
|--------|----------------|---------------------------|
| Linter | [23331851493](https://github.com/m-cahill/serena/actions/runs/23331851493) ✓ | _not re-listed here_ |
| Smoke | [23331851499](https://github.com/m-cahill/serena/actions/runs/23331851499) ✓ | exercised inside Quality job |
| Quality | N/A on PR | _TBD after merge_ |
