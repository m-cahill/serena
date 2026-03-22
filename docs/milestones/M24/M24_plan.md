# M24 Plan — Extension API Version & Contract Stabilization

**Milestone:** M24  
**Phase:** Phase V — UI & Extension Stabilization  
**Branch:** `m24-extension-api-contract`  
**Baseline:** `main` @ M23 tag / closeout (`64c232c3` merge)  
**Status:** In progress

---

## 1. Intent

Formalize the extension hook **surface** without changing behavior:

- Declared **`EXTENSION_API_VERSION`** and **`SUPPORTED_CALLBACKS`** (category strings).
- Architecture doc **`docs/architecture/extension_api_contract_v1.md`**.
- Quality tests: version string, **exact set equality** between `SUPPORTED_CALLBACKS` and categories derived from `callback_map` (`key.removeprefix("callbacks_")`).
- Policy comment block immediately **above** `callback_map` in `script_callbacks.py`.

---

## 2. Locked design

- **Canonical IDs:** category strings (not raw `callbacks_*` keys); derive with `removeprefix("callbacks_")` (e.g. `callbacks_on_reload` → `on_reload`).
- **`set(SUPPORTED_CALLBACKS) == set(derived)`** — exact match, no subset/superset.
- **Tests:** category names only; parameter shapes documented in markdown only — **no** signature introspection.
- **`extension_api.py`:** constants + tuple only — **no** import of `script_callbacks`.
- **Out of scope:** changing invocations, `ordered_callbacks`, extension loading, `Script` API, registry, runtime.

---

## 3. Deliverables

- `modules/extension_api.py`
- `docs/architecture/extension_api_contract_v1.md`
- `test/quality/test_extension_api_contract.py`
- `modules/script_callbacks.py` — contract banner only (above `callback_map`)
- `docs/milestones/M24/M24_plan.md`, `M24_toolcalls.md`
- `docs/serena.md` — M24 row **In progress** (same PR as implementation)

---

## 4. Verification

- PR: ruff, eslint, smoke  
- Post-merge: Quality, coverage ≥ 40%

---

## 5. Definition of done

- PR green; Quality green on `main`; ledger **Completed**; audit 5.0/5; tag **`v0.0.24-m24`** on squash merge commit.
