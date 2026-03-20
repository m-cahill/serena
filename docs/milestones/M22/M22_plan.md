# M22 Plan — txt2img / img2img Tab Modularization

**Milestone:** M22  
**Phase:** Phase V — UI & Extension Stabilization  
**Branch:** `m22-tab-modularization`  
**Baseline:** `main` @ `081de7e7` (M21 tag anchor)  
**Status:** Completed (2026-03-20)

---

## 1. Intent

Mechanically relocate txt2img and img2img top-level `gr.Blocks` bodies from `modules/ui.py` into dedicated modules. **No** change to labels, `ifid`, `elem_id`, nested tabs, callbacks, `shared.tab_names`, registry signatures, or M21 tests.

---

## 2. Locked design

- **`TabBuildResult`** (`interface`, `label`, `ifid`, `dummy_component=None`, `txt2img_preview_params=None`, `image_cfg_scale=None`): txt2img sets `dummy_component` and `txt2img_preview_params` (train tab wiring); img2img sets `image_cfg_scale` (settings visibility callback on main demo); img2img `dummy_component` field is `None`.
- **`create_ui()`** sets `modules.ui_img2img_tab.img2img_dummy_component = txt2img.dummy_component` before `create_img2img_tab()` so img2img wiring stays identical (img2img uses the same Gradio label as today).
- **Registry:** `core_tab_specs` / `build_top_level_interface_tuples` **unchanged**; `create_ui()` passes built interfaces as today.
- **Builders:** no parameters; lazy `import modules.ui as ui` inside builders to avoid import cycles with helpers/constants on `ui`.

---

## 3. Deliverables

- `modules/ui_tab_build_result.py` — `TabBuildResult`
- `modules/ui_txt2img_tab.py` — `create_txt2img_tab()`
- `modules/ui_img2img_tab.py` — `create_img2img_tab()`, module attr for dummy bridge
- `modules/ui.py` — orchestration only for these tabs; removed inlined bodies
- `test/quality/test_ui_tab_modularization.py` — contracts per ledger
- `docs/serena.md` — M22 row (after merge / per program timing)

---

## 4. Verification

- PR: ruff, eslint, smoke  
- Post-merge: Quality, coverage ≥ 40%  
- M21 tests: unchanged, still pass  

---

## 5. Definition of done

- PR green; post-merge Quality green; ledger updated; annotated tag `v0.0.22-m22` on merge commit `99b5f0c43806c3b521cbb6d8ef561fa87ef2c75d` (closeout).
