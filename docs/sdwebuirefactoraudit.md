# Pre-Refactor Audit: Stable Diffusion WebUI

**Auditor:** CodeAuditorGPT (staff-plus, architecture-first)  
**Repository:** AUTOMATIC1111/stable-diffusion-webui  
**Workspace:** `c:\coding\refactoring\serena`  
**Commit:** `82a973c04367123ae98bd9abdf80d9eda9b910e2`  
**Goal:** Produce the best possible pre-refactor audit for a full-repo transformation to a **5/5** score.

All findings are grounded in the codebase with file paths and line ranges. For each major section: **Observations** = directly evidenced; **Inferences** = reasoned conclusions; **Recommendations** = proposed changes.

---

## 0. Scoring Rubric (Used Consistently)

| Score | Meaning |
|-------|---------|
| 0 | Catastrophic (actively dangerous / unusable) |
| 1 | Fragile (frequent breakage, no guardrails) |
| 2 | Poor (works, but hard to change safely) |
| 3 | Acceptable (works, some guardrails, clear pain points) |
| 4 | Strong (well-structured, predictable, maintainable) |
| 5 | Exemplary (clear architecture, guardrails, docs, observability) |

---

## 1. Executive Summary

**Overall score: 2.4 / 5**

| Category     | Score | Category     | Score |
|-------------|-------|-------------|-------|
| Architecture | 2.5  | Performance  | 3     |
| Modularity   | 2     | DX           | 2     |
| Code health  | 2.5  | Docs         | 2     |
| Tests & CI   | 2     | Extensions   | 2.5   |
| Security     | 2     | **Overall**  | **2.4** |

**Strengths**
- Clear entry points (`webui.py`, `launch.py`) and a single core package (`modules/`). **Evidence:** `webui.py:1-24`, `launch.py` delegates to `launch_utils`.
- Rich extension and script callback system (`script_callbacks`, `extensions`, `scripts`) enabling hooks without forking. **Evidence:** `modules/script_callbacks.py:219-243`, `modules/extensions.py:226-300`.
- CI runs lint (ruff, eslint) and a full pytest suite against a live server with coverage and artifact upload. **Evidence:** `.github/workflows/on_pull_request.yaml`, `.github/workflows/run_tests.yaml:61-80`.
- API and UI both funnel into the same processing pipeline (`process_images`), so behavior is consistent. **Evidence:** `modules/api/api.py:479-482`, `modules/txt2img.py:104-108`.

**Critical weaknesses**
- **Global state hub:** `shared.opts`, `shared.state`, `shared.sd_model` are defined in `shared.py` and written in `shared_init.py` and `processing.py`; dozens of modules read them. Testability and determinism suffer. **Evidence:** `modules/shared.py:14-46`, `modules/shared_init.py:19,46`, `processing.py:823-833,885-886`.
- **No test tiers or coverage gate:** Single test job; no smoke/quality/nightly; no `--cov-fail-under`. **Evidence:** `run_tests.yaml:58-61`.
- **God modules and tight coupling:** `processing.py` (~1793 LOC), `ui.py` (~1236 LOC), `api/api.py` (~929 LOC) import many modules and rely on `shared`. **Evidence:** `modules/processing.py:18-31`, `modules/ui.py:16-31`.
- **Dependency and CI hygiene:** Mixed pinning in `requirements.txt`; `package-lock.json` gitignored; CI uses `npm i --ci` and action tags (`@v4`). **Evidence:** `requirements.txt`, `.gitignore:40`, `on_pull_request.yaml:36`, `run_tests.yaml:14`.
- **No CONTRIBUTING or extension API contract:** Onboarding and extension stability rely on wiki/tribal knowledge. **Evidence:** No CONTRIBUTING.md; extension hooks in `script_callbacks` not versioned.

**Architectural posture**
- **Current:** Single Gradio/FastAPI app with a large procedural `modules/` package; `shared` and `ui` act as hubs; processing, API, and UI are intertwined via global state.
- **Intended (from repo):** None explicitly documented; structure suggests “one app, script-style, extend via callbacks.”
- **One-sentence description:** A monolithic Gradio/FastAPI app whose core is a single `modules` package with shared global state, a central processing pipeline, and a callback-based extension system.

---

## 2. Architecture & System Map

**Text-based architecture map**

- **Entrypoints**
  - `launch.py`: Parses args, prepares environment, calls `launch_utils.start()` → `webui.start()`. **Evidence:** `launch.py:25-43`, `modules/launch_utils.py`.
  - `webui.py`: Imports timer/initialize, exposes `create_api()` and `webui()`; `initialize.initialize()` loads options and model state. **Evidence:** `webui.py:1-50`, `modules/initialize.py`.

- **Core packages**
  - `modules/`: Core logic (processing, models, samplers, UI, API, extensions, paths, options). **Evidence:** Directory layout; 150+ Python files.
  - `extensions-builtin/`: Lora, LDSR, SwinIR, etc.; loaded via `extensions.list_extensions()`, scripts via `script_loading`. **Evidence:** `modules/extensions.py:226-300`, `modules/script_loading.py:10-16`.
  - `scripts/`: Built-in scripts (xyz_grid, outpainting, etc.); discovered and run via `modules.scripts`. **Evidence:** `scripts/xyz_grid.py:15-18`, `modules/scripts.py`.

- **Surfaces**
  - **API:** FastAPI routes under `/sdapi/v1/*`; handlers in `modules/api/api.py` build `StableDiffusionProcessing*` and call `process_images(p)`. **Evidence:** `modules/api/api.py:211-251,432-490`.
  - **UI:** Gradio built in `modules/ui.py`; tabs and controls call into `txt2img.py`, `img2img.py`, which create `p` and call `scripts.run` / `process_images`. **Evidence:** `modules/ui.py:16-31`, `modules/txt2img.py:19-55,101-108`.
  - **Runtime:** No separate “runtime” package; generation lives inside `processing.py` and sampler modules.
  - **Extension surface:** Extensions register callbacks via `script_callbacks.add_callback`; scripts extend `scripts.Script` and are loaded from `scripts/` and extension dirs. **Evidence:** `modules/script_callbacks.py:127-147`, `modules/scripts.py:51-120`.

**Layers as they actually exist**
1. **Entry / bootstrap:** `launch.py`, `webui.py`, `initialize.py`, `shared_init.py`.
2. **Configuration / CLI:** `shared_cmd_options`, `cmd_args`, `options`, `shared_options` → populate `shared.opts` and `cmd_opts`.
3. **Global state:** `shared.py` (opts, state, sd_model, device, etc.), `shared_state.State`.
4. **Orchestration:** `processing.process_images` → `process_images_inner`; scripts run before/after via `p.scripts`.
5. **Model/sampler:** `sd_models`, `sd_samplers`, `sd_vae`, `sd_hijack*`; LDM/diffusion in `modules/models/`.
6. **UI / API:** `ui.py`, `api/api.py`, `txt2img.py`, `img2img.py` — all depend on shared and processing.

