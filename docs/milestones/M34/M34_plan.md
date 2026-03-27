# M34 — Runtime context model-identity seam

**Phase VIII** (per `docs/serena.md`). First milestone of post-v1 **5/5 recovery** (see `docs/serenav1audit.md`).

**Status:** Implementation complete on branch **`m34-runtime-context-model-identity`** (pending PR / CI).

---

## Title

Runtime context model-identity seam

---

## Objective

Introduce the **smallest safe, runtime-owned seam** so **model identity** (checkpoint display name and hash used for metadata/orchestration) is explicit on **`RuntimeContext`**, without removing the remaining tolerated **`processing.py`** ↔ **`shared.sd_model`** coupling. **M35** will migrate reads off the global where safe.

---

## `shared.sd_model` read points in `modules/processing.py` (classification)

| Location | Kind | Classification | M34 action |
|----------|------|----------------|------------|
| `StableDiffusionProcessing.sd_model` property getter (`return shared.sd_model`) | Ambient accessor | **Orchestration / global binding** — all `p.sd_model` use resolves here | **Deferred M35** |
| `edit_image_conditioning` — `shared.sd_model.encode_first_stage` | Direct call | **Load-bearing runtime access** | **Deferred M35** |
| `cached_params` — `shared.sd_model.sd_checkpoint_info` | Cache key tuple | **Identity / metadata** (invalidation) | **Deferred M35** (object identity semantics; do not swap for name/hash alone without proof) |
| `get_conds_with_caching` docstring / `function(shared.sd_model, …)` | Conditioning API | **Load-bearing runtime access** | **Deferred M35** |
| `process_images_inner` — `m = shared.sd_model`; `fix_dimensions` | Dimension fix | **Orchestration** | **Deferred M35** |
| `process_images_inner` — `model_identity_from_model(m)`; `p.sd_model_*` | Name/hash | **Identity / metadata** | **Done M34** — single source via `ModelIdentity` + `p.runtime_context.model_identity` |
| `process_images_inner` — `RuntimeContext(model=m, …)` | Model reference | Same object as before | **Unchanged** (reference, not identity fields) |
| `Img2Img` / inner paths — `lowvram` + `shared.sd_model.sd_checkpoint_info` | HR / low VRAM | **Orchestration** | **Deferred M35** |
| `Img2Img` init — `shared.sd_model.cond_stage_key` | Mode flag | **Orchestration** | **Deferred M35** |

**Note:** Many other uses are `self.sd_model`, which still resolves through the property to **`shared.sd_model`** — counted under the property row for migration purposes.

---

## Implementation (M34)

### `ModelIdentity` + `RuntimeContext`

- **`modules/runtime_context.py`**
  - **`ModelIdentity`** (frozen dataclass): `name_for_extra`, `model_hash` — mirrors the fields previously read separately from **`shared.sd_model`** for **`p.sd_model_name`** / **`p.sd_model_hash`**.
  - **`model_identity_from_model(model)`** — derives identity from the active model object (same source as pre-M34).
  - **`RuntimeContext`** extended with **`model_identity: ModelIdentity`** (after **`model`**).

### `process_images_inner`

- Bind **`m = shared.sd_model`** once for the early block.
- After **`fix_dimensions`**, build **`model_identity = model_identity_from_model(m)`**, assign **`p.sd_model_name`** / **`p.sd_model_hash`** from **`model_identity`** (behavior-preserving).
- Pass **`model_identity`** into **`RuntimeContext`**; **`model=`** remains **`m`**.

### Non-goals (confirmed)

- No removal of other **`shared.sd_model`** reads.
- No **`cached_params`** migration (cache key uses **`sd_checkpoint_info`** object identity).
- No hook moves, no API/UI changes, no CI threshold changes.

---

## Verification

- **Unit-style:** `model_identity_from_model` on **`FakeModel`**.
- **Integration:** **`test/quality/test_runtime_mock.py`** — full runner pipeline asserts **`p.runtime_context.model_identity`** matches **`FakeModel`** and **`p.sd_model_*`**; **`scripts.process`** hook sees **`runtime_context.model_identity`** before inner loop.

---

## Deliverables

| Artifact | Status |
|----------|--------|
| Code: `runtime_context.py`, `processing.py` | Done |
| Tests: `test_runtime_mock.py` | Done |
| `docs/architecture/serena_allowed_legacy_surfaces.md` | M34 note |
| `docs/milestones/M34/M34_toolcalls.md` | Updated |
| `docs/milestones/M34/M34_run1.md` | CI record after PR |
| `docs/milestones/M35/*` stubs | Seeded |
| `docs/serena.md` | Ledger / Phase VIII progress |

---

## Risk / rollback

**Risk:** Low — additive fields; **`p.sd_model_*`** assignment path is equivalent to previous attribute reads.

**Rollback:** Revert commit; restore **`RuntimeContext`** to five fields without **`model_identity`**.
