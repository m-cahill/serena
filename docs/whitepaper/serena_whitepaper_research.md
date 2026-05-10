# Serena White Paper — Research Notes

Research scope for the case-study arc **M00–M33** (Phase I through Phase VII release lock). **M34+** and **M41** are out of scope for deep narrative except a short “subsequent work” pointer where the ledger or post-M33 audits reference them.

---

## 1. Source Inventory

### Files explicitly reviewed

| Path | Contribution | Key evidence extracted | Limitations / uncertainties |
|------|----------------|------------------------|---------------------------|
| `docs/serena.md` | Authoritative program ledger: phases, milestone map, per-milestone notes, invariant registry, baseline SHA/tag, CI run references | Baseline **2.4/5**; phase map M00–M33; detailed M05–M41 narrative blocks; `ProcessingRunner`, runtime extraction, extension API, CI tiers; source-of-truth hierarchy | M00 **Completed At** **2025-03-07** vs **2026-03-08** for M01+ — **publication polish** treats as **likely one-year typo** (expected **2026-03-07**); ledger not rewritten here (`docs/serena.md` §4) |
| `docs/sdwebuirefactoraudit.md` | Pre-refactor audit at baseline SHA | **Overall 2.4/5**; category scores; global `shared.*` hub; god modules (`processing.py`, `ui.py`, `api.py`); weak test tiers; dependency/CI hygiene | Describes **upstream** repo name; workspace path in file is this fork — audit is baseline snapshot |
| `docs/serenav1audit.md` | Post-refactor audit at **M33** | **Overall 4.5/5**; per-category table vs pre-refactor; strengths list (3-tier CI, runner, runtime modules, extension API, locked CI); remaining opportunities (legacy glue, pip-audit deferrals, ~48% coverage) | **Publication polish:** header SHA **`8f65669e`** vs tag **`v0.0.33-m33`** @ **`ebb44177`** — verified **ancestor/descendant** on `main`; use **scored table** + ledger/tag jointly; do not equate commit IDs [Source: `docs/serenav1audit.md`; `docs/serena.md` M33; local `git`] |
| `docs/serenafinalaudit.md` | Latest scored audit (program continuation) | **4.8/5** at M41; progression M33 **4.5** → M37 **4.6** → M41 **4.8**; documents **outside** M00–M33 arc | Used **only** for optional “subsequent work” scoring context, not as end-state for core paper |
| `docs/architecture/serena_architecture_lock.md` | M31 steady-state lock | Locked boundaries table; authority order; `ProcessingRunner`, runtime modules, UI composition, extension contract, CI policies | Doc-only milestone; proof references point to milestone folders |
| `docs/architecture/serena_allowed_legacy_surfaces.md` | Tolerated globals / glue after lock | `_orchestration_model` / `model_provider` (M35); `_eff_opts` / snapshot-first opts (M39); runtime modules must not read `shared.sd_model` directly | Post-M33 updates (M35, M39) noted in doc — **transparent** for “deferred” section |
| `docs/architecture/serena_evidence_bundle.md` | Phase I–VI proof narrative through M29 | Phase table; architectural gains; CI binding refs (e.g. Quality **23618918747**); invariant summary | Says hierarchy includes `docs/milestones/MNN/` — see below |
| `docs/architecture/serena_evidence_matrix.md` | Phase → gain → proof (not fully re-read line-by-line) | Cited by lock and bundle as index | **Not** deep-read in this session — secondary |
| `docs/architecture/serena_case_study_summary.md` | External-facing summary | Cross-check against overclaiming | Secondary |
| `docs/architecture/ci_environment_contract.md` | Quality/Smoke/Nightly policy | `requirements-ci.txt`; CLIP install exception; **M28+** blocking `pip-audit`; deferrals **CVE-2025-69872**, **CVE-2026-4539**; pytest-only coverage **≥42%**; M41 performance regression **warn-first** | Smoke/Linter still use older install path per §4 — asymmetry documented |
| `docs/architecture/extension_api_contract_v1.md` | Extension API v1 | Versioned callback surface | Secondary lock details |
| `docs/architecture/extension_api_deprecation_policy.md` | Deprecation channel | Pairs with M25 | Secondary |
| `docs/architecture/performance_baseline.md` | Performance evidence | M29 snapshot / metrics narrative | Referenced in contract |
| `modules/runtime/runner.py` | Runner implementation | `ProcessingRunner` lifecycle; `model_provider` injection; `runtime_metrics` | Source confirms ledger claims |
| `modules/extension_api.py` | Extension contract constants | `EXTENSION_API_VERSION = "1.0"`; `SUPPORTED_CALLBACKS` tuple | Mechanical evidence for M24 |
| `.github/workflows/run_quality_tests.yaml` | Quality tier | (Partial) — contract doc is primary for behavior | Full YAML not line-audited this session |
| `.github/workflows/run_smoke_tests.yaml` | Smoke tier | Markers / gating pattern per `pytest.ini` | Partial |
| `.github/workflows/run_nightly_tests.yaml` | Nightly tier | M41 pip-audit alignment per `ci_environment_contract.md` | Partial |
| `.github/workflows/on_pull_request.yaml` | Linter / PR path | `npm ci` / ESLint per contract | Partial |
| `pytest.ini` | Test markers | `smoke`, `quality`, `nightly`; `testpaths = test` | Confirms 3-tier vocabulary |
| `.gitignore` | Workspace constraint | Line **`/docs/milestones/`** — milestone tree **not present** in a default clone | Per-milestone `MNN_run1.md` etc. **cannot** be quoted from disk here; ledger + architecture + audits carry milestone facts |