**Hub modules**
- **`shared.py`:** Defines and re-exports `cmd_opts`, `opts`, `state`, `sd_model`, `device`, and many other globals; read by almost every feature module. **Evidence:** `modules/shared.py:14-95`.
- **`ui.py`:** Builds the Gradio UI; imports script_callbacks, sd_models, processing, ui_*, shared; central for all UI tabs. **Evidence:** `modules/ui.py:16-31`.

**Cross-cutting concerns**
- **Logging:** Standard `logging`; `modules/logging_config.py`; no structured/observability stack observed.
- **Config:** `options.Options` in `shared.opts`; loaded/saved via `shared_options` and UI; overrides applied in `process_images`. **Evidence:** `modules/options.py`, `processing.py:823-833`.
- **State:** `shared_state.State` (job, interrupted, sampling_step, etc.); mutated in processing, API, call_queue, progress. **Evidence:** `modules/shared_state.py:11-80`, grep of `state.` across modules.
- **Error handling:** `modules/errors.report()`; callbacks wrapped with try/except in `script_callbacks`. **Evidence:** `modules/script_callbacks.py:15-16,253-259`.

**Drift analysis**
- The repo does not claim a “clean layered” architecture. **Observation:** Layers are implicit (bootstrap → config → state → orchestration → model → UI/API). **Drift:** Orchestration and model code are mixed in `processing.py`; UI and API both depend directly on `shared` and processing with no abstraction layer. To reach a clean layered design would require extracting a **runtime layer** (generation pipeline with explicit inputs/outputs) and **dependency injection** for opts/state/model.

**Score: architecture 2.5 / 5**

---

## 3. Runtime Pipeline Analysis

**End-to-end generation pipelines**

**txt2img**
- **Request handling:** API: `api.text2imgapi(txt2imgreq)` builds `StableDiffusionProcessingTxt2Img` from request, sets `p.script_args`, then `scripts.scripts_txt2img.run(p, *p.script_args)` or `process_images(p)`. UI: `txt2img_create_processing()` builds `p` from Gradio args, then `scripts.scripts_txt2img.run(p, *p.script_args)` or `process_images(p)`. **Evidence:** `modules/api/api.py:432-490`, `modules/txt2img.py:14-55,101-108`.
- **Processing:** `process_images(p)` applies override_settings to `opts`, reloads model/VAE if needed, then `process_images_inner(p)`. **Evidence:** `modules/processing.py:819-858`.
- **Inner loop:** `process_images_inner(p)` fixes seed, sets job_count, calls `p.init()` then for each iteration `p.sample()` (which creates sampler, runs `sampler.sample(...)`, optionally hires pass). **Evidence:** `modules/processing.py:863-934,1307-1371`.
- **Sampler:** `sd_samplers.create_sampler(p.sampler_name, p.sd_model)`; sampler’s `sample(p, x, conditioning, unconditional_conditioning, ...)` produces latents; then `decode_first_stage` (or batch decode) and image save. **Evidence:** `modules/processing.py:1307-1345`, `modules/sd_samplers_common.py:73`, `modules/sd_samplers_kdiffusion.py:190`.
- **Model loading:** `shared.sd_model` is set by `sd_models.reload_model_weights()`; used inside `process_images` and in sampler. **Evidence:** `processing.py:828-830,885-886`, `modules/sd_models.py`.

**img2img / inpainting**
- Same orchestration: API or UI builds `StableDiffusionProcessingImg2Img` (with init_image, mask, etc.), then `process_images(p)`. `p.init()` and `p.sample()` are overridden in img2img subclass; init latent comes from VAE encode of image. **Evidence:** `modules/img2img.py:10-17`, `modules/processing.py` (img2img subclass).

**Orchestration**
- **Orchestration layer:** Effectively `process_images` + `process_images_inner` + `p.init()` / `p.sample()`. Scripts hook via `p.scripts.before_process`, `process`, `process_before_every_sampling`. **Evidence:** `processing.py:819-821,912-914,1336-1343`.
- **Sampler orchestration:** One sampler per `p`; created inside `p.sample()` (e.g. `sd_samplers.create_sampler(self.sampler_name, self.sd_model)`). **Evidence:** `processing.py:1307-1308,1384`.
- **Model loading and selection:** `sd_models.reload_model_weights()` / `get_closet_checkpoint_match`; override in `p.override_settings['sd_model_checkpoint']`. **Evidence:** `processing.py:828-836`, `modules/sd_models.py`.
- **Seed handling:** `get_fixed_seed(p.seed)`; `p.all_seeds`/`p.all_subseeds` set in `process_images_inner`; `p.rng` used in sample. **Evidence:** `processing.py:871-907`, `processing.py:1335,1759-1760`.
- **Batching:** `p.n_iter` outer iterations; `p.batch_size` per iteration; loop in `process_images_inner` over batches. **Evidence:** `processing.py:929-934` and following.

**Control flow**
- **Tangled/duplicated:** Override application and model/VAE reload are in `process_images`; seed/prompt setup in `process_images_inner`; script hooks at multiple points. Some logic (e.g. hires) is in `StableDiffusionProcessingTxt2Img.sample` and `sample_hr_pass` (large methods). **Evidence:** `processing.py:819-858,863-934,1307-1393`.
- **Seams for a “runtime” layer:** (1) Everything after `p.init()` and before image save could be a pure function `run_sampling(p, sampler, model, rng)`. (2) Override application could be a function that returns an opts snapshot and restores it. (3) Script hooks could be a formal pipeline stage interface.

**Reproducibility**
- **Exact inputs for reproducible output:** Seed(s), subseed, subseed_strength, prompt, negative_prompt, sampler, steps, cfg_scale, dimensions, model (checkpoint), VAE, and all options that affect sampling (e.g. clip_skip). Override_settings applied in `process_images` mutate `opts` for the duration of the run. **Evidence:** `processing.py:823-833,871-907`, `StableDiffusionProcessing` dataclass fields.
- **Inherent vs avoidable nondeterminism:** Inherent: none if seed and hardware are fixed. Avoidable: (1) `opts` and `state` are global, so concurrent or re-entrant calls can interfere. (2) Model/VAE loaded from `shared` so any change elsewhere affects the run. Passing opts/state/model explicitly would make runs deterministic given the same inputs.

---

## 4. Global State & State Model

**Global state inventory**

