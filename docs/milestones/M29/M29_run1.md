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

**Round 4c fix:** Smoke failed on successive **`js=`** call sites (**`ui_prompt_styles`**, etc.). **`gradio_event_compat`** (early **`EventListener.__init__`** patch) was abandoned: Gradio 6 **`Component`** cooperatively calls **`EventListener.__init__(self)`**, and CI layouts differ on **`Events` / `_setup`**. **Working approach:** strip **`js` / `_js`** in **`gradio.blocks.BlocksConfig.set_event_trigger`** (see **`modules/gradio_extensons.py`**), loaded with **`gradio_extensons`** after **`import gradio`** in **`initialize.imports()`**.

### Round 5 — dual-Gradio compatibility (2026-03-26)

**Stacks:** **Smoke** CI installs the legacy pin set (**`requirements_versions.txt`**, e.g. **Gradio 3.41.2** / older Pillow). **Quality** CI uses the locked manifest (**`requirements-ci.txt`**, **Gradio 6.x** / newer Pillow). They are intentionally different until dependency alignment is a separate milestone.

**Bind blocker under smoke:** **`TypeError: EventListenerMethod.__call__() got an unexpected keyword argument 'js'`** — Gradio 3 expects **`_js=`** on event bindings; M29.1 migrated call sites to **`js=`** for Gradio 6. Stripping all client **`js`** (Round 4c) avoided the crash but removed essential UI behavior (interrupt placeholder, clear-prompt confirm, style dialogs).

**Fix direction (this round):** centralized **`js` ↔ `_js`** normalization in **`modules/gradio_extensons.py`** (**`EventListenerMethod.__call__`** + **`BlocksConfig.set_event_trigger`**) so the repo keeps a **single** convention (**`js=`**) while smoke translates to **`_js`** at runtime. **`gr.Image`**: branch **`sources=`** vs **`source=`** by major version (G6-style vs G3). **No** workflow or requirements file changes in this pass; **no** broad callsite **`js`** removal as the primary strategy.

### Round 7 — Pydantic v1/v2 dual-stack compatibility (2026-03-26)

