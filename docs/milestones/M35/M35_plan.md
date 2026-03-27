# M35 — Remove tolerated `processing.py` ↔ `shared.sd_model` orchestration coupling

**Phase VIII** (per `docs/serena.md`). Follows **M34** (runtime model-identity seam on `RuntimeContext`).

**Status:** Planned — kickoff when M35 execution starts.

---

## Title

Remove tolerated **`processing.py` ↔ `shared.sd_model`** **orchestration** coupling (narrow scope)

---

## Objective

Use the **`RuntimeContext.model_identity`** seam from **M34** and existing **M19 `ModelProvider`** discipline to **reduce load-bearing orchestration** that still routes through **`shared.sd_model`** in **`processing.py`** where the audit and **`serena_allowed_legacy_surfaces.md`** call it out.

**In scope:** The **orchestration seam** between **`process_images_inner`** (and closely related preparation) and **model identity / model acquisition** — moving reads and decisions toward **`RuntimeContext`** + **`model_provider`** where the architecture lock allows.

**Out of scope for M35:** Broad **global-state cleanup** across the repo, unrelated refactors of **`shared.opts`**, **`shared.state`**, or “fix all globals” sweeps. Those belong to later milestones or explicit follow-ups, not M35.

---

## Authority

- `docs/serena.md`
- `docs/serenav1audit.md`
- `docs/architecture/serena_architecture_lock.md`
- `docs/architecture/serena_allowed_legacy_surfaces.md`
- `docs/milestones/M34/M34_plan.md` (residue / deferral notes)

---

## Deliverables (at kickoff)

- Code + tests for migrated orchestration paths
- Update **`serena_allowed_legacy_surfaces.md`** if coupling is reduced or reclassified
- `docs/milestones/M35/M35_run1.md`, summary, audit per program discipline