| Variable | Definition | Writers | Readers (representative) |
|---------|------------|---------|---------------------------|
| `shared.cmd_opts` | `shared_cmd_options.cmd_opts` | Parsed at startup | Many (paths, options, extensions, api) |
| `shared.opts` | `options.Options(...)` in shared_init | `shared_init.py:19`; `opts.set()` in processing, options UI | processing, api, ui, sd_models, sd_samplers, images, etc. |
| `shared.state` | `shared_state.State()` in shared_init | `shared_init.py:46`; `state.begin()`, `.skip()`, `.interrupt()`, job_count/sampling_step in processing, progress, api | processing, progress, api, ui_toprow, call_queue, sd_samplers_cfg_denoiser |
| `shared.sd_model` | `shared.py:46` | sd_models (load/unload) | processing, api, ui, sd_samplers, sd_hijack, etc. |
| `shared.device` | `shared.py:25` | initialization | processing, models, samplers |
| `shared.demo` | `shared.py:23` | ui.py (create_ui) | webui, ui |
| `shared.hypernetworks`, `loaded_hypernetworks` | `shared.py:31-33` | hypernetwork loading | sd_hijack, api |
| `shared.sd_upscalers` | `shared.py:63` | upscaler registration | api, extras |
| `shared.face_restorers` | `shared.py:41` | face_restoration_utils | api, processing |
| `shared.prompt_styles`, `interrogator`, `total_tqdm`, `mem_mon` | `shared.py:37-39,71,73,74` | ui/init / progress | ui, progress, etc. |

**State mutation map (who mutates what)**
- **opts:** Set at startup from config; mutated in `process_images` for override_settings; restored in `finally` if `override_settings_restore_afterwards`; also mutated by options UI. **Evidence:** `processing.py:823-833,851-854`, `modules/options.py`.
- **state:** `state.begin(job=...)` at API/UI entry; `state.job_count`, `state.sampling_step`, `state.current_image`, etc. set during processing; `state.interrupt()`, `state.skip()` from API. **Evidence:** `modules/shared_state.py`, `processing.py:927-928`, `api/api.py:475`.
- **sd_model:** Loaded/unloaded by `sd_models.reload_model_weights()`, called from processing and API. **Evidence:** `modules/sd_models.py`, `processing.py:828-836`.

**Classification**
- **Configuration:** `cmd_opts`, `opts` (with override_settings applied per run).
- **Runtime execution:** `state` (job, interrupted, sampling_step, current_image, etc.).
- **Model registry:** `sd_model`, `clip_model`, `sd_upscalers`, `face_restorers`, `hypernetworks`, `loaded_hypernetworks`.
- **UI/session:** `demo`, `settings_components`, `tab_names`, `gradio_theme`, `prompt_styles`.
- **Extension-owned:** Extensions register callbacks and scripts; extension list in `extensions.extensions`; no single “extension state” object.

**Testability impact:** Unit-testing any code that reads `shared.opts` or `shared.state` or `shared.sd_model` requires patching globals or starting the full app. **Determinism impact:** Concurrent or sequential runs can affect each other via shared opts/state/model. **Extension impact:** Extensions that read or mutate `shared` are tied to the current layout; any refactor of shared state can break them.

**Score: modularity 2 / 5** (reflects global-state risk)

---

## 5. Dependency Graph & Coupling

**Top 20 most imported modules (by number of files importing)**  
(Derived from grep of `from modules.* import` / `import modules.*` in repo.)

1. `shared` / `modules.shared`
2. `paths_internal` (paths, script_path, models_path, etc.)
3. `processing` (Processed, process_images, StableDiffusionProcessing*)
4. `options` / `OptionInfo`, `options_section`
5. `script_callbacks`
6. `ui_components`
7. `sd_samplers` / `sd_models`
8. `infotext_utils`
9. `images`
10. `scripts`
11. `shared_cmd_options` / `cmd_opts`
12. `sd_hijack` / `model_hijack`
13. `errors`
14. `devices`
15. `extensions`
16. `paths`
17. `upscaler` / `Upscaler`, `UpscalerData`
18. `util`
19. `sd_vae`
20. `ui_common`

**Top 10 hub modules (inbound references)**
1. `shared` — re-exports and global state; used by almost every feature module.
2. `paths_internal` — paths used by options, shared, extensions, config, images.
3. `processing` — API, UI, scripts all call process_images and use Processed.
4. `script_callbacks` — samplers, scripts, extensions register and call callbacks.
5. `options` / `shared_options` — UI and shared depend on OptionInfo/options_section.
6. `ui_components` — ui_*, scripts use FormRow, ToolButton, etc.
7. `sd_samplers` / `sd_models` — processing, api, scripts, ui.
8. `infotext_utils` — ui, processing, api, scripts.
9. `images` — ui, processing, api, extras.
10. `scripts` — ui, api, txt2img, img2img, extensions.

**Cyclic dependencies**
- No strict import cycles detected at module level (Python would fail to load). **Observation:** `shared` imports `shared_cmd_options`, `options`, `shared_items`, etc.; those do not import `shared` at top level (some use it at runtime). So no cycle in the static graph. **Inference:** Cycles could appear at runtime (e.g. script_callbacks → shared → options → …). Not fully traced here.

**God modules**
- **ui.py:** ~984 LOC; imports 16+ modules; builds entire Gradio UI. **Evidence:** `modules/ui.py:16-31`, file size.
- **processing.py:** ~1793 LOC; imports 15+ modules; contains processing classes and the full sampling loop. **Evidence:** `modules/processing.py:18-31`, line count.
- **api/api.py:** ~929 LOC; many routes and handlers; imports shared, processing, scripts, sd_models, etc. **Evidence:** `modules/api/api.py:19-34`, file size.

**God functions**
- `process_images_inner` — long loop, seed/prompt setup, batch iteration, script hooks. **Evidence:** `processing.py:863-~1100+`.
- `StableDiffusionProcessingTxt2Img.sample` and `sample_hr_pass` — large methods with hires and decode logic. **Evidence:** `processing.py:1307-1393`.

**Per major module (summary)**
- **shared:** Inbound: almost all; outbound: shared_cmd_options, options, paths_internal, util, shared_items, shared_gradio_themes. Reliance on global state: is the state holder.
- **processing:** Inbound: api, img2img, txt2img, scripts (many). Outbound: shared, sd_models, sd_samplers, sd_vae, devices, scripts, images, etc. Heavy reliance on shared.opts, shared.state, shared.sd_model.
- **api/api:** Inbound: webui (create_api). Outbound: shared, processing, scripts, sd_models, images, progress, etc. Reliance on shared and process_images.

**Import centrality vs runtime criticality:** `shared` is central both in imports and at runtime (opts/state/sd_model). `processing` is runtime-critical and highly imported. `paths_internal` is central for imports but less “hot” at runtime.

