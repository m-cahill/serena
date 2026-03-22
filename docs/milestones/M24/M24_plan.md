# M24 Plan — Extension API Version & Contract Stabilization

**Milestone:** M24  
**Phase:** V — UI & Extension Stabilization  
**Branch:** `m24-extension-api-contract`  
**PR:** [#43](https://github.com/m-cahill/serena/pull/43)  
**Baseline:** `main` @ M23 closeout (merge `64c232c3`)  
**Intent:** Formalize the extension callback surface into an explicit, versioned contract **without altering runtime behavior**.  
**Status:** Completed (2026-03-22)

---

## 1. Intent / target

After M21–M23:

- Top-level UI modularized  
- Runtime extracted and mockable  
- Registry stabilized  
- Extension callbacks still informal and implicitly defined in `script_callbacks.callback_map`

M24 introduces:

- `EXTENSION_API_VERSION = "1.0"` (declarative)  
- `SUPPORTED_CALLBACKS` canonical tuple (category strings)  
- Explicit contract documentation  
- Quality tests locking callback categories against `callback_map`  
- Deprecation policy comment block colocated with `callback_map`

**No behavior change. No extension breakage. No invocation logic modification.**

---

## 2. Scope boundaries

### In scope

#### Code

- **`modules/extension_api.py`**
  - `EXTENSION_API_VERSION = "1.0"`
  - `SUPPORTED_CALLBACKS` (canonical category strings)
  - **No** imports from `script_callbacks`

- **`modules/script_callbacks.py`**
  - Add policy comment block:

    ```
    # === Extension API Contract (v1.0) ===
    ```

    Immediately **above** `callback_map`  
  - **No** logic edits

- **`test/quality/test_extension_api_contract.py`**
  - Assert:
    - Version exists and is string (`"1.0"`)
    - No duplicate entries in `SUPPORTED_CALLBACKS`
    - All keys in `callback_map` start with `"callbacks_"`
    - `set(SUPPORTED_CALLBACKS)` **equals** `{k.removeprefix("callbacks_") for k in callback_map}`

#### Docs

- **`docs/architecture/extension_api_contract_v1.md`** — versioning rules, stability guarantees, deprecation policy, category list, invocation shape summaries  
- **`docs/milestones/M24/`** — `M24_plan.md`, `M24_toolcalls.md`  
- **`docs/serena.md`** — M24 row **In progress**; Phase V progress updated  

### Explicitly out of scope

- Changing callback invocation order  
- Modifying `ordered_callbacks`  
- Editing callback signatures  
- Modifying `Script` API  
- Modifying registry  
- Modifying runtime  
- Changing extension load behavior  
- Adding enforcement of parameter arity  
- Raising coverage threshold  

---

## 3. Locked design (preconditions)

- **Canonical IDs:** category strings (not raw `callbacks_*` keys); derive with `removeprefix("callbacks_")` (e.g. `callbacks_on_reload` → `on_reload`).  
- **`set(SUPPORTED_CALLBACKS) == set(derived)`** — exact match only (not subset / superset).  
- **Tests:** category names only; parameter shapes documented in markdown only — **no** signature introspection.  
- **`extension_api.py`:** constants + tuple only — **no** `script_callbacks` import.  

---

## 4. Invariants (must not change)

| Surface | Must remain stable |
|--------|-------------------|
| Extension loading | Unchanged |
| Callback invocation | Unchanged |
| Callback order | Unchanged |
| Registry API | Unchanged |
| Runtime modules | Unchanged |
| CI gates | Unchanged |
| Coverage | ≥ 40% |

**M24-specific:**

- `SUPPORTED_CALLBACKS` exactly matches `callback_map` keys (derived via prefix stripping).  
- No callback removed without version review.  
- No callback added without updating the declarative tuple **and** tests (they will fail until aligned).  

---

## 5. Implementation validation checklist (pre-merge)

1. **Canonical naming:** `SUPPORTED_CALLBACKS` uses category strings; `callbacks_on_reload` → `on_reload`.  
2. **Exact equality:** `set(SUPPORTED_CALLBACKS) == derived_categories` (not subset/superset).  
3. **Import-light:** `extension_api.py` does not import `script_callbacks`; no new import cycles.  
4. **No behavior drift:** `callback_map` structure unchanged; invocation sites unchanged; registration helpers unchanged.  
5. **CI posture:** ruff, eslint, smoke on PR; post-merge Quality ≥ 40%.  

---

## 6. Verification plan

### PR gates

- ruff  
- eslint  
- smoke  

### Post-merge

- Quality run  
- Coverage ≥ 40%  
- No pip-audit regression (program baseline)  

---

## 7. PR #43 — CI evidence (representative `pull_request` wave)

*Recorded when checks were green; re-verify on merge tip if needed.*

| Gate | Workflow run ID | Job links |
|------|-----------------|-----------|
| **Linter** (ruff + eslint) | `23395344432` | [workflow](https://github.com/m-cahill/serena/actions/runs/23395344432) |
| **Smoke Tests** | `23395344428` | [workflow](https://github.com/m-cahill/serena/actions/runs/23395344428) |

Parallel **push** wave (also green): Linter **`23395342959`**, Smoke **`23395342950`**.

---

## 8. Risk & rollback

**Risks:** missed key in tuple; typo in canonical name; drift between map and tuple.  
**Mitigation:** exact set equality test; derived-from-map logic in tests; small diff.  
**Rollback:** revert M24 PR; no runtime risk.  

---

## 9. Deliverables

- `modules/extension_api.py`  
- `docs/architecture/extension_api_contract_v1.md`  
- `test/quality/test_extension_api_contract.py`  
- Milestone docs under `docs/milestones/M24/`  
- Ledger **Completed**; tag **`v0.0.24-m24`** on squash merge commit **`2c8bc5b7`**  

---

## 10. Definition of done

- PR green  
- Post-merge Quality green  
- Coverage ≥ 40%  
- Ledger updated  
- Audit 5.0 / 5  
- Tag `v0.0.24-m24` on squash merge commit  

---

## 11. Why M24 is correct now

After M23, UI modularization and the registry are stable. The next likely drift surface is **extension callbacks without an explicit contract**. M24 formalizes that surface before Phase VI hardening.
