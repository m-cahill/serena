# M31 — Summary: Architecture lock

**Status:** Completed (documentation-only — **not** a runtime-change milestone)  
**Audit score:** 5.0 / 5 (see `M31_audit.md`)  
**Merge:** **[PR #83](https://github.com/m-cahill/serena/pull/83)** squash-merged to **`main`** → **`09f1d785677df7400ed21d45ebb7bf3c96c7c979`** (merged **2026-03-26T22:49:34Z**).  
**Pre-merge head:** **`ffb97c144cc2d3a083fb4b25cdb258d49274a959`** on branch **`m31-architecture-lock`**.

---

## What shipped

1. **`docs/architecture/serena_architecture_lock.md`** — Authority order, locked architecture summary, boundaries table, change-control rules, proof references.
2. **`docs/architecture/serena_allowed_legacy_surfaces.md`** — Tolerated `shared.sd_model` / `processing.py` glue vs M19 runtime modules; anti–drive-by-refactor guidance.
3. **`docs/serena.md`** — Post-M31 source hierarchy; Phase VII progress; M31 ledger row (completed with PR/merge in `M31_run1.md` / ledger).
4. **`docs/architecture/serena_evidence_bundle.md`**, **`serena_evidence_matrix.md`** — Cross-references for M31.
5. **`docs/milestones/M31/M31_plan.md`**, **`M31_toolcalls.md`**, **`M31_run1.md`**, **`M31_audit.md`** (this milestone folder).
6. **`docs/milestones/M32/*`** — Minimal stubs for evidence/audit closure.

---

## What did not ship (by design)

- No application code, workflow YAML, or dependency file changes.
- No CI policy or threshold changes.

---

## Verification

- **Content:** Consistent with existing evidence docs and ledger; lock distinguishes **locked architecture** from **allowed legacy** surfaces.
- **Diff:** M31 merge **#83** contained **only** `docs/**` paths (see `M31_run1.md` §3).

---

## Evidence and provenance

- **PR #83** Linter + Smoke: **`M31_run1.md` §6** — **hygiene only**, not binding architecture proof.
- **Post-merge** Linter + Quality on **`09f1d785`**: **`M31_run1.md` §7** — **optional** routine CI signal after docs merge.

---

## Next

**M32 — Evidence/audit closure** per `docs/serena.md` (stubs only; no speculative scope).