**Surgical decouplings (3–5, PR-sized)**
1. **Pass opts snapshot into process_images:** Add a helper that builds a dict or small struct from `opts` (and override_settings) and pass it into a new `process_images_with_opts(p, opts_snapshot)` used by one API endpoint first; keep reading from snapshot instead of global inside that path. **Evidence to address:** `processing.py:823-833`.
2. **Extract “sampler runner”:** Move the call `self.sampler.sample(self, x, conditioning, ...)` and the immediate decode into a function `run_sampler_step(p, sampler, x, conditioning, uc, image_cond)` in a new module; call it from `StableDiffusionProcessingTxt2Img.sample`. Reduces god-method size and gives a seam for testing. **Evidence:** `processing.py:1345`.
3. **UI tab registry:** Replace the single `ui.create_ui()` with a list of “tab builders”; each tab is a function that returns (name, blocks). Register txt2img, img2img, settings, etc. from their modules. One PR: move one tab into a function and register it. **Evidence:** `modules/ui.py` (single create_ui).
4. **API handler → processing adapter:** Introduce `Txt2ImgRunner.run(request) -> Processed` that builds `p`, calls `process_images(p)`, returns `Processed`; have `text2imgapi` call `Txt2ImgRunner.run(txt2imgreq)`. Keeps API thin and gives a single place to swap implementation later. **Evidence:** `api/api.py:432-490`.
5. **Extension callback types:** In `script_callbacks`, add a small module that defines dataclasses or protocols for each callback param (e.g. `ImageSaveParams` already exists). Document and version the callback signatures; add a “supported callback API version” constant. **Evidence:** `script_callbacks.py:19-109,219-243`.

**Score: modularity 2 / 5**

---

## 6. Code Health & Maintainability

**File size distribution (top 20 by LOC)**

| Path | LOC |
|------|-----|
| modules/processing.py | 1793 |
| modules/models/diffusion/ddpm_edit.py | 1236 |
| modules/ui.py | 984 |
| modules/scripts.py | 790 |
| modules/models/diffusion/uni_pc/uni_pc.py | 752 |
| modules/sd_models.py | 750 |
| modules/api/api.py | 750 |
| modules/images.py | 673 |
| modules/deepbooru_model.py | 668 |
| modules/ui_extra_networks.py | 662 |
| scripts/xyz_grid.py | 643 |
| modules/hypernetworks/hypernetwork.py | 633 |
| modules/textual_inversion/textual_inversion.py | 564 |
| modules/ui_extensions.py | 544 |
| modules/models/sd3/mmdit.py | 528 |
| modules/sd_hijack_optimizations.py | 501 |
| modules/script_callbacks.py | 437 |
| modules/models/sd3/other_impls.py | 417 |
| modules/infotext_utils.py | 400 |
| modules/shared_options.py | 385 |

**Complexity hotspots (top functions by scope and branches)**
- `process_images_inner` — long loop, many branches, script hooks. **Evidence:** `processing.py:863-~1100`.
- `StableDiffusionProcessingTxt2Img.sample` / `sample_hr_pass` — hires logic, decode paths. **Evidence:** `processing.py:1307-1393`.
- `ui.create_ui` — builds all tabs and controls. **Evidence:** `modules/ui.py` (single large function/flow).
- Sampler `sample` methods (e.g. k-diffusion, timesteps) — steps, conditioning. **Evidence:** `sd_samplers_kdiffusion.py:190`, `sd_samplers_timesteps.py:141`.
- `api.text2imgapi` / `img2imgapi` — request parsing, script args, process_images. **Evidence:** `api/api.py:432-565`.

**Lint configuration**
- **Ruff:** `pyproject.toml`: select B, C, I, W; ignore E501, E721, E731, I001, C901, C408, W605; per-file ignore E402 in webui.py. **Evidence:** `pyproject.toml:1-35`.
- **Pylint:** `.pylintrc` disables C, R, W, E, I. **Evidence:** `.pylintrc:2-3`.
- **Observation:** Line length and complexity (C901) are ignored; many long files and long functions.

**Anti-patterns**
- **Broad imports:** `from modules import shared` then use of `shared.opts`, `shared.state` everywhere. **Evidence:** grep results across modules.
- **Re-exports:** `shared.py` re-exports `cmd_opts`, `OptionInfo`, `natural_sort_key`, `list_checkpoint_tiles`, etc. **Evidence:** `shared.py:75-95`.
- **Dynamic imports:** `script_loading.load_module(path)` for extensions; scripts loaded by importlib. **Evidence:** `script_loading.py:10-16`, `extensions.py` (preload).
- **Broad except:** Callbacks wrapped with try/except that report and continue. **Evidence:** `script_callbacks.py:254-259`.

**Dead code / unused abstractions**
- `batch_cond_uncond` in shared (“old field, unused now”). **Evidence:** `shared.py:17`.
- No automated dead-code analysis run; inference: large files likely contain legacy or redundant paths.

**Score: code_health 2.5 / 5**

---

## 7. Tests, CI/CD & Reproducibility

**Test pyramid**
- **Unit:** Almost none; a few tests in `test_torch_utils.py`, `test_utils.py` (e.g. parametrized URL/float checks). **Evidence:** `test/test_torch_utils.py`, `test/test_utils.py`.
- **Integration:** Majority: tests start the app (via `launch.py --test-server`), then pytest hits HTTP endpoints (e.g. `/sdapi/v1/txt2img`). **Evidence:** `test/test_txt2img.py:42-43`, `conftest.py:34-36`, `run_tests.yaml:44-61`.
- **E2E:** Same as integration (server + HTTP); no separate E2E layer.

**Coverage**
- Collected: `coverage run` for server, `pytest --cov . --cov-report=xml`. **Evidence:** `run_tests.yaml:46-61,65-69`.
- No `--cov-fail-under` or threshold in config. **Evidence:** grep for cov-fail-under / fail_under: none.

**Flakiness risks**
- Server startup: `wait-for-it --service 127.0.0.1:7860 -t 20`; if startup is slow or port in use, tests fail. **Evidence:** `run_tests.yaml:58-59`.
- Single job: server and pytest in one job; no retries or separate smoke step.

**CI job structure**
- Lint: ruff (Python), eslint (JS); on push/PR. **Evidence:** `on_pull_request.yaml`.
- Tests: one job “tests on CPU with empty model”; install deps, launch server in background, pytest, upload artifacts. **Evidence:** `run_tests.yaml`.
- Branch policy: `warns_merge_master.yml` fails PRs targeting `master`. **Evidence:** `warns_merge_master.yml:9-12`.

**Reproducibility**
- **Python:** `requirements.txt` mixed pins; `requirements_versions.txt` has more pins; CI uses `requirements-test.txt` + `launch.py` with TORCH_INDEX_URL for CPU. No single lockfile. **Evidence:** `requirements.txt`, `requirements_versions.txt`, `run_tests.yaml:29-40`.
- **JS:** `package-lock.json` in `.gitignore`; CI uses `npm i --ci`. **Evidence:** `.gitignore:40`, `on_pull_request.yaml:36`.
- **Models:** CI caches `models` with key `2023-12-30`; tests run with “empty model” (no download in test flow). **Evidence:** `run_tests.yaml:24-28`.

**Action pinning**
- Uses tags: `actions/checkout@v4`, `actions/setup-python@v5`, `actions/cache@v4`, `actions/upload-artifact@v4`. Not SHA-pinned. **Evidence:** `on_pull_request.yaml:14,15`, `run_tests.yaml:14,25,71,78`.

