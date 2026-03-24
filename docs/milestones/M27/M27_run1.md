# M27 — CI run log

**PR #54:** [merged](https://github.com/m-cahill/serena/pull/54) → `d1897cf2668b6df35b233e9b0da2e0d135aa4773`  
**PR #55:** [merged](https://github.com/m-cahill/serena/pull/55) — coverage follow-up tests  
**PR #56:** [merged](https://github.com/m-cahill/serena/pull/56) — drop flaky `refresh-embeddings` POST from Quality  
**PR #57:** [wave 2 tests](https://github.com/m-cahill/serena/pull/57) — prompt-parser + options API bulk coverage _(merge pending when opened)_

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

## Quality attempt 4 (binding)

**Expected after #57 merge:** combined **≥ 42%**, Radon + **`radon_report.txt`**, D/E/F `::warning` likely.

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | _(after #57)_ | | |

---

## Linter / Smoke

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| _(optional)_ | | | Fill from PR checks when closing M27. |

---

## Final verdict

**Pending:** Quality **attempt 4** green on `main` after **#57**. Then audit / summary / `docs/serena.md` per permission.
