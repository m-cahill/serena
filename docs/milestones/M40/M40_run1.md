# M40 — Run 1 (baseline, recovery, binding Quality)

## A. Pre-M40 binding baseline (from ledger)

| Metric | Value | Source |
|--------|-------|--------|
| Quality tests (pass count) | 222 | M39 binding `main` |
| Total coverage (pytest-only) | ~48% | Same |
| Coverage gate (`--fail-under`) | 42% | `run_quality_tests.yaml` |

## B. Target modules (M40 scope)

| Priority | Module |
|----------|--------|
| A | `modules/processing_helpers.py` |
| A | `modules/processing_infotext.py` |
| A | `modules/processing_types.py` |
| B | `modules/runtime/processing_runtime.py` |

## C. Implementation PRs

| PR | Purpose | Merge commit on `main` |
|----|---------|-------------------------|
| [#96](https://github.com/m-cahill/serena/pull/96) | M40 tests + milestone stubs | `75f9bb33` |
| [#97](https://github.com/m-cahill/serena/pull/97) | Defer `processing_infotext` / `processing_types` imports until after `initialize` | `b2c13eaf` |
| [#98](https://github.com/m-cahill/serena/pull/98) | Defer `processing_runtime` import | `5bff4c1a` |
| [#99](https://github.com/m-cahill/serena/pull/99) | Defer `processing_helpers` module-level import | `acce4474` |
| [#100](https://github.com/m-cahill/serena/pull/100) | Test assertion fixes (random tensor shape; `token_merging_ratio` on instance) | `15dcdb59` |

**PR #96 approval head (historical):** `696971ce` — Linter **23721581850**, Smoke **23721581839** (green).

**Root cause of recovery chain:** Module-level imports during **pytest collection** ran before `shared.opts` / full `sd_models` init, causing `AttributeError` on `hide_samplers` or `model_path`. Fix: **no** eager imports of those modules; **`initialize`** on every test that imports them; imports **inside** test bodies.

## D. Binding post-merge Quality (`main`)

| Field | Value |
|--------|--------|
| **Run ID** | `23722341901` |
| **URL** | https://github.com/m-cahill/serena/actions/runs/23722341901 |
| **`main` tip (merge commit)** | `15dcdb59ce0d7a04943102c55820703f623b46a5` |
| **Pass count** | **243** |
| **TOTAL (pytest-only)** | **49%** |
| **Gate** | **42%** unchanged (`coverage report --fail-under=42` passed) |

## E. Per-file coverage (post-M40, target modules)

From the binding run’s coverage table (pytest phase):

| Module | Stmts | Miss | Cover |
|--------|------:|-----:|------:|
| `modules/processing_helpers.py` | 94 | 25 | **73%** |
| `modules/processing_infotext.py` | 39 | 7 | **82%** |
| `modules/processing_types.py` | 765 | 416 | **46%** |
| `modules/runtime/processing_runtime.py` | 60 | 10 | **83%** |

Pre-M40 per-file baselines were not recorded in a prior artifact; **TOTAL** moved from **~48%** (M39) to **49%** on this binding run.

## F. Gate decision

**Coverage gate remains 42%.** Total improved by ~1 percentage point; **not** raised to 44% — consistent with M36 policy (earned, stable buffer required before raising the floor).

### Closeout

**M40 implementation closed:** **2026-03-30T00:07:07Z** UTC (merge commit **`15dcdb59`** for PR **#100**); binding Quality **`23722341901`** on push to **`main`** (Linter **`23722341896`**).

## G. Documentation closeout PR (ledger, summary, audit, M41 stubs)

| Field | Value |
|--------|--------|
| **PR** | [#101](https://github.com/m-cahill/serena/pull/101) |
| **Merge commit** | `e07b31edcd58e1bf9a99887a8fef7058e5dce15d` |
| **Approval head** | `dfcbfa5c215532e61ed969d491e9ce07ded372a4` |
| **PR CI** | Linter **`23722485873`** (ruff + eslint **success**); Smoke **`23722485863`** (**success**) |
| **Post-merge `main` Quality** | **`23722553628`** — https://github.com/m-cahill/serena/actions/runs/23722553628 (**243** collected items, **49%** TOTAL, **`--fail-under=42`** satisfied) |

Doc-only; confirms **`main`** remains green after milestone artifacts land.
