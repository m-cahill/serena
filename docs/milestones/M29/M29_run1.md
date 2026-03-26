# M29 — Quality run analysis (run1)

**Date (UTC):** 2026-03-25  
**Repository:** `m-cahill/serena`  
**Branch under test:** `main`

## PRs in scope

| PR | Title (short) | Role |
|----|----------------|------|
| **#64** | M29: health & performance verification (runner metrics + CI snapshot) | Core M29 feature merge |
| **#65** | `requests` 2.33.0 — CVE-2026-25645 (pip-audit) | Unblock blocking audit gate |
| **#66–#67** | transformers pin experiments | Superseded by torch upgrade |
| **#68** | torch **2.2.2+cpu** / torchvision **0.17.2+cpu** | Align PyTorch with `transformers` 4.57 + `register_pytree_node` |
| **#69** | scikit-image **0.25.x** | NumPy 2 ABI (`dtype size changed`) |
| **#70** | `ui.py` — Gradio 6 without `gr.deprecation` | Server import |
| **#71** | `gradio_extensons` — Button `tooltip` shim | Gradio 6 Button kwargs |

**M29 squash merge commit (PR #64):** `f18b73f2` (on `main` history before follow-up fixes).

**Current `main` HEAD (at closeout doc authoring):** `cd56d7c6077e87e987477761c4e399d9b7564d80` (includes #71).

## Binding Quality run

**No passing “binding” Quality run on `main` was achieved during this closeout window.**

The most informative failing run after the dependency and shim chain:

| Field | Value |
|--------|--------|
| **Workflow** | Quality Tests |
| **Run ID** | `23569206049` |
| **URL** | `https://github.com/m-cahill/serena/actions/runs/23569206049` |
| **Outcome** | **failure** |
| **pip-audit** | **passed** (requests CVE + torch/transformers stack consistent) |
| **pytest / server** | **failed** — server startup proceeds further than earlier runs; failure during UI wiring |

### Failure excerpt (root cause)

After `pip-audit`, smoke, and server start, execution fails with **Gradio 6** API drift vs legacy WebUI patterns, for example:

```text
TypeError: EventListener._setup.<locals>.event_trigger() got an unexpected keyword argument '_js'
```

(see `modules/ui_toprow.py` — `.click(..., _js=...)`).

**Gradio 5.x** cannot be selected without violating the **Pillow ≥12** constraint (Gradio 5 requires `pillow<12`; resolver reports unsatisfiable with `pillow>=12`).

### Coverage % and test count

**Not available** from the failing run (pytest step did not complete successfully). Last known fully green reference on this repo remains **M27** Quality run **23513449859** (ledger); **not** claimed as M29 binding.

### Performance artifact

`performance_snapshot.txt` is generated **after** pytest in the workflow. Because pytest did not complete, the **performance-snapshot** artifact was **not** produced for run `23569206049` (workflow annotations: no file at expected path).

---

## Result

**Result:** **BLOCKED** — M29 instrumentation and docs merged; **Quality CI not green** on `main` at closeout time. **Root cause:** **Gradio 6** interaction with existing UI (`_js` on `.click()`, and related 5→6 API differences) **combined with** **Pillow ≥12** (cannot pin Gradio 5 without relaxing Pillow).

**Follow-up (recommended):** dedicated milestone for **Gradio 6 UI event / JS hook migration** (or approved architectural alternative), then re-run binding Quality and attach `performance_snapshot.txt`.

---

## M29.1 — Gradio 6 event kwargs (`_js` → `js`)

**Milestone docs:** `docs/milestones/M29.1/` (plan + toolcalls log).

**Code fix:** Gradio 6 event triggers accept **`js=`** instead of **`_js=`**. Affected `modules/` call sites were updated mechanically (same callback and JS strings; keyword rename only). This addresses the failure in run `23569206049` (`unexpected keyword argument '_js'`).

**Binding Quality run (post–M29.1 code):** merged via **#73** (`m29.1-gradio6-compat`). Subsequent **CI / Gradio** follow-ups: **#74–#78** (torch 2.4+cpu stack, tooltip shims, `Box` alias, `get_config` varargs, `Image` `source`/`tool` compat). Best attempt after **#78**:

| Field | Value |
|--------|--------|
| **Workflow** | Quality Tests |
| **Run ID** | `23573723272` |
| **URL** | `https://github.com/m-cahill/serena/actions/runs/23573723272` |
| **Outcome** | **failure** (pytest exit code 1) |
| **Tests** | **190 passed**, **9 failed** |
| **Coverage (TOTAL)** | **47%** (meets numeric ≥42% gate; pytest still failed overall) |
| **Server** | **starts** (7860 reachable) |
| **`performance_snapshot.txt`** | **Not** produced — workflow skips the write step when pytest fails |

**Example failures:** `test_img2img` → HTTP **422**; `sdapi/v1/cmd-flags`, `samplers`, `progress` → **500**; pydantic **`sampler_index`** validation; **`runtime_metrics`** contract test.

**Binding verdict:** **not PASS** — ledger / audit **stay at 4.0 / 5 pending binding CI** until a **fully green** Quality run **and** confirmed **`performance_snapshot.txt`** artifact.

---

## M29.1 — Binding CI recovery (branch `m29.1-binding-ci-recovery`)

**Diagnosis (pre-code, 2026-03-25):** targeted fixes below; no audit bump or `v0.0.29-m29` tag until a green Quality run with `performance_snapshot.txt`.

| Symptom | Likely root cause | Fix direction |
|--------|-------------------|---------------|
| Pydantic error on **`sampler_index=None`** in **`_text2imgapi_impl` / `_img2imgapi_impl`** | `populate.sampler_index = None` after **`_model_copy_with_update`**; field is **`str`**, not optional | Remove assignment; rely on defaults / valid string (no `None`) |
| **`ProcessingRequest` has no `runtime_metrics`** vs **`p.runtime_metrics = request.runtime_metrics`** in **`process_images`** | Runner already writes **`p.runtime_metrics`** in **`ProcessingRunner.run`** / **`_execute`** | Drop assignment from **`request`**; **`p`** is sole owner |
| **`GET /sdapi/v1/cmd-flags` → 500** | **`get_cmd_flags`** returns **`vars(shared.cmd_opts)`**, which includes **extra attributes** (e.g. post-parse fields) **not** in **`FlagsModel`** | Return only keys (and values) compatible with **`FlagsModel`** |
| **`GET /sdapi/v1/progress` → 500** (when job active path) | **`ProgressResponse`** missing **`current_task`**, but handler passes **`current_task=...`** → response validation failure | Add optional **`current_task`** to **`ProgressResponse`** |
| Smoke **`POST /sdapi/v1/img2img` → 422** with **`mask: null`** | Img2img API model declares **`mask`** as plain **`str`** while smoke sends JSON **`null`** | **`Optional[str]`** (or **`str \| None`**) for **`mask`** |
| **`test_txt2img_path_uses_runner`** touches real **`cond_stage_model`** / device | **`process_images`** still runs **`apply_token_merging`** etc. with minimal **`p`** | Mirror API contract test: mock **`apply_token_merging`** (and keep **`reload_model_weights`** mocked) |

### Round 2 — remaining failure cluster (2026-03-26)

**Ledger anchor (still the best documented failing Quality run):** `23573723272` — **190 passed / 9 failed**, **47%** coverage, **no** `performance_snapshot.txt` (pytest exit ≠ 0).

**Branch state:** `m29.1-binding-ci-recovery` already includes Round 1 fixes (no `sampler_index=None`, `p.runtime_metrics` ownership, `mask` optional, `ProgressResponse.current_task`, `get_cmd_flags` key filter, contract-test mocks).

**Hypothesis for CI still seeing 500s on `samplers` / `progress` / `cmd-flags` after Round 1:**

| Endpoint / area | Additional likely cause | Round 2 fix direction |
|-------------------|-------------------------|------------------------|
| **`GET /sdapi/v1/samplers`** | **`SamplerItem.options`** is **`dict[str, str]`** but runtime sampler metadata includes **booleans** (e.g. `second_order`, `uses_ensd`) → response validation **500** | Widen **`options`** to a JSON object type (**`dict[str, Any]`**) so the payload matches real data |
| **`GET /sdapi/v1/progress`** | **`textinfo`** / **`current_image`** declared as **`str`** with **`default=None`** → **`None`** at runtime fails Pydantic v2 | Use **`Optional[str]`** for nullable fields |
| **`GET /sdapi/v1/cmd-flags`** | Filtered values may still include **Path** / nested structures that do not match **`FlagsModel`** until JSON-coerced | **`jsonable_encoder`** before **`model_validate`** |

**Validation:** next green **Quality** run on `main` (or PR branch) is the binding proof; **M29 audit remains 4.0 / 5** until then.

### Round 3 — failure list + fix order (2026-03-26)

**Anchor run (unchanged):** `23573723272` — **190 passed / 9 failed**, **47%** coverage, **no** `performance_snapshot.txt`.

**Remaining failure classes (from that run; narrowed in prior rounds):**

| # | Area | Tests / symptom |
|---|------|-----------------|
| 1 | **img2img 422** | `test_img2img_simple_performed`, `test_img2img_sd_upscale_performed` (and same payload family) |
| 2 | **API 500** | `GET /sdapi/v1/cmd-flags`, `GET /sdapi/v1/samplers`, `GET /sdapi/v1/progress` (`test_get_api_endpoint` / extended API) |
| 3 | **Pydantic / API path** | `sampler_index` / request validation (addressed in prior commits; re-verify) |
| 4 | **Runner seam** | `test_api_txt2img_uses_runner`, `test_txt2img_path_uses_runner` (avoid real pipeline / `cond_stage_model`) |
| 5 | **`runtime_metrics`** | Ownership on **`p`** only (already fixed; re-verify) |

**Round 3 fix order (this pass):**

1. **img2img 422:** Smoke sends **`"inpainting_mask_invert": false`**; generated API field from the dataclass is **`Optional[int]`**, so Pydantic v2 rejects **`bool`**. Override **`inpainting_mask_invert`** to **`int | bool`** (minimal widen) in **`StableDiffusionImg2ImgProcessingAPI`** additional fields (last definition wins).
2. **API 500s:** Rely on Round 2 schema fixes (**`SamplerItem.options`**, **`ProgressResponse`** nullables, **`get_cmd_flags`** encode + validate); re-verify in CI.
3. **Seam tests:** Patch **`ProcessingRunner.execute`** to return a **`Processed`** stub instead of only mocking **`process_images_inner`**, so the runner’s inner **`from modules.processing import process_images_inner`** cannot bypass the mock and touch **`sd_model`**.

### PR validation — recovery branch → `main` (2026-03-26)

| Field | Value |
|--------|--------|
| **PR** | https://github.com/m-cahill/serena/pull/79 |
| **Title** | M29.1: binding CI recovery for Gradio 6 / API / runner compatibility |
| **Merge** | **Do not merge** without approval; binding **Quality** on **`main`** + **`performance_snapshot.txt`** still required for M29 closeout |

**First PR checks snapshot** (immediately after PR open; Actions runs e.g. `23574993304` / `23574993308`):

| Check | Result | Notes |
|--------|--------|--------|
| **eslint** | **pass** | — |
| **ruff** | **fail** | Seam test duplicate/unused `Processed` import; plus repo-wide Ruff items addressed in follow-up commit |
| **smoke** | **fail** | Await re-run after **`4611740b`** (Ruff + CI hygiene); capture logs if still red |

**Follow-up on branch** (commit **`4611740b`**): Ruff clean — `test_txt2img_runner_contract` import fix; `write_performance_snapshot.py` import order; remove unused `pytest` in `test_m27_util_errors_coverage.py`; `pyproject.toml` per-file **`F811`** ignore for `modules/processing.py` (dataclass/property pattern); Ruff **exclude** `modules/ui_components.pyi` (local stub layout). **Re-verify** PR **ruff** + **smoke** on latest push.

**Second PR checks snapshot** (after push **`4611740b`** / docs **`af78464b`**; Actions e.g. **`23576902822`** lint, **`23576902847`** smoke):

| Check | Result | Notes |
|--------|--------|--------|
| **eslint** | **pass** | — |
| **ruff** | **pass** | Confirms hygiene commit |
| **smoke** | **fail** | **`wait-for-it`** timed out on **`127.0.0.1:7860`** (20s) — test server did not accept connections in time. See workflow **`output.txt`** artifact on run **`23576902847`** for launch traceback / logs (not an HTTP 422/500 from pytest in this failure mode). |

**Next:** Inspect **`output.txt`** from the failing smoke run; if startup is flaky, re-run workflow; if reproducible, fix **launch / server bind** path (outside HTTP handler fixes above).

### Round 4 — smoke bind / startup (2026-03-26)

**Failing smoke run(s):** **`23576902847`** (PR **#79** checks after **`4611740b`**; companion lint run **`23576902822`**).

**Failure mode:** pytest never reached HTTP API assertions — **`wait-for-it`** timed out on **`127.0.0.1:7860`** because the Web UI process **crashed during `ui.create_ui()`** before Gradio listened. This is **not** the earlier **`23573723272`** cluster (422 / 500 on live server).

**First tracebacks in smoke `output/output.txt` (authoritative):**

1. **Background model load** (thread `initialize.load_model` / empty checkpoint **`test/test_files/empty.pt`**):

```text
AttributeError: 'LatentDiffusion' object has no attribute 'cond_stage_model'
  ...
  File ".../modules/sd_models.py", line 397, in set_model_type
    elif hasattr(model.cond_stage_model, 'model'):
```

2. **Process-fatal UI build** (main thread — prevents bind):

```text
TypeError: Image.__init__() got an unexpected keyword argument 'source'
  ...
  File ".../modules/ui_img2img_tab.py", line 69, in create_img2img_tab
    init_img = gr.Image(..., source="upload", ... tool="editor", ...)
  File ".../gradio/component_meta.py", line 194, in wrapper
    return fn(self, **kwargs)
```

**Classification:** **Gradio 6** constructor drift — legacy **`source=`** / sketch kwargs on **`gr.Image`** (CI uses **`gradio==6.10.0`** per `requirements-ci.txt`). Secondary: **`set_model_type`** must not assume **`cond_stage_model`** exists for partially constructed / minimal checkpoint paths.

**Fix direction (this round):** use **`sources=`** on **`gr.Image`** at WebUI call sites (and drop unsupported **`tool` / `brush_color`** on `Image` where present); guard **`set_model_type`** with **`getattr(model, "cond_stage_model", None)`** before probing **`.model`**.

**Checklist:** `[x]` traceback extracted; `[x]` documented here; startup/bind fixes applied on branch; re-run PR **#79** checks; **do not** merge / audit bump / tag until policy gates (green Quality on `main` + **`performance_snapshot.txt`**).

**Post-push smoke (`23578226657`, after `sources=` / `set_model_type` commit):** `output.txt` shows the **first process-fatal** error is **`TypeError: EventListenerMethod.__call__() got an unexpected keyword argument 'js'`** from **`modules/ui_toprow.py`** (Interrupt **`.click(..., js=...)`**). The img2img **`source=`** failure did not appear in that run (Image fixes are still kept). Background thread may still log **`load_state_dict`** on **`empty.pt`** after **`set_model_type`**; treat as secondary until main thread reaches **`create_img2img_tab`**.

**Round 4b fix:** remove **`js=`** from Interrupt and clear-prompt **`.click`** in **`ui_toprow`** (no dependency change; JS confirm/placeholder hooks deferred).

**Round 4c fix:** Smoke still failed on the next **`js=`** site (**`ui_prompt_styles`** → **`style delete`**). Rather than Whac‑A‑Mole across **`modules/`**, add **`modules/gradio_event_compat.py`** and import it **before** **`import gradio`** in **`initialize.imports()`**, wrapping each **`gradio.events.Events.*.listener`** so **`js` / `_js`** are stripped (client hooks no‑op; UI construction unblocked). *Note:* patching **`EventListener._setup` alone is fragile across Gradio builds (attribute may live only on subclasses); listener wrap runs before component meta instantiates triggers.*