### Not reviewed (time / relevance)

- `modules/processing.py` full file (structure described in audits and lock)
- `requirements-ci.txt` line-by-line pin proof
- `test/quality/test_runtime_mock.py` and full `test/` tree

---

## 2. Timeline (M00–M33)

Derived primarily from **`docs/serena.md`** §3 phase map, §4 milestone ledger table, and phase completion paragraphs.

| Phase | Milestone range | Date range (from ledger) | Primary objective | Key architectural / governance result | Verification evidence (as recorded) |
|-------|-----------------|--------------------------|-------------------|--------------------------------------|-------------------------------------|
| **I — Baseline & Guardrails** | M00–M04 | M00: *2025-03-07* (see uncertainty); M01–M04: **2026-03-08** – **2026-03-09** | Baseline freeze, honest CI, CONTRIBUTING, smoke/quality/nightly, coverage/security guardrails | Action SHA pinning, smoke path, test architecture, **≥** coverage gate introduced | Ledger: Linter/Tests/Smoke/Quality run IDs per row |
| **II — Runtime Seam Preparation** | M05–M09 | **2026-03-10** – **2026-03-12** | Isolate opts / prompt / snapshot / execution context | `temporary_opts`, `prompt_seed_prep`, `opts_snapshot`, `RuntimeContext` | Quality run IDs; ledger narrative §M05–M09 |
| **III — Runner & Service Boundary** | M10–M15 | **2026-03-12** – **2026-03-18** | `ProcessingRunner`, lifecycle, hooks, txt2img/API contract tests, queue seam | Single execution boundary; prepare/execute/finalize; optional queue | `test_txt2img_path_uses_runner`, `test_api_txt2img_uses_runner` per ledger |
| **IV — Runtime Extraction** | M16–M20 | **2026-03-19** – **2026-03-20** | Extract processing/sampler/decode; `ModelProvider`; fake model tests | `processing_runtime`, `sampler_runtime`, `decode_runtime`, `model_provider.py`; **FakeModel** tests | Ledger M16–M20; Quality coverage stepping 40% → 40% |
| **V — UI & Extension Stabilization** | M21–M25 | **2026-03-20** – **2026-03-23** | Tab registry, modular tabs, extension API v1, deprecation | `ui_tab_registry`, `ui_*_tab.py`, `extension_api.py`, `deprecation.py` | Contract tests per ledger |
| **VI — Hardening & Reproducibility** | M26–M30 | **2026-03-23** – **2026-03-26** | Locked `requirements-ci.txt`, pytest-only coverage, blocking `pip-audit`, Radon, performance snapshot | **`ci_environment_contract.md`**; M28 deferrals documented; `performance_snapshot.txt` | Binding Quality **23618918747** (M29); M30 doc-only evidence bundle |
| **VII — Release Lock** | M31–M33 | **2026-03-26** – **2026-03-27** | Architecture lock, evidence closure, release-ready governance closeout | **`serena_architecture_lock.md`**, **`serena_allowed_legacy_surfaces.md`**; tag **`v0.0.33-m33`** @ **`ebb44177`** | Doc-only milestones; **`docs/serenav1audit.md`** @ M33 **4.5/5** |

**Pattern (recurring):** plan → implementation PR(s) → CI run reference(s) → summary/audit language in ledger or architecture docs → explicit “deferred” or “allowed legacy” where scope ends.

**M00 date note:** The ledger’s **2025-03-07** for M00 is **inconsistent** with the rest of the March **2026** program timeline; treat as **likely typo** in `docs/serena.md` **without** rewriting the ledger in this documentation pass.

---

## 3. Before State

From **`docs/sdwebuirefactoraudit.md`** and **`docs/serena.md`** §2.

