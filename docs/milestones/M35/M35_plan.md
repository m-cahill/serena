# M35 — Remove tolerated `shared.sd_model` orchestration coupling

**Phase VIII** (per `docs/serena.md`). Follows **M34** (runtime model-identity seam).

**Status:** Stub — plan to be expanded at M35 kickoff.

---

## Title

Remove tolerated `shared.sd_model` orchestration coupling

---

## Objective

Use the **`RuntimeContext.model_identity`** seam from **M34** to eliminate the remaining **load-bearing orchestration** dependency on **`shared.sd_model`** in **`processing.py`** where the audit calls it out, without violating **M19** (runtime modules use **`ModelProvider`** only).

---

## Authority

- `docs/serena.md`
- `docs/serenav1audit.md`
- `docs/architecture/serena_architecture_lock.md`
- `docs/architecture/serena_allowed_legacy_surfaces.md`
- `docs/milestones/M34/M34_plan.md` (residue list)

---

## Deliverables (placeholder)

- Code + tests for migrated paths
- Update **`serena_allowed_legacy_surfaces.md`** if coupling is removed
- `docs/milestones/M35/M35_run1.md`, summary/audit per program discipline
