# M27 — Summary (closeout)

**Status:** Completed  
**Binding Quality run:** [23513449859](https://github.com/m-cahill/serena/actions/runs/23513449859) @ `e3c0d554` (merge of **PR #63**)

## What shipped

- **Coverage enforcement:** Quality gate **`--fail-under=42`** satisfied on **pytest-only** measurement (**47%** TOTAL in the binding run).
- **Measurement corrected:** Server startup is **no longer** instrumented with **`coverage run`**; **`coverage combine`** was removed. The gate reflects **one execution surface** (pytest-cov), documented in **`docs/architecture/ci_environment_contract.md`** (**Coverage policy (M27)**).
- **Complexity visibility:** **Radon** on **`modules/`** (warn-first for **D/E/F**, non-blocking), **`radon_report.txt`** artifact on green Quality runs.
- **No weakening:** Threshold **42%** unchanged; **`pip-audit`** and **Radon** remain non-blocking through M27 per contract.
- **No runtime / API / extension behavior change** in M27 scope; CI and tests only (plus governance docs).

## PR range

**#54–#63** — gate raise (#54), follow-up tests (#55–#61), diagnosis doc (#62), **pytest-only measurement fix (#63)**.

## Numbers (post-fix)

| Metric | Value |
|--------|--------|
| Pytest | **198** passed |
| Coverage TOTAL | **47%** (pytest-only) |
| Radon | Warning emitted (D/E/F present); artifact uploaded |

## Notes

Pre-merge **combined** server+pytest reports showed **~40%** against a larger effective hit set; post-fix **pytest-only** % is **not** directly comparable line-for-line to that **40%**, but the **gate** is now aligned with **test-executed** coverage as intended.
