# M20 Milestone Audit

**Milestone:** M20 — Runtime tests with mockable boundaries  
**Target score:** 5.0 / 5  
**Verdict:** **5.0 / 5**

---

## 1. Scope compliance

| Criterion | Evidence |
|-----------|----------|
| No runtime code changes | Diff limited to `test/fixtures/*`, `test/quality/test_runtime_mock.py`, and milestone docs. No edits under `modules/runtime/{processing_runtime,sampler_runtime,decode_runtime,model_provider}.py`. |
| Runner-only test entry | Tests use `ProcessingRunner(model_provider=...).run(ProcessingRequest(p))` only. |
| Provider injection exercised | `FakeModelProvider.get_model` used by real runtime code paths; call-count test asserts usage. |
| Determinism / failure contracts | Structural equality test; `pytest.raises` for propagated provider error. |

---

## 2. CI truthfulness

| Criterion | Evidence |
|-----------|----------|
| Gates unchanged | Linter, Smoke, Quality, `--fail-under=40` unchanged. |
| Quality green | Run [23333740069](https://github.com/m-cahill/serena/actions/runs/23333740069): **87** tests passed, **40%** coverage after combine. |
| Failed first merge run | Documented in `M20_run2.md`; fixed with **test-only** adjustments (dataclass init, CPU autocast, `FakeModel` surface, opts snapshot defaults for CI). No weakening of thresholds. |

---

## 3. Test quality

| Criterion | Evidence |
|-----------|----------|
| No test ordering dependence | Each test builds fresh `p` / runner; fixture restores `shared.sd_model`. |
| Isolation | Monkeypatches scoped to fixture + pytest undo. |
| Honest about glue | `shared.sd_model` aligned with provider return value for `process_images_inner` metadata (documented in run1/run2). |

---

## 4. Behavior preservation

- No change to production code paths for real generation; additions are **test infrastructure** and **documentation** only.

---

## 5. Conclusion

M20 meets the program bar: **mockable runtime boundary proven in CI**, **no runtime refactor in scope**, **CI honest and green** at closeout.

**Score: 5.0 / 5**
