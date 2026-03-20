# M21 Plan — UI Tab Registry

**Milestone:** M21 — UI Tab Registry  
**Phase:** Phase V — UI & Extension Stabilization  
**Branch:** `m21-ui-tab-registry`  
**Status:** Canonical plan (locked 2026-03-20)

---

## 1. Intent / Target

Introduce a **top-level tab registry** so `modules/ui.py` is not the sole owner of tab-list wiring, without changing UI behavior, extension hooks, or nested `gr.Tab` layout.

**In scope:** The `interfaces` pipeline in `create_ui()` only:

- Six core tabs (fixed order and labels)
- `script_callbacks.ui_tabs_callback()` results
- Settings and Extensions append order
- `shared.tab_names` pre-sort sequence
- Existing `sorted_interfaces` / `hidden_tabs` behavior (unchanged logic)

**Out of scope:** Nested txt2img/img2img tabs, moving tab implementations to new modules, runtime/API changes.

---

## 2. TabSpec Design (M21)

Frozen dataclass holding **already constructed** `gr.Blocks` (or equivalent) references:

- `interface`, `label`, `ifid`, `source: Literal["core", "extension"]`
- Extension rows from `ui_tabs_callback()` map to `source="extension"`; Settings/Extensions use `source="core"`.

No lazy builders in M21 (deferred to M22+).

---

## 3. Invariants

| Invariant | Verification |
|-----------|--------------|
| Pre-sort `shared.tab_names` = core → extension callbacks → Settings → Extensions | Quality test Contract A |
| Sorting only via `opts.ui_tab_order` and `hidden_tabs` | No logic change; code review |
| `loadsave.add_block` / exclusions for settings & extensions | Preserved in `ui.py` loop |
| Extension callback signatures and merge position | Quality merge test |

---

## 4. Verification

- **PR:** Linter + Smoke green  
- **Post-merge:** Quality green, coverage ≥ 40%  
- **Tests:** `test/quality/test_ui_tab_registry.py` — core order, merge position, `build_top_level_interface_tuples` + `core_tab_specs` wiring  

---

## 5. Closeout

- Tag after merge + Quality on `main`: `v0.0.21-m21`
