# M38 — Audit

**Milestone:** `processing.py` class and helper decomposition  
**Scope:** Phase IX — internal score-lift (structural decomposition)

---

## Conclusion

**Pass.** M38 was a **pure structural decomposition** milestone:

- **Import compatibility** through **`modules.processing`** **re-exports** was **preserved** (existing `from modules.processing import …` paths remain valid).
- **`ProcessingRunner`** boundaries and **runtime module** boundaries were **unchanged** in intent — only code was relocated into **`processing_types`**, **`processing_helpers`**, and **`processing_infotext`** with **`processing.py`** as orchestration.
- **Script hook call sites** remain in **`processing.py`** (`process_images` / `process_images_inner` / `postprocess` pipeline).
- **No behavior change** was intended; CI remained **truthful** and **unchanged in policy** (no gates relaxed, no deprecation scaffolding abuse).

**Pre-merge ledger note:** `M38_run1.md` §B **lagged** the final PR head due to doc-only commits advancing the tip after the last table refresh. **Merge approval** used the **later green `pull_request` tip** **`3654f8a30433a1ecd7de54811da6a454f23db458`** (Linter **`23700334490`**, Smoke **`23700334489`**), not the older SHA recorded in §B alone. The authoritative story is reconciled here and in **`M38_run1.md`** post-merge.

---

## CI

**Binding PR evidence (approval):** head **`3654f8a30433a1ecd7de54811da6a454f23db458`** — **`pull_request`** Linter **`23700334490`**, Smoke **`23700334489`** — **success**.

**Post-merge `main`:** merge commit **`17c21be669942518ab4683ba504c87c1ad58900e`** — **`push`** Linter **`23700723142`**, Quality **`23700723134`** — **success**; **217** tests passed; **TOTAL** coverage **48%** (as reported by Quality workflow).

---

## Risks / follow-ups

- **M39** may continue **legacy-surface narrowing** without broad globals cleanup — see **`docs/milestones/M39/M39_plan.md`**.