**3-tier test strategy (recommended)**
- **Tier 1 (smoke):** Single health or minimal txt2img request; run first; required; low threshold (e.g. 5% coverage or none). **Acceptance:** Job completes in &lt;2 min; required on PR.
- **Tier 2 (quality):** Full test suite; coverage gate with ≥2% margin below current; required. **Acceptance:** All tests pass; coverage above threshold.
- **Tier 3 (nightly):** Same suite + optional extras; non-blocking; alert on failure. **Acceptance:** Runs on schedule; artifacts and report.

**Coverage threshold plan**
- Measure current coverage (e.g. `coverage report -i` after one run). Set `--cov-fail-under=X` where X = current − 2%. Enforce in Tier 2.

**Reproducible environment plan**
- Single locked manifest for CI: e.g. generate `requirements-ci.txt` from current env with pins; use in CI. Commit `package-lock.json` and use `npm ci` for JS. Document model expectations (empty for CI; optional cache key for reproducibility).

**Score: tests_ci 2 / 5**

---

## 8. Security & Supply Chain

**Dependency pinning**
- **Observation:** `requirements.txt` has mixed: some `==` (gradio, protobuf, transformers), some `>=` (fastapi). `requirements_versions.txt` pins many. No single source of truth for CI. **Evidence:** `requirements.txt`, `requirements_versions.txt`.
- **Inference:** Supply-chain and build reproducibility are at risk without a single locked manifest.

**Vulnerability exposure**
- No `pip-audit` or `npm audit` in CI. **Evidence:** Grep: no pip-audit/npm audit in workflows.
- Known sensitive deps: `protobuf==3.20.0` (historical CVE; 3.20.x had fixes); versions in repo may have known issues. Recommend running `pip-audit` and `npm audit` to get current list.

**Secret handling**
- API auth uses `secrets.compare_digest` for HTTP basic. **Evidence:** `modules/api/api.py:17` (import). No secrets in repo observed; no dedicated secret scan in CI.

**CI trust boundaries**
- Workflows use checkout, setup-python, setup-node, cache, upload-artifact. **Evidence:** workflow files.
- **Recommendation:** Pin all actions to full SHA to avoid action supply-chain risk.

**SBOM**
- No SBOM or dependency export found in repo or workflows.

**Recommendations**
- Add `pip-audit` (and optionally `npm audit`) as a CI step; fail or warn on known vulns.
- Pin GitHub Actions to immutable SHAs.
- Use locked manifests: one for Python (CI), commit and use `package-lock.json` with `npm ci`.

**Score: security 2 / 5**

---

## 9. Performance & Scalability

**Hot paths**
- **processing.py:** `process_images_inner`, `p.sample()`, sampler `sample()`, decode_first_stage / batch decode. **Evidence:** `processing.py:863-934`, `sd_samplers_common.py:73`.
- **Model forward:** Inside sampler and LDM/diffusion models. **Evidence:** `modules/models/diffusion/`, `sd_samplers_*.py`.

**Model loading and caching**
- Models loaded via `sd_models.reload_model_weights()`; kept in `shared.sd_model`. VAE similarly. **Evidence:** `modules/sd_models.py`, `modules/sd_vae.py`.
- Caching: `diskcache` in requirements; `modules/cache.py` used for extension git info. **Evidence:** `requirements.txt`, `modules/cache.py`, `extensions.py:146`.

**Queueing**
- Gradio queue: `shared.demo.queue(64)`. **Evidence:** `webui.py:69`.
- API: queue lock in `call_queue`; `wrap_gradio_gpu_call` etc. **Evidence:** `modules/call_queue.py`, `api/api.py` (task_id, start_task, finish_task).

**Performance risks**
- Repeated I/O: model load on first request; embedding reload when not disabled. **Evidence:** `processing.py:909-910` (embedding load).
- Unnecessary recomputation: no obvious redundant forward passes; some options (e.g. live preview) add work. **Evidence:** `processing.py:923-924`.

**Profiling plan**
1. Run a single txt2img request with `python -m cProfile -o trace.stats` (or PyTorch profiler) and inspect hotspots in `process_images_inner` and sampler.
2. Add a lightweight `/sdapi/v1/health` or `/sdapi/v1/timing` that returns startup time and (if stored) last-request latency for smoke and monitoring.
3. Optionally: small load script (e.g. 10 sequential txt2img) to measure P95 latency.

**Performance budget proposal**
- Not stated in repo. **Recommendation:** If performance is a goal, define e.g. “P95 txt2img (N steps) &lt; X s on CPU test config” and “startup &lt; Y s”; measure in CI or nightly and alert on regression.

**Score: performance 3 / 5**

---

## 10. Developer Experience (DX)

**15-minute new-dev journey**
- **Steps:** Clone → install Python 3.10.x (and Node for lint) → run `webui-user.bat` or `webui.sh` (first run installs deps) → run `ruff .` and `npm run lint` → run tests (start server in background, then `pytest test/`). **Evidence:** README, workflow files.
- **Blockers:** No single “run tests” script; CONTRIBUTING missing; lockfile gitignored so `npm ci` not possible; tests require full server.

**Local test workflow**
- **Lint:** `ruff .` (Python), `npm run lint` (JS). **Evidence:** `package.json`, `pyproject.toml`.
- **Tests:** Start server (`launch.py --skip-torch-cuda-test --test-server ...`), then `pytest test/` (or `pytest test/test_txt2img.py -v`). **Evidence:** `run_tests.yaml:44-61`, `conftest.py`.
- **Single test:** `pytest test/test_txt2img.py::test_txt2img_simple_performed -v` (with server running).

**CONTRIBUTING**
- **Observation:** No CONTRIBUTING.md in repo. **Evidence:** No file found.
- **Recommendation:** Add CONTRIBUTING.md with lint commands, test commands, branch policy (e.g. PR to dev), and link to extension docs.

**Extension developer experience**
- **Observation:** Extension authors learn from wiki and by reading `script_callbacks`, `scripts.Script`, and built-in extensions. No single “Extension API” doc in repo. **Evidence:** CODEOWNERS comment about localizations and extensions wiki.
- **Recommendation:** Document callback list and signatures, script lifecycle, and “supported API version”; provide a minimal extension template and test approach (e.g. run with one extension enabled).

**Score: dx 2 / 5**

---

## 11. Documentation

**README**
- **Observation:** Installation (Windows/Linux), features, running, limitations (e.g. Python 3.10.6). **Evidence:** `README.md:94-120`, feature list.
- **Gaps:** No “Development” or “Contributing” section; no local test/lint steps.

**CONTRIBUTING**
- **Observation:** Absent. **Evidence:** No CONTRIBUTING.md.

**Architecture docs**
- **Observation:** No ADRs or architecture diagrams in repo. **Evidence:** No docs in repo root or docs/.

**Extension API docs**
- **Observation:** Callback names and param types exist in code (`script_callbacks.py`); no explicit “contract” doc or versioning. **Evidence:** `script_callbacks.py:19-109,219-243`.
- **Inference:** Extension API is tribal knowledge plus code inspection.

**Score: docs 2 / 5**

