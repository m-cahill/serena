# M35 — Remove tolerated `processing.py` ↔ `shared.sd_model` orchestration coupling

**Phase VIII** · **Status:** In progress  
**Branch:** `m35-remove-shared-sd-model-orchestration`  
**Depends on:** M34 (`RuntimeContext.model_identity`, binding Quality on `main`)

---

## Intent / target

Eliminate **direct** `shared.sd_model` reads on the **supported orchestration path** in `modules/processing.py` by routing through **`p.model_provider`** via **`_orchestration_model(p)`**, using the M34 identity seam for **`RuntimeContext`** / **`p.sd_model_name`** / **`p.sd_model_hash`** as before.

**Non-goal:** A repo-wide purge of `shared.opts`, `shared.state`, or other globals.

---

## Scope boundaries

**In scope**

- Inventory and replace load-bearing **`shared.sd_model`** touchpoints in `processing.py` (or document as compatibility-only).
- One **`processing.py`** helper: **`_orchestration_model(p)`** → **`model_provider.get_model(p)`** when set; else **`shared.sd_model`**.
- **`StableDiffusionProcessing.sd_model`**: remain a **compatibility alias** unless inspection proves zero external risk; document that it is **not** the orchestration authority.
- Regression tests (extend `test/quality/test_runtime_mock.py` where readable).
- This file, **`M35_toolcalls.md`**, **`M35_run1.md`**, updates to **`serena_allowed_legacy_surfaces.md`**.

**Out of scope**

- Broad `shared.*` cleanup, runtime module redesign, hook relocation, UI/API changes, CI threshold changes, M36+.

---

## Invariants

- **`ProcessingRunner`** remains the execution boundary; **`prepare`** attaches **`model_provider`** before **`process_images_inner`**.
- **`processing.py`** keeps script hook call sites.
- **`processing_runtime`**, **`sampler_runtime`**, **`decode_runtime`**: model access only via **`ModelProvider`** (unchanged).
- No intentional user-visible behavior drift; no CI weakening.

---

## Verification plan

- **Static:** No load-bearing **`shared.sd_model`** in `processing.py` except compatibility property + **`_orchestration_model`** fallback (documented).
- **Tests:** Provider-backed orchestration identity when **`shared.sd_model`** differs; existing M34 identity / hook-order tests still pass.
- **CI:** PR Linter + Smoke; post-merge Quality on `main` as binding proof (record in **`M35_run1.md`**).

---

## Implementation steps (completed in this branch)

1. Add **`_orchestration_model(p)`** in `modules/processing.py`.
2. Replace direct **`shared.sd_model`** uses (process entry, cond cache, HR lowvram branch, img2img init, **`edit_image_conditioning`**) with **`_orchestration_model(self)`** / **`_orchestration_model(p)`**.
3. Document **`sd_model`** property as compatibility-only.
4. Add **`test_orchestration_identity_ignores_mismatched_shared_sd_model`**.
5. Update **`serena_allowed_legacy_surfaces.md`** and milestone logs.

---

## Risk & rollback

| Risk | Mitigation |
|------|------------|
| Extension assumes **`p.sd_model` === global** | Property unchanged; only internal orchestration paths use **`_orchestration_model`**. |
| Call site without **`model_provider`** | Fallback to **`shared.sd_model`** preserves prior behavior. |

**Rollback:** Revert `processing.py` / test / doc commits; keep helper only if behavior-neutral.

---

## Deliverables

- [x] Code + tests
- [x] **`serena_allowed_legacy_surfaces.md`** update
- [ ] **`M35_run1.md`** (CI IDs after PR)
- [ ] **`M35_summary.md`**, **`M35_audit.md`** (closeout)
- [ ] **`docs/serena.md`** milestone row (closeout)
- [ ] M36 stubs (post-closeout)