- **Monolithic WebUI:** Single Gradio/FastAPI application; **`modules/`** package as procedural hub; **`launch.py`** / **`webui.py`** entrypoints (audit §2).
- **`shared` global state:** **`shared.opts`**, **`shared.state`**, **`shared.sd_model`** widely read/written; hurts testability (audit §1, §2).
- **`processing.py` / `ui.py` / `api.py` coupling:** Large modules; UI and API both call into **`process_images`**; tight coupling via `shared` (audit §1; ledger §2 “Top architectural problems”).
- **CI / test weakness:** No smoke/quality/nightly tiers; no coverage fail-under; single-job pattern in baseline audit (audit §1); mixed pinning; **`package-lock.json`** gitignored upstream-style; actions tags not SHA (audit §1).
- **Supply-chain weakness:** Mixed **`requirements.txt`** pinning; npm not reproducible from lockfile in baseline narrative.
- **Extension API risk:** No formal versioned contract or CONTRIBUTING for stability (audit §1).
- **Baseline audit score:** **2.4 / 5** overall (`docs/sdwebuirefactoraudit.md` §1; `docs/serena.md` §2).

---

## 4. After State (end of M00–M33 arc)

From **`docs/serenav1audit.md`**, **`docs/architecture/serena_architecture_lock.md`**, and **`docs/serena.md`** Phase IV–VII summaries.

- **`ProcessingRunner` boundary:** prepare → execute → finalize; hooks; optional queue; **`model_provider`** injection at prepare (`modules/runtime/runner.py`; lock §3).
- **Runtime modules:** `processing_runtime`, `sampler_runtime`, `decode_runtime`, `model_provider` — inner loop model access via **`get_model(p)`** only (lock §3–4).
- **`ModelProvider` abstraction:** Dependency inversion for runtime modules; **`SharedModelProvider`** default preserves global-load semantics (lock §3; allowed-legacy doc).
- **Mockable runtime:** **`FakeModel` / `FakeModelProvider`** and Quality tests — ledger M20; serenav1audit cites mockable proof as strength area.
- **UI modularization:** Tab registry + per-tab modules; order and extension callbacks preserved (lock §3; ledger M21–M23).
- **Extension API contract:** **`EXTENSION_API_VERSION`**, **`SUPPORTED_CALLBACKS`**, contract tests, deprecation policy docs (lock §3; `modules/extension_api.py`).
- **3-tier CI:** Smoke, Quality, Nightly — **`pytest.ini`** markers; workflows exist; serenav1audit §1.
- **Security / supply-chain hardening:** Committed **`requirements-ci.txt`**, **`package-lock.json`**, blocking **`pip-audit`** with **documented** ignores only ( **`ci_environment_contract.md`** ).
- **Evidence artifacts:** `pip_audit_report.txt`, coverage XML/HTML, Radon artifact, **`performance_snapshot.txt`** (post-M29, still part of governance story by M33).
- **Post-refactor audit score at M33:** **4.5 / 5** overall (`docs/serenav1audit.md` §1).

---

## 5. Open / Deferred Items (transparent constraints)

**As of M33 and architecture lock language (with later doc updates noted):**

- **`processing.py` legacy glue:** Still orchestrates pipeline and **script hook call sites**; not replaced by runtime modules (lock §3 “Orchestration and script hooks”; allowed-legacy §2).
- **`shared.sd_model` coordination:** Narrowed post-M35 in **`serena_allowed_legacy_surfaces.md`** — **`_orchestration_model`**, compatibility property, fallback when no provider; **not** same as “eliminated.”
- **`shared.opts` after snapshot:** **`_eff_opts(p)`** snapshot-first with fallback (M39); further migration milestone-governed.
- **pip-audit deferrals:** **diskcache** / **pygments** CVEs — no PyPI fix at M37 recheck per **`ci_environment_contract.md`**; **governed `--ignore-vuln`**.
- **Coverage headroom:** ~**48%** pytest-only with **≥42%** gate — serenav1audit “Remaining Opportunities.”
- **Allowed legacy surfaces:** Explicit list in **`serena_allowed_legacy_surfaces.md`**; not exhaustive beyond cited program docs (“do not invent”).
- **`docs/milestones/` unavailable locally:** This clone **gitignores** **`/docs/milestones/`** — some evidence lines in audits reference **`M37_run1.md`** etc.; cannot verify those files on disk here.

---

## 6. Subsequent work (out of core arc — pointer only)

Per user direction: **M34–M37** (Phase VIII) and **M38–M41** (Phase IX) may be mentioned briefly. **`docs/serena.md`** records Phase VIII–IX completion; **`docs/serenafinalaudit.md`** gives **4.8/5** after M41. The **white paper’s primary “final” score for the transformation narrative** should remain **4.5/5 at M33** unless the paper explicitly frames later audits as continuation.

---

*End of research notes.*