---

## 12. Extension Ecosystem Stability

**Extension loading**
- **Discovery:** `list_extensions()` scans `extensions_builtin_dir` and `extensions_dir`; builds `Extension` with `ExtensionMetadata` from `metadata.ini`. **Evidence:** `extensions.py:226-300`.
- **Import:** Scripts under extension dirs loaded via `script_loading.load_module()` (e.g. `preload.py`); scripts list from `extension.list_files('scripts', '.py')`. **Evidence:** `script_loading.py:10-16`, `extensions.py:178-189`.
- **Lifecycle:** Extensions listed at startup; enabled/disabled via opts; callbacks registered when scripts load. **Evidence:** `extensions.active()`, `shared.opts.disabled_extensions`.

**Extension API surface**
- **Hooks/callbacks:** `script_callbacks.callback_map` (app_started, model_loaded, ui_tabs, before_image_saved, cfg_denoiser, etc.). **Evidence:** `script_callbacks.py:219-243`.
- **Stability:** No version field in callback API; params are dataclasses (e.g. `ImageSaveParams`). Adding or changing params can break extensions. **Evidence:** `script_callbacks.py:19-109`.

**Backwards compatibility risks**
- Extensions import `modules.*` (e.g. `modules.ui_components`, `modules.scripts`, `modules.processing`, `modules.shared`). Any rename or move of these breaks them. **Evidence:** `extensions-builtin/Lora/network_lora.py:4`, `extensions-builtin/soft-inpainting/scripts/soft_inpainting.py:4-6`.
- **Classification:** **Internal-but-relied-upon:** `modules.shared`, `modules.scripts`, `modules.processing`, `modules.ui_components`, `modules.paths_internal`, `modules.script_callbacks`. **Semi-private:** callback param types (used by extensions but not clearly versioned). **Stable:** Only the existence of callback names and the Script base class; no formal stability guarantee.

**Governance gaps**
- No extension API versioning; no deprecation policy; no compatibility matrix (e.g. “extensions built for API v1”).

**Recommendations**
- **Extension API contract:** Publish a minimal doc listing callback names, param types, and “contract version” (e.g. 1.0); state that new fields may be added but existing ones will not be removed for that version.
- **Versioning:** Add `EXTENSION_API_VERSION = "1.0"` and document what it covers; bump when breaking callback or Script interface changes.
- **Deprecation path:** For breaking changes, add new callbacks or params, deprecate old ones with a comment and log warning, remove in next major version.

**Score: extensions 2.5 / 5**

---

## 13. Target Architecture Definition (What 5/5 Looks Like)

**Clear separation**
- **Runtime (generation pipelines):** A dedicated package or module that takes (prompt, negative_prompt, sampler_name, steps, seed, model_ref, opts_snapshot, …) and returns (images, infotext). No global `shared.opts` or `shared.sd_model` inside this layer; model and sampler are injected or resolved from a registry interface.
- **API:** HTTP layer that maps requests to runtime inputs and runtime outputs to responses; uses a runner/adapter that calls the runtime with explicit parameters.
- **UI:** Gradio (or other) that builds controls and calls the same runner or runtime via a thin adapter; no direct access to `shared.sd_model` or processing internals for generation.
- **Extension system:** Documented callback and Script API with a version; extensions register with a stated contract; core does not depend on extension internals.

**Explicit dependency injection**
- **Models:** Runtime receives a “model provider” or “checkpoint loader” interface; API/UI obtain it from a registry (which may still wrap `sd_models`) and pass it in.
- **Samplers:** Sampler creation behind an interface; runtime gets a sampler for the current model and step config.
- **Configuration:** Options passed as a snapshot (or immutable view) into the runtime; no `opts.set()` inside the core pipeline.

**No critical global state in hot paths**
- Generation path uses only explicit arguments and injected dependencies; `state` (job, interrupted) can remain for progress/cancellation if accessed via a narrow interface (e.g. “execution context”) rather than raw global.

**Deterministic artifact outputs**
- Same (seed, prompt, opts_snapshot, model version) → same output; runtime is pure modulo RNG and model weights.

**Reproducible CI**
- Pinned Python deps (lockfile or single requirements-ci.txt); committed package-lock.json and `npm ci`; SHA-pinned GitHub Actions; 3-tier tests with coverage gate and ≥2% margin.

**Stable extension API**
- Documented callback and Script contract; version number; deprecation policy (new optional params allowed; removal only with version bump and notice).

---

## 14. Refactorability & Extraction Analysis

**Architectural fault lines**
- **Runtime vs rest:** Boundary = “everything needed to produce images from (prompt, seed, opts, model, sampler).” Cut at: (1) entry to `process_images_inner` (caller supplies opts snapshot and model reference), (2) exit after `Processed` is built. **Evidence:** `processing.py:863-858`.
- **API vs shared:** Boundary = API handlers should not read/write `shared` except via a narrow facade (e.g. “get current model,” “apply overrides”). Cut at: replace direct `opts`/`sd_models` usage in `api.py` with calls to an adapter. **Evidence:** `api/api.py:471-472`, `opts.outdir_*`.
- **UI vs processing:** Boundary = UI should only build `p` and call a single entry point (e.g. `run_txt2img(p)` or script runner). Cut at: `txt2img()` / `img2img()` in txt2img.py/img2img.py already call `process_images(p)`; further cut = move creation of `p` into an adapter that takes “request” and returns `Processed`.

**Safe extraction seams**
- **Seed/prompt setup:** Logic in `process_images_inner` that sets `p.all_seeds`, `p.all_prompts` could move to a `prepare_prompts_and_seeds(p)` function in the same file. **Evidence:** `processing.py:871-907`.
- **Override apply/restore:** The block in `process_images` that applies override_settings and restores in `finally` could be a context manager `with temporary_opts(override_settings): ...`. **Evidence:** `processing.py:823-857`.
- **Script callbacks (params):** `script_callbacks` already uses dataclasses; moving them to a `callback_params.py` (or keeping and documenting) is a small, safe move. **Evidence:** `script_callbacks.py:19-109`.

**Minimal architectural cuts**
- **Extract runtime layer:** (1) Introduce `runtime.run_txt2img(p, opts_snapshot, model_provider)` that does not read `shared.opts`/`shared.sd_model` inside; call it from `process_images` with snapshot and current model. (2) Gradually move logic from `process_images_inner` into `runtime` and pass opts/model explicitly.
- **Decouple UI from processing:** (1) Keep UI building `p` and calling `scripts.run` / `process_images`; (2) Introduce `ProcessingRunner.run_txt2img(args)` that returns `Processed`; UI and API both call the runner. No need to change UI internals in the first cut.
- **Decouple API from shared:** (1) API builds `p` and calls a runner that takes `p` and (optionally) opts_snapshot; (2) Runner uses snapshot for paths/options instead of `opts` global; (3) Model still from registry/facade until a later phase.

