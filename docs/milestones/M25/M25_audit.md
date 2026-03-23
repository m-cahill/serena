# M25 Milestone Audit

**Milestone:** M25 — Deprecation & compatibility scaffolding  
**Mode:** Delta audit  
**Target score:** 5.0 / 5  
**Verdict:** **5.0 / 5**

---

## 1. Scope compliance

| Criterion | Evidence |
|-----------|----------|
| `modules/deprecation.py` added | `warn_deprecated`, `@deprecated`, `format_extension_api_deprecation`; no `script_callbacks` import (no cycles). |
| `deprecate_callback` present | `script_callbacks.py`; uses shared message formatter + `warnings.warn(..., stacklevel=2)` for correct caller attribution. |
| No `callback_map` change | Dict keys/values unchanged; M25 block and function **after** map definition only. |
| No invocation order change | No edits to `ordered_callbacks` or `*_callback` dispatch paths. |
| No registry change | `extension_api.SUPPORTED_CALLBACKS` unchanged; quality tests assert set equality vs `callback_map`. |
| No runtime change | No edits under `modules/runtime/` or generation pipeline. |
| CI gates unchanged | Linter, Smoke, Quality; `fail-under=40` not relaxed. |

---

## 2. CI truthfulness

| Criterion | Evidence |
|-----------|----------|
| PR green | ruff, eslint, smoke — `M25_run1.md` / PR #44 checks. |
| Post-merge Quality green | [23421440167](https://github.com/m-cahill/serena/actions/runs/23421440167): **success**, **112 passed**, coverage **40%** (gate **≥ 40%**). |

---

## 3. Test quality

| Criterion | Evidence |
|-----------|----------|
| No full render / signature introspection | Per locked design. |
| Drift prevention | `SUPPORTED_CALLBACKS` ↔ `callback_map` equality; key count check; warning message assertions. |

---

## 4. Conclusion

M25 meets the program bar: **deprecation infrastructure** and **documented policy** with **no behavioral or registry drift**, **CI honest** at closeout.

**Score: 5.0 / 5**
