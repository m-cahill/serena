# M27 — CI run log

**PR #54:** [merged](https://github.com/m-cahill/serena/pull/54) → `d1897cf2668b6df35b233e9b0da2e0d135aa4773`  
**PR #55:** [merged](https://github.com/m-cahill/serena/pull/55) — coverage follow-up tests  
**PR #56:** [merged](https://github.com/m-cahill/serena/pull/56) — drop flaky `refresh-embeddings` POST from Quality  
**PR #57:** [merged](https://github.com/m-cahill/serena/pull/57) — prompt-parser + options API bulk coverage (**no net TOTAL delta** vs attempt 3: same **11237** miss).  
**PR #58:** [merged](https://github.com/m-cahill/serena/pull/58) — util + `errors` tests.  
**PR #59:** [merged](https://github.com/m-cahill/serena/pull/59) — fix `display_once` assertion.  
**PR #60:** [merged](https://github.com/m-cahill/serena/pull/60) — `images` + `extras` cold-path tests.  
**PR #61:** [merged](https://github.com/m-cahill/serena/pull/61) — drop sampler-config image tests (CI has no `Euler a` config).

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

## Quality attempt 6 — **fail (pytest then coverage)**

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| Quality (`main`) | [23510513615](https://github.com/m-cahill/serena/actions/runs/23510513615) | **fail** | **#60:** `get_scheduler_str` / `get_sampler_scheduler` — **`find_sampler_config` returned `None`** in CI. |
| Quality (`main`) | [23510740367](https://github.com/m-cahill/serena/actions/runs/23510740367) | **fail** | **#61:** tests pass; **TOTAL** still **18844 / 11237 miss (40%)** — same as attempts 3–5. |

---

## Diagnosis — **why extra tests are not moving the gate**

Quality **combines** coverage from (1) the **long-running server** (`coverage run … launch.py`) and (2) **pytest**. Any statement already executed during server startup stays **hit** in the merged data set; pytest tests that call the same `modules/*` paths **do not increase** the numerator.

The remaining **11237** misses are concentrated in code paths **neither** the server nor the current tests reach (large legacy surfaces: merge/train/exotic model stacks, etc.). Raising **`fail-under` by +2** without changing **measurement scope** (omit list) or **which runs feed the gate** (e.g. pytest-only) implies **hundreds of genuinely new** statement executions — not duplicates of startup-imported modules.

**Governance fork (needs explicit milestone decision, not silent CI weakening):**

1. **Expand `[tool.coverage.run] omit`** for frozen legacy trees out of Serena scope (shrinks denominator; must be documented).  
2. **Gate on pytest-only** combined data (excludes server `.coverage*`), or split metrics.  
3. **Revert `fail-under` to 40%** until a dedicated coverage milestone maps cold paths (user has ruled this out unless re-approved).

---

## Linter / Smoke

| Workflow | Run ID | Result | Notes |
|----------|--------|--------|-------|
| _(optional)_ | | | Fill from PR checks when closing M27. |

---

## Final verdict

**Blocked on governance:** **`--fail-under=42`** is not satisfied with the **current** combined server+pytest report (**40%**, **11237** miss). Further **contract tests alone** are unlikely to move the TOTAL until one of the **Diagnosis** options above is chosen. **Radon** has not run on a green Quality job in this sequence (coverage step fails first).

**Next:** program decision on **measurement scope** vs **threshold** vs **dedicated integration coverage** work — then either adjust contract explicitly or continue targeted cold-path work with a clear coverage map.