**Recommended order of extractions**
1. **Phase 0 (stabilize):** Pin CI actions to SHA; add smoke test; add pip-audit; commit package-lock and use npm ci. No architectural change.
2. **Phase 1 (seams):** Add CONTRIBUTING; document extension callback API version; add `temporary_opts` (or equivalent) and use it in `process_images`; add pytest markers for smoke.
3. **Phase 2 (runtime boundary):** Introduce `opts_snapshot` type and build it in `process_images` from `opts` + override_settings; pass snapshot into `process_images_inner` and refactor inner to read from snapshot where possible (leave `state` and model for later).
4. **Phase 3 (runner):** Add `Txt2ImgRunner` / `Img2ImgRunner` (or single `ProcessingRunner`) that builds `p`, applies overrides, calls `process_images`, returns `Processed`; switch API and then UI to use runner.
5. **Phase 4 (model injection):** Introduce a model-provider interface; runtime gets model from provider instead of `shared.sd_model`; registry implementation wraps current sd_models. Then option to run tests with a mock provider.
6. **Phase 5 (UI registry):** Replace monolithic `create_ui` with a list of tab builders; move one tab at a time into a builder and register.

---

## 15. Refactor Strategy (Goal: 5/5)

### Option A — Iterative (low blast radius)

- **PR-sized steps,** each ≤60 minutes; reversible.
- **Focus:** CI guardrails, test tiers, pinning, small decouplings.

**Phases**
- **Phase 0 — Fix-first & stabilize (0–1 day):** Add smoke test (one health or txt2img); pin checkout/setup-python to SHA; add pip-audit step; upload artifacts on fail. **Risks:** Low. **Rollback:** Revert workflow changes.
- **Phase 1 — Document & guardrail (1–3 days):** CONTRIBUTING.md; pytest markers (smoke); explicit test path in CI; pin Ruff/pytest in requirements-test; commit package-lock, use npm ci. **Risks:** Low. **Rollback:** Revert doc and workflow.
- **Phase 2 — Harden (3–7 days):** Add --cov-fail-under with 2% margin; make smoke required; add “quality” job or ordered steps. **Risks:** Medium (coverage may fluctuate). **Rollback:** Remove threshold.
- **Phase 3 — Small decouplings (ongoing):** temporary_opts context manager; prepare_prompts_and_seeds extraction; one API endpoint via Txt2ImgRunner; extension API version constant + doc. **Risks:** Low per PR. **Rollback:** Revert individual PRs.

**Milestone labels:** Phase 0–1 = foundational; Phase 2 = hardening; Phase 3 = enabling (enables later architectural work).

### Option B — Strategic (structural)

- **Introduce runtime/service layer:** Extract generation into a module that accepts opts_snapshot and model provider; move sampling loop and decode there.
- **Decouple shared.py:** Pass option/state snapshots into processing; introduce “execution context” for state if needed; reduce direct shared reads in hot path.
- **Modularize UI:** Tab registry; one tab per module; lazy or explicit registration.
- **ProcessingRunner:** API and UI call a runner that builds `p`, applies overrides, calls runtime, returns Processed.
- **3-tier CI with coverage gates:** Smoke (required), quality (required, coverage threshold), nightly (optional, alert).
- **Deterministic environment:** Locked Python manifest for CI; npm ci; document model handling.

**Phases**
- **Phase 0:** Same as Option A (stabilize). **Goals:** Reliable CI. **Risks:** Low. **Rollback:** Revert.
- **Phase 1:** Runtime boundary + opts_snapshot. **Goals:** process_images_inner receives opts_snapshot; no opts.set in inner. **Risks:** Medium (large diff). **Rollback:** Feature-flag or branch; keep old path.
- **Phase 2:** ProcessingRunner + API/UI switch. **Goals:** Single entry for generation; API and UI call runner. **Risks:** Medium. **Rollback:** Keep old API/UI paths until runner stable.
- **Phase 3:** Model provider interface; 3-tier CI; extension API version and doc. **Goals:** Testable runtime with mock model; full guardrails; stable extension contract. **Risks:** Medium. **Rollback:** Per-component revert.

**Milestone labels:** Phase 0 = foundational; Phase 1–2 = architectural; Phase 3 = hardening.

---

## 16. Risk Register

| id | title | likelihood | impact | mitigation | residual risk |
|----|--------|------------|--------|-------------|----------------|
| R1 | Dependency vuln (PyTorch/Gradio/etc.) | medium | high | pip-audit + npm audit in CI; pin major deps | low |
| R2 | Flaky CI (server startup / port) | medium | medium | Smoke tier with health endpoint; increase wait-for-it or retries | low |
| R3 | Coverage regression | high | medium | Add --cov-fail-under with 2% margin | low |
| R4 | Action/plugin compromise | low | high | Pin all actions to full SHA | low |
| R5 | Breaking extension API | medium | high | Document and version callback/Script API; deprecation path | medium |
| R6 | Refactor introduces bugs in generation | medium | high | Small PRs; feature flags; keep old path until new path validated | medium |
| R7 | Global state races (concurrent requests) | low | high | Queue/lock already in place; document single-worker assumption or add tests | low |

---

## 17. Machine-Readable Appendix (JSON)