**Failing smoke run(s):** **`23580424792`** (PR **#79** checks after Round 5 commit **`f661bc8e`**).

**Confirmed:** Round 5 **`js ↔ _js`** shim **IS reached** (`output.txt` line 152 shows **`_elm_compat`** in the call stack). The event kwarg translation works.

**New bind blocker — cascade failure from Pydantic v1 metaclass conflict:**

1. **`modules/api/models.py:115`** — M29.1 migrated `generate_model()` to use **`ConfigDict(populate_by_name=True, ...)`** as `__config__=` param to `create_model`. Under smoke's **Pydantic 1.10.26**, `ConfigDict` is a `TypedDict` (not a config class) → **`TypeError: metaclass conflict`** on every `create_model` call.
2. This crashes the **import of `modules.api.models`** — which is done inside **`create_script_ui_inner()`** for every script → **9 scripts** fail UI creation (non-fatal, caught by try/except).
3. The **Sampler** script's `steps` Slider is never created → `steps = None`.
4. **`ui_txt2img_tab.py:245`** passes `steps` (= `None`) as input to **`.change()`** → **`AttributeError: 'NoneType' object has no attribute '_id'`** — **process-fatal**, server never binds.

**Also at risk:** **`api.py:742-744`** uses **`model_fields`** and **`model_validate`** (Pydantic v2-only); under v1 these would be **`__fields__`** and **`parse_obj`**. Fixed proactively.

**Fix direction:** version-gate `generate_model()` — Pydantic ≥ 2 uses `ConfigDict`; Pydantic 1 uses the original `__config__` mutation style. Same pattern for `get_cmd_flags` in `api.py`.

#### Round 7 — implementation (completed)

**Gradio:** **`js ↔ _js`** shim confirmed active in smoke artifacts; event-kwarg drift is not the remaining blocker.

**Pydantic:** Primary startup/bind blocker was **dual-stack incompatibility** — Quality uses **Pydantic v2**, smoke legacy stack uses **Pydantic 1.10.26**.

**Files changed:** **`modules/api/models.py`** (`_PYDANTIC_V2` from `pydantic.VERSION`; v2 path: `ConfigDict` + `create_model(..., __config__=...)`; v1 path: `create_model(**fields)` then `__config__.allow_population_by_field_name` / `allow_mutation`). **`modules/api/api.py`** — **`get_cmd_flags`**: `model_fields` / `model_validate` when present, else **`__fields__`** / **`parse_obj`**.

**PR #79 verification (post-fix):** eslint **pass**, ruff **pass**, smoke **pass** (e.g. workflow runs **`23582809675`**, **`23582812333`**). Server binds; smoke reaches pytest. **No merge** in this documentation-only follow-up unless policy gates are met separately.

### Post-merge Quality — PR **#79** → `main` (2026-03-26)

**Merge:** PR **#79** merged (**squash**), merge commit **`603b1dc026ee96e5e00c6aa0eda02f1306d12476`** (merged **`2026-03-26T20:17:11Z`**).

**First Quality run on `main` after merge:** **`23615984557`** — https://github.com/m-cahill/serena/actions/runs/23615984557

| Item | Value |
|------|--------|
| **Overall** | **failure** |
| **Failed step** | **Run quality tests** (pytest exit **1**) |
| **pip-audit (M28 policy)** | **pass** — dependency vulnerability scan step completed before pytest |
| **Tests** | **196 passed**, **3 failed**, ~**75s** |
| **Coverage (pytest `--cov`)** | **~48%** total line coverage (term report in log) |
| **`performance_snapshot.txt`** | **Not produced** — **Write performance snapshot (M29)** skipped because pytest failed; upload step reported *No files were found with the provided path: performance_snapshot.txt* |

**Failures (pytest short summary):**

1. **`test/smoke/test_utils.py::test_get_api_url[sdapi/v1/cmd-flags]`** — `500` vs `200`
2. **`test/quality/test_api_extended.py::test_get_api_endpoint[sdapi/v1/cmd-flags]`** — same
3. **`test/quality/test_txt2img_runner_contract.py::test_txt2img_path_uses_runner`** — `AssertionError: assert 'runner_execute' in []`

**First fatal API error (from `output` artifact, `output.txt`):** `GET /sdapi/v1/cmd-flags` returns **500** with **`ValidationError`**: **27 validation errors for `Flags`** — multiple fields (**`loglevel`**, **`models_dir`**, **`ckpt_dir`**, …) — **Input should be a valid string** with **`input_value=None`**. Under **Pydantic v2**, **`model_validate(...)`** rejects **`None`** for fields typed as **`str`** when those keys are present in the payload built from **`vars(shared.cmd_opts)`**.

**Classification:**

- **Continuation (with new symptom)** of the **M29.1 `get_cmd_flags` / FlagsModel** thread: Round 7 switched the v2 path to **`model_validate`**, which is **stricter** than the prior **`parse_obj`** / omitted-key behavior for optional CLI strings that are **`None`** at runtime.
- **`test_txt2img_path_uses_runner`** looks **separate** (expects **`runner_execute`** in captured log lines); treat as a **second** failing assertion until triaged — may or may not share root cause with cmd-flags.

**M29 closeout:** **blocked** — do **not** raise audit to **5.0 / 5**, do **not** tag **`v0.0.29-m29`**, do **not** mark M29 completed in the ledger until a **green** Quality run on **`main`** produces **`performance_snapshot.txt`**.

---

## M29.2 — post-merge Quality recovery (after run `23615984557`)

**Canonical detail:** `docs/milestones/M29.2/M29.2_toolcalls.md`

### Diagnosis (no code — evidence from `23615984557`)

**Failing tests:**

1. `test/smoke/test_utils.py::test_get_api_url[sdapi/v1/cmd-flags]` — `500` vs `200`
2. `test/quality/test_api_extended.py::test_get_api_endpoint[sdapi/v1/cmd-flags]` — same
3. `test/quality/test_txt2img_runner_contract.py::test_txt2img_path_uses_runner` — `assert 'runner_execute' in []`

**Traceback snippets:**

```text
AssertionError: assert 500 == 200
 +  where 500 = <Response [500]>.status_code
# ... GET http://127.0.0.1:7860/sdapi/v1/cmd-flags
```

```text
pydantic_core._pydantic_core.ValidationError: 27 validation errors for Flags
loglevel
  Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
# ... (models_dir, ckpt_dir, vae_dir, gfpgan_model, …)
```

```text
AssertionError: assert 'runner_execute' in []
```

**Classification:**

| Failure | New vs continuation |
|---------|---------------------|
| cmd-flags **500** | **Continuation** — M29.1 **`model_validate`** path on Pydantic v2 rejects **`None`** for **`str`** `FlagsModel` fields when **`vars(shared.cmd_opts)`** supplies explicit **`None`**. |
| **`test_txt2img_path_uses_runner`** | **New (test bug)** — **`TestRunner.execute`** is overwritten by a second monkeypatch on **`ProcessingRunner.execute`** after **`ProcessingRunner`** was aliased to **`TestRunner`**, so **`"runner_execute"`** is never appended. |

**Root cause hypothesis:**

- Optional CLI destinations are **`None`** at runtime; **`FlagsModel`** maps many to **`str`** + **`Field(default=None)`**; Pydantic v2 **`model_validate`** does not accept **`None`** for a plain **`str`** field when the key is present.
- **Smoke** (Pydantic v1 + **`parse_obj`**) did not hit this failure mode on PR checks.
- **Quality** (Pydantic v2) does.

### Minimal fix plan (invariants)

**Must not change:** API JSON shape/contract, CLI semantics, production runner behavior, smoke outcomes.

**Allowed:** `get_cmd_flags` — omit **`None`** values before **`model_validate`** so missing keys resolve via model defaults. Runner contract test — smallest fix: record **`runner_execute`** inside **`fake_execute`** and remove the conflicting double-patch.

**Preferred order:** (1) filter **`None`** in **`out`**; (2) fix test harness; (3) **`models.py`** only if still red.

### Implementation / validation

**PR #80** (`m29.2-quality-recovery` → `main`, squash merge **`03d9c167fb1abe929177aecf2e37837be766c091`**): docs + **`get_cmd_flags`** omit **`None`** + **`test_txt2img_runner_contract`** harness fix. PR checks: eslint / ruff / smoke **pass** (e.g. runs **`23617925743`**, **`23617934522`**).

**Intermediate Quality on `main` (post–#80):** **`23618080882`** — **failure**. **197 passed**, **2 failed** (cmd-flags only; runner test **pass**). **`output.txt`:** `ValidationError` for **`port`**: **`input_value=7860`**, **`input_type=int`**, field typed **`str`** — **`FlagsModel`** used **`_type = str`** whenever argparse **`default is None`**, ignoring **`--port`** **`type=int`**.

**PR #81** (`m29.2-flags-argparse-types` → `main`): **`modules/api/models.py`** — when **`flag.default is None`**, set field type from **`argparse` `type=`** (**`int`** / **`float`** / **`bool`** / else **`str`**). Merge: **`1b2e2f692d35365de584b7468e8bd9122617358a`**.

### Binding Quality PASS (M29 evidence)

**Run:** **`23618918747`** — https://github.com/m-cahill/serena/actions/runs/23618918747  
**Head:** **`1b2e2f692d35365de584b7468e8bd9122617358a`** (post–PR **#81**)

| Item | Result |
|------|--------|
| **Overall** | **success** |
| **pytest** | **199 passed**, 13 warnings, ~63s |
| **Coverage** | **~48%** total line coverage; **`--fail-under=42`** satisfied |
| **pip-audit (M28)** | **pass** (blocking step) |
| **Artifact `performance_snapshot.txt`** | **Yes** — workflow artifact name **`performance-snapshot`** |

**Snapshot contents (representative):** header **`# Serena performance_snapshot (M29)`**, **`generated_utc`**, **`sample_runner_execute_time_s=0.001067741000042588`**, **`sample_runner_total_time_s=0.0010740239999904588`** — confirms M29 instrumentation path executed in CI.

**M29 closeout:** **unblocked** — binding **Quality** green + **`performance_snapshot.txt`** present (see audit / ledger / tag **`v0.0.29-m29`**).
