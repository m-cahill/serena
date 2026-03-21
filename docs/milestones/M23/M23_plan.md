# M23 Plan — Settings & Extensions modularization

**Milestone:** M23  
**Phase:** Phase V — UI & Extension Stabilization  
**Branch:** `m23-settings-extensions-modularization`  
**Baseline:** `main` @ M22 closeout (`99b5f0c4`)  
**Status:** Completed (2026-03-21)

---

## 1. Intent

Relocate Settings and Extensions top-level tab assembly from `modules/ui.py` into `modules/ui_settings_tab.py` and `modules/ui_extensions_tab.py`, returning `TabBuildResult` (unchanged dataclass). **Pure relocation:** no registry API change, no `UiSettings` lifecycle change, no extension behavior change.

---

## 2. Locked design (preconditions)

- **`create_settings_tab(settings, loadsave, dummy_component)`** — calls `settings.create_ui(loadsave, dummy_component)`; returns `TabBuildResult(interface=settings.interface, label="Settings", ifid="settings")`. `UiSettings()` and `register_settings()` remain in `create_ui()` before other tabs.
- **`create_extensions_tab()`** — lazy-import `ui_extensions`, `return TabBuildResult(ui_extensions.create_ui(), "Extensions", "extensions")`.
- **No** `TabBuildResult` extension; **no** new dataclasses.
- **Loadsave guard** `ifid not in ["extensions", "settings"]` stays in `modules/ui.py`.

---

## 3. Deliverables

- `modules/ui_settings_tab.py`
- `modules/ui_extensions_tab.py`
- `modules/ui.py` — wire builders; drop unused `ui_extensions` import if only used for tab.
- `test/quality/test_ui_settings_extensions_modularization.py`
- `docs/serena.md` — M23 ledger row (in progress → completed at closeout)

---

## 4. Verification

- PR: ruff, eslint, smoke  
- Post-merge: Quality, coverage ≥ 40%

---

## 5. Definition of done

- PR green; post-merge Quality green; ledger + tag `v0.0.23-m23` on squash merge commit `64c232c3` (closeout complete).
