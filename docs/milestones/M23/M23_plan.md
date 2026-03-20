# M23 Plan — Settings & Extensions Modularization

**Milestone:** M23  
**Phase:** Phase V — UI & Extension Stabilization  
**Branch:** *(TBD)*  
**Baseline:** `main` @ post-M22 merge (`99b5f0c4` / tag `v0.0.22-m22`)  
**Status:** Stub — not started

---

## 1. Intent

Modularize **Settings** and **Extensions** top-level tab construction behind the existing `ui_tab_registry` seam (per Phase V map: “Settings/extensions modularization”). Preserve M21/M22 ordering, `shared.tab_names` pre-sort behavior, `sorted_interfaces` / `hidden_tabs`, and extension callback semantics unless explicitly approved.

---

## 2. Deliverables (provisional)

- Plan refinement after kickoff; contract tests as appropriate; ledger row; evidence at closeout.

---

## 3. Definition of done

- PR green; post-merge Quality green; ledger updated; annotated milestone tag per program rules.
