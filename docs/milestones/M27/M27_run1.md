# M27 — CI run log

**PR #54:** [merged](https://github.com/m-cahill/serena/pull/54) → `d1897cf2668b6df35b233e9b0da2e0d135aa4773`  
**PR #55:** [merged](https://github.com/m-cahill/serena/pull/55) — coverage follow-up tests  
**PR #56:** [merged](https://github.com/m-cahill/serena/pull/56) — drop flaky `refresh-embeddings` POST from Quality  
**PR #57:** [merged](https://github.com/m-cahill/serena/pull/57) — prompt-parser + options API bulk coverage (**no net TOTAL delta** vs attempt 3: same **11237** miss).  
**PR #58:** [merged](https://github.com/m-cahill/serena/pull/58) — util + `errors` tests.  
**PR #59:** [merged](https://github.com/m-cahill/serena/pull/59) — fix `display_once` assertion.  
**PR #60:** `images` + `extras` cold-path tests _(pending merge)_.

---

## Quality attempt 1 — **fail (coverage)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | [23473843412](https://github.com/m-cahill/serena/actions/runs/23473843412) | **fail** | **40%** < **42%**; **116** tests passed; Radon skipped. |

```text
TOTAL ... 40%
Coverage failure: total of 40 is less than fail-under=42
```

---

## Quality attempt 2 — **fail (pytest)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | [23509328890](https://github.com/m-cahill/serena/actions/runs/23509328890) | **fail** | **`POST /sdapi/v1/refresh-embeddings`** non-200 (TI reload / 5xx). **#55** merged; Radon skipped. |

**Remediation:** **#56** removed `refresh-embeddings` from parametrized POST tests (commented rationale in `test_api_extended.py`).

---

## Quality attempt 3 — **fail (coverage)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | [23509549518](https://github.com/m-cahill/serena/actions/runs/23509549518) | **fail** | All tests passed; **Show coverage**: **40%** (18844 stmts, **11237** miss, **7607** hit) < **42%**. Radon skipped. |

Net vs attempt 1: **+36** covered statements (**7571 → 7607**), still **~308** short of **7915** (~42%).

**Remediation:** **#57** — `test_m27_coverage_wave2.py`: `parse_prompt_attention`, `get_learned_conditioning_prompt_schedules`, `get_multicond_prompt_list`, options POST round-trip, extra infotext/override helpers.

---

## Quality attempt 4 — **fail (coverage, no progress)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | [23509818680](https://github.com/m-cahill/serena/actions/runs/23509818680) | **fail** | Tests passed; **TOTAL** unchanged (**18844** stmts, **11237** miss, **40%**). **#57** only re-hit already-covered lines (e.g. `prompt_parser`). Radon skipped. |

**Remediation:** **#58** — `test_m27_util_errors_coverage.py` targets **`modules/util.py`** and **`modules/errors.py`** (previously thin in the combined report).

---

## Quality attempt 5 — **fail (coverage, util/errors duplicate hits)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | [23510044040](https://github.com/m-cahill/serena/actions/runs/23510044040) | **fail** | Pytest: `test_display_once_dedupes` _(fixed in **#59**)._ |
| Quality (`main`) | [23510268169](https://github.com/m-cahill/serena/actions/runs/23510268169) | **fail** | Tests pass; **TOTAL** still **18844 / 11237 miss (40%)** — `util`/`errors` lines were **already** counted hit in the combined report. |

**Remediation:** **#60** — `test_m27_images_extras_cold.py` (`image_grid`, `split_grid`/`combine_grid`, `extras.to_half`, etc.) to reach **uncovered** statements in **`modules/images.py`** / **`modules/extras.py`**.

---

## Quality attempt 6 (binding)

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | _(after #60)_ | | **≥42%**, Radon + artifact if green. |

---

## Linter / Smoke

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| _(optional)_ | | | Fill from PR checks when closing M27. |

---

## Final verdict

**Pending:** Quality **attempt 6** green on `main` after **#60**. Then audit / summary / `docs/serena.md` per permission.