```json
{
  "issues": [
    {
      "id": "ARC-001",
      "title": "Extract runtime layer with explicit opts and model",
      "category": "architecture",
      "path": "modules/processing.py:863-934",
      "severity": "high",
      "priority": "high",
      "effort": "high",
      "impact": 5,
      "confidence": 0.9,
      "evidence": "process_images_inner and sample() read shared.opts, shared.state, shared.sd_model throughout.",
      "fix_hint": "Introduce opts_snapshot and pass into process_images_inner; add model_provider interface and use it in sample()."
    },
    {
      "id": "MOD-001",
      "title": "Reduce shared global state in hot path",
      "category": "modularity",
      "path": "modules/shared.py:14-46",
      "severity": "high",
      "priority": "high",
      "effort": "high",
      "impact": 5,
      "confidence": 0.95,
      "evidence": "opts, state, sd_model defined in shared; written in shared_init and processing; read by dozens of modules.",
      "fix_hint": "Pass opts/state snapshot into process_images; introduce execution context for state."
    },
    {
      "id": "CI-001",
      "title": "Add coverage threshold and 3-tier tests",
      "category": "tests_ci",
      "path": ".github/workflows/run_tests.yaml:61",
      "severity": "medium",
      "priority": "high",
      "effort": "medium",
      "impact": 4,
      "confidence": 1.0,
      "evidence": "Single test job; no --cov-fail-under; no smoke/quality/nightly.",
      "fix_hint": "Add smoke step; add --cov-fail-under=(current-2); document 3-tier strategy."
    },
    {
      "id": "SEC-001",
      "title": "Pin GitHub Actions to SHA; add pip-audit",
      "category": "security",
      "path": ".github/workflows/on_pull_request.yaml:14",
      "severity": "medium",
      "priority": "medium",
      "effort": "low",
      "impact": 4,
      "confidence": 1.0,
      "evidence": "Actions use @v4/@v5; no pip-audit or npm audit in CI.",
      "fix_hint": "Replace with actions/checkout@<sha> etc.; add pip install pip-audit && pip-audit."
    },
    {
      "id": "DOC-001",
      "title": "Add CONTRIBUTING and extension API contract",
      "category": "docs",
      "path": "README.md",
      "severity": "low",
      "priority": "high",
      "effort": "low",
      "impact": 3,
      "confidence": 1.0,
      "evidence": "No CONTRIBUTING.md; extension API is code-only, no version.",
      "fix_hint": "Create CONTRIBUTING.md; add EXTENSION_API_VERSION and callback/script doc."
    },
    {
      "id": "EXT-001",
      "title": "Version and document extension callback API",
      "category": "extensions",
      "path": "modules/script_callbacks.py:219-243",
      "severity": "medium",
      "priority": "medium",
      "effort": "medium",
      "impact": 4,
      "confidence": 0.9,
      "evidence": "callback_map and param types exist but are not versioned or documented as contract.",
      "fix_hint": "Add EXTENSION_API_VERSION; publish minimal doc of callbacks and params; deprecation policy."
    }
  ],
  "scores": {
    "architecture": 2.5,
    "modularity": 2,
    "code_health": 2.5,
    "tests_ci": 2,
    "security": 2,
    "performance": 3,
    "dx": 2,
    "docs": 2,
    "extensions": 2.5,
    "overall_weighted": 2.4
  },
  "phases": [
    {
      "name": "Phase 0 — Fix-First & Stabilize",
      "milestones": [
        {
          "id": "P0-1",
          "milestone": "Add smoke test and pin actions to SHA",
          "acceptance": ["Smoke step runs and is required", "Checkout/setup-python use full SHA"],
          "risk": "low",
          "rollback": "Revert workflow",
          "est_hours": 1
        },
        {
          "id": "P0-2",
          "milestone": "Add pip-audit and artifact upload on fail",
          "acceptance": ["pip-audit runs in CI", "Artifacts uploaded when job fails"],
          "risk": "low",
          "rollback": "Remove step",
          "est_hours": 0.5
        }
      ]
    },
    {
      "name": "Phase 1 — Document & Guardrail",
      "milestones": [
        {
          "id": "P1-1",
          "milestone": "CONTRIBUTING.md and pytest markers",
          "acceptance": ["CONTRIBUTING exists", "pytest -m smoke runs subset"],
          "risk": "low",
          "rollback": "Revert",
          "est_hours": 1
        },
        {
          "id": "P1-2",
          "milestone": "Commit package-lock and npm ci",
          "acceptance": ["package-lock.json in repo", "CI uses npm ci"],
          "risk": "low",
          "rollback": "Revert commit and workflow",
          "est_hours": 0.5
        }
      ]
    },
    {
      "name": "Phase 2 — Harden & Enforce",
      "milestones": [
        {
          "id": "P2-1",
          "milestone": "Coverage threshold with 2% margin",
          "acceptance": ["CI fails if coverage below threshold"],
          "risk": "medium",
          "rollback": "Remove --cov-fail-under",
          "est_hours": 1
        }
      ]
    }
  ],
  "dependency_graph": {
    "hub_modules": ["shared", "paths_internal", "processing", "script_callbacks", "options", "ui_components", "sd_samplers", "sd_models", "infotext_utils", "images"],
    "cycles": [],
    "top_imported_modules": ["shared", "paths_internal", "processing", "options", "script_callbacks", "ui_components", "sd_samplers", "sd_models", "infotext_utils", "images", "scripts", "shared_cmd_options", "sd_hijack", "errors", "devices", "extensions", "paths", "upscaler", "util", "sd_vae"]
  },
  "global_state": {
    "variables": ["cmd_opts", "opts", "state", "sd_model", "device", "demo", "hypernetworks", "loaded_hypernetworks", "sd_upscalers", "face_restorers", "prompt_styles", "interrogator", "total_tqdm", "mem_mon"],
    "writers": ["shared_init.py (opts, state)", "processing.py (opts override, state fields)", "options (opts)", "sd_models (sd_model)", "ui.py (demo)", "progress/call_queue (state)"],
    "readers": "Most of modules/ (shared.opts, shared.state, shared.sd_model)"
  },
  "largest_files": [
    {"path": "modules/processing.py", "loc": 1793},
    {"path": "modules/models/diffusion/ddpm_edit.py", "loc": 1236},
    {"path": "modules/ui.py", "loc": 984},
    {"path": "modules/scripts.py", "loc": 790},
    {"path": "modules/api/api.py", "loc": 750}
  ],
  "complexity_hotspots": [
    {"name": "process_images_inner", "file": "modules/processing.py", "rough_complexity": "high"},
    {"name": "StableDiffusionProcessingTxt2Img.sample / sample_hr_pass", "file": "modules/processing.py", "rough_complexity": "high"},
    {"name": "create_ui", "file": "modules/ui.py", "rough_complexity": "high"},
    {"name": "text2imgapi / img2imgapi", "file": "modules/api/api.py", "rough_complexity": "medium"}
  ],
  "metadata": {
    "repo": "AUTOMATIC1111/stable-diffusion-webui",
    "commit": "82a973c04367123ae98bd9abdf80d9eda9b910e2",
    "languages": ["py", "js"],
    "workspace_path": "c:\\coding\\refactoring\\serena"
  }
}
```

---

## 18. Top 10 Highest-Leverage Refactor Targets

| Rank | Target | What it unlocks | Track |
|------|--------|------------------|-------|
| 1 | **Introduce opts_snapshot and pass into process_images_inner** | Deterministic runs; testable pipeline; first step to runtime layer | Strategic |
| 2 | **Add ProcessingRunner (or Txt2ImgRunner/Img2ImgRunner)** | Single entry for API and UI; swap implementation later without touching callers | Strategic |
| 3 | **3-tier CI + coverage gate** | Fast feedback; coverage regression guard; foundation for all other work | Iterative |
| 4 | **Pin CI actions to SHA + pip-audit** | Reproducibility and supply-chain safety; low effort | Iterative |
| 5 | **CONTRIBUTING.md + extension API version doc** | Onboarding and extension stability; unblocks contributors | Iterative |
| 6 | **Model provider interface** | Unit-test runtime with mock model; decouple from shared.sd_model | Strategic |
| 7 | **temporary_opts context manager in process_images** | Clean override/restore; smaller blast radius than full snapshot | Iterative |
| 8 | **Extract prepare_prompts_and_seeds** | Smaller process_images_inner; clearer seam for future runtime extraction | Iterative |
| 9 | **UI tab registry** | Modular UI; load tabs on demand; easier to add/remove features | Strategic |
| 10 | **Extension callback contract + deprecation policy** | Safe evolution of script_callbacks; fewer breaking changes for extensions | Iterative |

---

*End of pre-refactor audit. All sections completed. Use this document as the basis for a 5/5 refactor plan.*

