# Serena: Audit-First AI-Augmented Refactoring of a Monolithic AI WebUI into a Governed Inference Runtime

**Status:** Publication draft **v2** — tightened for external readers; case-study arc **M00–M33**.  
**Audience:** Senior engineers, engineering managers, CTOs, AI infrastructure practitioners, architecture readers.

---

## Abstract

Maintaining a popular open-source AI web UI strains three fronts: **global state** every feature touches, **extension hooks** that expect stability, and **CI** that is expensive to make honest when real inference dominates cost and flake budgets. **Serena** documents a governed, milestone-bounded refactor of a **stable-diffusion-webui** fork from an audited **2.4/5** baseline to **4.5/5** at **M33**—**release-lock** in a **governance** sense, not a contest over prettier samples. The method is **audit-first**: declare invariants and **non-claims** early; introduce **runtime seams** before extractions; route generation through **`ProcessingRunner`**; move orchestration into **`modules/runtime/`** behind **`ModelProvider`**; and make CI failures blocking only when the program will remediate or **defer** with CVE-level documentation. Readers should expect **architecture description and governance evidence**, not aesthetic benchmarks or pixel-level equivalence. The paper’s spine is **M00–M33**; phases through **M41** are **subsequent work** only [Source: `docs/serena.md`, Phase IX; `docs/serenafinalaudit.md`].

---

## Executive Summary

- **Baseline:** Serena began from **2.4/5** on the frozen upstream snapshot in the pre-refactor audit [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serena.md`, §2].
- **M33 endpoint (core case study):** The **M00–M33** arc closed at **4.5/5** in the post-refactor audit (`Serena v1.0` at M33) [Source: `docs/serenav1audit.md`, §1]. This is the **primary scored endpoint**; **4.8/5** after **M41** is **subsequent work** only—see **§7** and **§8**.
- **Method:** Milestone-bounded, **behavior-preserving by default**, **invariant-driven** refactoring with evidence-first closeouts [Source: `docs/serena.md`, §1, §5–§6].
- **Architecture result:** **Runtime seams** (opts snapshot, context), **`ProcessingRunner`**, extracted **`modules/runtime/`**, **`ModelProvider`** inversion [Source: `docs/architecture/serena_architecture_lock.md`, §3–§4].
- **Governance result:** Three-tier tests, **pytest-only** coverage policy, locked Quality installs, blocking **`pip-audit`** with **documented** deferrals, and explicit **non-claims** [Source: `docs/architecture/ci_environment_contract.md`; `docs/serenav1audit.md`, §1].
- **Primary lesson:** **AI-augmented** refactoring works best when tools accelerate work **inside** a **governance loop** (milestones, CI, audits, human approval)—not as unconstrained generation. See **§3.5**.

**Provenance:** For M00 ledger date vs later milestones and M33 audit SHA vs release tag, see **Appendix — Provenance and archival hashes**.

---

## 1. Introduction

Large, user-facing AI applications rarely fail because the core model is opaque. They fail because the **product surface**—Gradio components, FastAPI handlers, script callbacks, on-disk conventions—outruns the **architectural story**. A single “generation call” fans out across options (`shared.opts`), latent state (`shared.state`), the loaded checkpoint (`shared.sd_model`), sampler implementations, VAE decode, postprocessing scripts, and extension hooks. When every subsystem imports every other through shared globals, **behavior-preserving** change degrades into “we hope nothing important moved,” because nobody can name the full coupling fan-in.

Refactoring under those conditions is intellectually straightforward and organizationally dangerous. The intellectually straightforward move is to “clean up” modules or rewrite flows in large pull requests. The organizational danger is that you cannot separate **progress** from **drift**: CI may stay green while extensions break subtly, API JSON shapes shift, or generation settings stop round-tripping through saved metadata. For AI apps there is an additional trap: the most truthful tests are also the slowest—full model loads, GPU assumptions, flaky environments—so teams often settle for tests that prove **very little** about the runtime path users actually exercise.

Serena inverts that posture: **behavior-preserving by default** plus **evidence-based closeout** each milestone [Source: `docs/serena.md`, §1–§2]. The thesis—adopted here—is that **AI-augmented coding** is a responsible accelerator only inside a **governance loop**: declared invariants, milestone isolation, CI allowed to fail, **audit scoring**, and **explicit non-claims**.

This paper is not a diffusion tutorial, an image-quality benchmark, or a claim that Serena is **production-proven at scale**. It is a **technical case study**: a WebUI monolith scored **2.4/5** reshaped into a **governed inference runtime** with a testable runner boundary, runtime modules, an extension contract, and three-tier CI, reaching **4.5/5** at **M33** when Phase VII closed as **release-ready** in a **governance** sense—not blanket enterprise certification [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serenav1audit.md`, §1; `docs/serena.md`, M33 narrative].

> **Release-ready (M33) — means / does not mean**  
> **Means:** program and **governance** closeout; **architecture lock** and consolidated **evidence** posture; **explicit deferrals** where policy allows (e.g. CVE-level `pip-audit` documentation).  
> **Does not mean:** enterprise **production certification**; pixel- or semantic-equivalence proofs for all outputs; **zero** residual risk; **universal** extension compatibility without versioning.  
> *Aligned with the ledger M33 paragraph and expanded **non-claims** in **§8** [Source: `docs/serena.md`, M33 paragraph].*

**Scope boundary.** The narrative arc ends at **M33**. The ledger records **M34–M41** (narrower globals, coverage, performance guardrails); cite as **subsequent work**, not the spine [Source: `docs/serena.md`, Phases VIII–IX].

---

## 2. Baseline Audit

The baseline audit at frozen upstream (**SHA** `82a973c04367123ae98bd9abdf80d9eda9b910e2`, tag `baseline-pre-refactor`) supplies the numeric posture and the architectural diagnosis [Source: `docs/serena.md`, §2; `docs/sdwebuirefactoraudit.md`, header].

**Overall score: 2.4 / 5.** Categories include **Architecture 2.5**, **Modularity 2.0**, **Tests & CI 2.0**, **Security 2.0**, **Docs 2.0**; **Performance 3.0** is higher but does not offset governance gaps [Source: `docs/sdwebuirefactoraudit.md`, §1 table].

Critical weaknesses read like Serena’s later todo list: **global state hub** (`shared.opts`, `shared.state`, `shared.sd_model`); **no test tiers or coverage gate**; **god modules** (`processing.py`, `ui.py`, `api/api.py`); **dependency / CI hygiene** (pinning, lockfile, actions); **no CONTRIBUTING / extension API contract** [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serena.md`, §2]. Strengths include clear entrypoints, a single `modules/` package, rich extension callbacks, and **API/UI funneling into `process_images`**—consistency worth preserving deliberately [Source: `docs/sdwebuirefactoraudit.md`, §1 “Strengths”]. **Extensions** at **2.5/5**: later **extension API v1** treats hooks as a **named, versioned, tested** public contract [Source: `docs/sdwebuirefactoraudit.md`, §1 table; `modules/extension_api.py`; `docs/serena.md`, M24].

Architecturally, the baseline is a **monolithic Gradio/FastAPI** app whose runtime is a procedural knot: UI and API both land in `process_images`, which reads global model and options state throughout [Source: `docs/sdwebuirefactoraudit.md`, §2].

**Operational reading of “Tests & CI: 2.0”.** Low trust: non-reproducible installs, no coverage gate, no tiers—the green/red signal cannot separate refactor progress from environmental roulette. Phase I therefore buys **CI truthfulness** before Phase II seams [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serena.md`, M01–M04].

This baseline matters because Serena’s later audits use the **same rubric** (below), making **2.4 → 4.5** a deliberate **comparability** choice rather than narrative rebranding [Source: `docs/serenav1audit.md`, §0; §1].

### 2.1 Scoring rubric (0–5)

Post-refactor audits use a **CodeAuditor-style** scale aligned with the baseline audit: **0** catastrophic (dangerous / unusable); **1** fragile; **2** poor (works, hard to change safely); **3** acceptable; **4** strong (structured, predictable); **5** exemplary (architecture, guardrails, docs, observability) [Source: `docs/serenav1audit.md`, §0]. **Weighted category scores** roll up to an overall; the paper’s headline numbers are the **baseline** table in `sdwebuirefactoraudit.md` and the **M33** table in `serenav1audit.md` [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serenav1audit.md`, §1]. Category names are comparable across both reports so readers can align cells directly.

---

## 3. Method

Serena is **program management for refactors**, not a new model. The unit is a scoped milestone, CI evidence, and an honest deferral log.

### 3.1 Principles and invariants

The ledger states **no silent drift**, **no CI weakening**, preserve extension/API semantics unless a milestone versions a break, and **evidence-first closeout** [Source: `docs/serena.md`, §5]. The **invariant registry** names CLI flags, API JSON, formats, public imports, hooks, generation semantics [Source: `docs/serena.md`, §6]—**backpressure** against “helpful” agent diffs with ambiguous externals.

### 3.2 Milestone mechanics

**M00–M33** repeat: **seam** (scopes, snapshots, context) → **route** through a stable entry → **extract** once the seam validates the cut → **prove** with tests, including **mockable runtime** without a real checkpoint [Source: `docs/serena.md`, Phase II–IV; M20]. CI is structural: **M01–M04** workflows and tiers; later milestones tighten coverage, complexity visibility, supply chain [Source: `docs/serena.md`, M03–M04, M26–M28; `docs/architecture/ci_environment_contract.md`].

### 3.3 Audit scoring as a steering signal

Ledger “Audit Score / Notes” give **qualitative steering**; the comparative anchor is **`serenav1audit.md` at M33** [Source: `docs/serena.md`, §4 table; `docs/serenav1audit.md`, §1]. Interim ledger cells are not treated as independent external audits; the measured arc is **2.4 → 4.5** on comparable tables.

### 3.4 Documentation hierarchy

**Program ledger** leads; **`serena_architecture_lock.md` (M31)** fixes steady-state after Phases I–VI; evidence and per-milestone material follow [Source: `docs/serena.md`, §1; `docs/architecture/serena_architecture_lock.md`, §1–§2]. **`serena_allowed_legacy_surfaces.md`** lists **allowed legacy surfaces**—tolerated coupling that is **not** accidental—not a second source of truth above the lock [Source: `docs/serena.md`, §1; `docs/architecture/serena_allowed_legacy_surfaces.md`, header].

### 3.5 AI-augmented governance (loop and accountability)

**Non-claim:** this paper does **not** assert that AI tools **autonomously** refactored Serena, **guaranteed** correctness, or **replaced** human architecture. **AI-augmented** means editing/search/drafting accelerated **only** inside a **governance loop** bounded by milestone scope, invariants, CI, audit artifacts, **human approval** on PRs and ledger closeouts, and the **non-claims** in **§8** [Source: `docs/serena.md`, §4–§6; `docs/whitepaper/serena_whitepaper_claims_register.md`].

1. **Human** sets objective, scope, invariants (including what must **not** change).  
2. **Tooling / agents** (e.g. Cursor) do **bounded** implementation and docs.  
3. **CI and audits** yield machine- or reviewer-checkable evidence; failures are signals.  
4. **Human** chooses approve, revise, rollback, or **defer** (documented where policy allows).  
5. **Closeout** records proof and seeds the next milestone.

The repository has no full human-vs-agent keystroke log; what **is** evidenced is milestone-governed work—**PRs**, run IDs, contract tests, docs a human-led team can review [Source: `docs/serena.md`, §4]. One green run does not prove “no semantic drift”; the loop makes drift **harder to rationalize** without a trail.

### 3.6 Evidence bundles, doc-only milestones, and release-ready semantics

Not every milestone changes runtime code. **M30–M33** include **documentation-only** closeouts that consolidate proof, lock architecture, and record decisions **without** equating a docs PR with historical CI [Source: `docs/serena.md`, M30–M33]. **Release-ready** at **M33** is **program/governance** closeout, not blanket certification of the upstream WebUI [Source: `docs/serena.md`, M33 paragraph]. The evidence bundle stays **subordinate** to the ledger and lock [Source: `docs/architecture/serena_evidence_bundle.md`, §1–§2; `docs/architecture/serena_architecture_lock.md`, §2].

---

## 4. Architectural Transformation

### 4.1 Baseline monolith versus governed runtime

Before the runner, “runtime” was **`processing.py`** plus scattered sampler/decode calls through globals. After Phase III–IV, traffic still enters `process_images` / `process_images_inner`, but execution is **mediated** by **`ProcessingRunner`**, and inner-loop work lives in **`modules/runtime/`** under a **model access rule**: weights via **`p.model_provider.get_model(p)`**, not direct `shared.sd_model` reads in extracted files [Source: `docs/architecture/serena_architecture_lock.md`, §3–§4; `modules/runtime/runner.py`; `docs/serena.md`, M19–M20].

**Figure 1 — Baseline architecture (schematic).** *Schematic only; not a full call graph.*

```
  UI (Gradio)   ──┐
                  ├──► process_images ──► processing.py (monolith)
  HTTP API   ─────┘         │
                              └──► shared.opts / shared.state / shared.sd_model
                                   (global hub)
```

**Figure 2 — Governed runtime (schematic).** *Schematic only; not a full call graph. Named owners match the architecture lock [Source: `docs/architecture/serena_architecture_lock.md`, §3].*

```
   UI (Gradio)  ──┐
                  ├──► process_images ──► ProcessingRunner.run(request)
  HTTP API ─────────┘                              │
                                                 │ prepare: attach model_provider
                                                 ▼
                                        process_images_inner(p)
                                                 │
                         ┌──────────────────────┼──────────────────────┐
                         ▼                      ▼                      ▼
               processing_runtime        sampler_runtime        decode_runtime
                         │                      │                      │
                         └──────────────────────┴──────────────────────┘
                                       model via ModelProvider
```

### 4.2 ProcessingRunner as the runtime boundary

`ProcessingRunner` exposes **prepare → execute → finalize** with optional hooks and an optional queue seam on **execute** only (default synchronous pass-through) [Source: `modules/runtime/runner.py`, docstring header; `docs/serena.md`, M10–M15]. **Prepare** attaches **`model_provider`** (**M19**) [Source: `modules/runtime/runner.py`, `prepare`; `docs/serena.md`, M19]. **`runtime_metrics`** record execute/total wall time via `perf_counter` [Source: `modules/runtime/runner.py`; `docs/architecture/ci_environment_contract.md`, § Guarantee].

### 4.3 Runtime extraction: seams before big moves

**Phase II:** opts isolation, prompt/seed prep, deterministic **opts snapshot**, snapshot threading for saves, **`RuntimeContext`** on the processing instance [Source: `docs/serena.md`, M05–M09]—**runtime modules** wait until shared reads are scoped.

**Phase IV:** batch, sampler, decode/save/postprocess extracted; **script hook sites and ordering** stay in `processing.py` through **M18** by explicit decision [Source: `docs/architecture/serena_architecture_lock.md`, §3]. The lock forbids silently moving hooks or introducing **direct** `shared.sd_model` reads inside extracted runtime files without a milestone [Source: `docs/architecture/serena_architecture_lock.md`, §4 table]. That table exemplifies **governance as code culture**: not only comments, but **change-control rules** tied to proof references.

### 4.4 ModelProvider and mockable runtime

**ModelProvider** inverts the inner loop: runtime modules must not silently re-globalize; tests inject **`FakeModelProvider`** / **`FakeModel`** [Source: `docs/serena.md`, M19–M20; `docs/serenav1audit.md`, §1 strengths]. This does **not** claim every path is cheap without stubs.

### 4.5 UI composition and extension contract

**Phase V:** tab registry and modular builders preserve extension ordering [Source: `docs/serena.md`, M21–M23]. **Extension API v1:** `EXTENSION_API_VERSION = "1.0"`, **`SUPPORTED_CALLBACKS`** aligned to `script_callbacks.callback_map`, enforced by tests [Source: `modules/extension_api.py`; `docs/serena.md`, M24–M25]; deprecation policy signals future removals [Source: `docs/architecture/extension_api_deprecation_policy.md`; `docs/serena.md`, M25].

### 4.6 Subsequent work only — Phase VIII onward (optional context)

After **M33**, **Phase VIII (M34–M37)** and **Phase IX (M38–M41)** (*subsequent work*) record further context narrowing, coverage, security re-audit, `processing.py` decomposition, warn-first performance tooling [Source: `docs/serena.md`, Phases VIII–IX]. **`serena_allowed_legacy_surfaces.md`** updates across those milestones—**allowed legacy surfaces** as a **living contract**. That period is **continuation**, not proof M33 was incomplete [Source: `docs/architecture/serena_allowed_legacy_surfaces.md`, §2; `docs/serena.md`, M33].

---

## 5. Phase Narrative (M00–M33)

### Phase I — Baseline and guardrails (M00–M04)

**Problem:** No frozen baseline or honest CI makes refactors unobservable. **Changes:** Baseline SHA/tag, smoke paths, action hygiene, tiered tests, coverage/security/repro scaffolding [Source: `docs/serena.md`, Phase I; §4 M00–M04]. **Evidence:** Representative Linter/Smoke/Quality run IDs in the ledger [Source: `docs/serena.md`, §4]. **Deferred:** Early environmental/dependency pain documented [Source: `docs/serena.md`, M00 row].

### Phase II — Runtime seam preparation (M05–M09)

**Problem:** Editing `processing.py` would mix behavior with structure. **Changes:** Opts isolation, prompt/seed prep, snapshot create/consume for saves, runtime context attachment [Source: `docs/serena.md`, M05–M09]. **Evidence:** Quality runs; write-only staging to shrink blast radius [Source: `docs/serena.md`, M07–M09].

### Phase III — Runner and service boundary (M10–M15)

**Problem:** A seam is not yet a contract. **Changes:** `ProcessingRunner` lifecycle, hooks, contract tests for txt2img and API paths, optional queue seam [Source: `docs/serena.md`, M10–M15]. **Evidence:** Tests named in ledger for M13/M14 [Source: `docs/serena.md`, M13–M14].

### Phase IV — Runtime extraction (M16–M20)

**Problem:** Inner loop still monolithic. **Changes:** processing/sampler/decode modules; `ModelProvider`; fake-model tests [Source: `docs/serena.md`, M16–M20]. **Evidence:** Coverage/test counts in ledger; M20 closes Phase IV [Source: `docs/serena.md`, M20].

### Phase V — UI and extension stabilization (M21–M25)

**Problem:** UI/extensions break silently under refactors. **Changes:** Tab registry + modular tabs; extension API v1 + deprecation channel [Source: `docs/serena.md`, M21–M25]. **Evidence:** Contract tests [Source: `docs/serena.md`, M24–M25].

### Phase VI — Hardening and reproducibility (M26–M30)

**Problem:** Measurement must match architectural seriousness. **Changes:** `requirements-ci.txt` + `npm ci` for lint tier; pytest-only coverage gate; Radon; blocking `pip-audit` with deferrals; performance snapshot + runner metrics [Source: `docs/architecture/ci_environment_contract.md`; `docs/serena.md`, M26–M29]. **M30:** evidence bundle [Source: `docs/architecture/serena_evidence_bundle.md`; `docs/serena.md`, M30]. **Evidence:** Quality run **23618918747** cited for M29 posture [Source: `docs/architecture/serena_evidence_bundle.md`, §5].

### Phase VII — Release lock (M31–M33)

**Problem:** Without steady-state docs, contributors “fix” tolerated seams as bugs. **Changes:** **M31** architecture lock + allowed legacy; **M32** evidence synthesis; **M33** program closeout with explicit non-certification language [Source: `docs/architecture/serena_architecture_lock.md`; `docs/serena.md`, M31–M33]. **Evidence:** Doc milestones with PR/check provenance; tag **`v0.0.33-m33`** at **`ebb44177`** [Source: `docs/serena.md`, M33 row]. **Deferred:** `pip-audit` deferrals; **release-ready** ≠ blanket production certification [Source: `docs/serena.md`, M33 paragraph].

### 5.1 Cross-cutting observations

Three patterns recur as **method**, not trivia.

First, **verification milestones** (**M13**, **M14**) add **contract tests** after the runner already routes traffic—guarding **two entrypoints, one forgotten** without a large behavioral rewrite [Source: `docs/serena.md`, M13–M14].

Second, **dependency inversion arrives late but precisely**: **opts snapshots** and **context** first, then **runner**, then **`ModelProvider`**, so inversion lands on the baseline’s concentrated pain—the inner sampling and decode loop [Source: `docs/serena.md`, Phase II–IV].

Third, **hardening** is allowed to be boring: `requirements-ci.txt`, `pip-audit`, `npm ci`, and Radon **visibility** prevent the codebase from outrunning its evidence. The CI contract’s **pytest-only** coverage rule prefers a defensible percentage over a inflated one [Source: `docs/architecture/ci_environment_contract.md`, § “Coverage policy (M27)”].

---

## 6. Verification and Governance

Serena reacts to baseline **Tests & CI: 2.0** [Source: `docs/sdwebuirefactoraudit.md`, §1].

### 6.1 Three-tier tests and CI entrypoints

`pytest.ini` defines **`smoke`**, **`quality`**, **`nightly`**; workflows live under `.github/workflows/` [Source: `pytest.ini`; `docs/serenav1audit.md`, §1]. Intent: fast PR feedback, deeper merge/main signal, a home for slower checks—without one noisy job [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serenav1audit.md`, §1].

| Tier / job | pytest marker | Workflow file(s) | Primary purpose | Typical gate |
| ---------- | ------------- | ----------------- | --------------- | ------------- |
| Smoke | `smoke` | `run_smoke_tests.yaml` | Fast PR signal | PR |
| Quality | `quality` | `run_quality_tests.yaml` | Coverage, `pip-audit`, Radon, deeper tests | merge / main (per contract) |
| Nightly | `nightly` | `run_nightly_tests.yaml` | Slower / broader | scheduled / manual |
| Linter | — | `on_pull_request.yaml` (Ruff, ESLint) | Python/JS style | PR |

The **Nightly** tier is the designated home for slower or broader checks without blocking every PR with full inference-cost workloads; exact schedules and triggers follow the workflow files and `ci_environment_contract.md` [Source: `pytest.ini`; `docs/architecture/ci_environment_contract.md`].

**Known asymmetry:** **Quality** uses committed **`requirements-ci.txt`** (+ CLIP exception discipline). **Smoke** and the **Python linter** job keep the pre–M26-style multi-step install in that era—documented as a possible future alignment [Source: `docs/architecture/ci_environment_contract.md`, § “Python — Smoke / Linter (unchanged in M26)”].

### 6.1b JavaScript lint reproducibility

Committed **`package-lock.json`** and **`npm ci`** on PR lint workflows; **`npm ls`** artifact for supply chain visibility [Source: `docs/architecture/ci_environment_contract.md`, § “JavaScript — Linter job”], addressing baseline lockfile neglect [Source: `docs/sdwebuirefactoraudit.md`, §1].

### 6.2 Coverage honesty (pytest-only)

Coverage gating uses **pytest execution only**—not `coverage run launch.py` inflation [Source: `docs/architecture/ci_environment_contract.md`, § “Coverage policy (M27)”]. Post–M33 audit still cites **~48%** with headroom—the gate does not claim full UI line coverage [Source: `docs/serenav1audit.md`, §1 “Remaining Opportunities”].

### 6.3 Supply-chain enforcement and deferrals

Post-**M28a**, Quality fails on unresolved `pip_audit` unless remediated or **documented** `--ignore-vuln` [Source: `docs/architecture/ci_environment_contract.md`, § “pip-audit policy (Phase VI)”]. Two deferrals (**diskcache**, **pygments**) without installable PyPI fixes at recorded dates [Source: `docs/architecture/ci_environment_contract.md`, § “pip-audit deferrals (M28)”]. **Subsequent work:** **M37** re-check [Source: `docs/serena.md`, M37 note].

### 6.4 Perf evidence vs. perf guarantees

**M00–M33:** **M29** adds `performance_snapshot.txt` and runner timing fields [Source: `docs/architecture/ci_environment_contract.md`, § Guarantee; `docs/serena.md`, M29]. **Subsequent work:** **M41** warn-first regression checks [Source: `docs/serena.md`, Phase IX]. No claim of inference speedups—**observability** and governed workflows only.

### 6.5 Docs as living truth

Evidence bundle and matrix are subordinate to ledger and lock [Source: `docs/architecture/serena_evidence_bundle.md`, §1–§2; `docs/architecture/serena_architecture_lock.md`, §7]. **Caveat:** **`docs/milestones/`** may be **gitignored**—verify run records from ledger, PR host, or exports [Source: `.gitignore`; `docs/whitepaper/serena_whitepaper_research.md`, §1].

### 6.6 Complexity visibility (Radon)

**Radon** on **`modules/`** is **warn-first**: visible complexity without failing Quality, scoped to the refactored surface [Source: `docs/architecture/ci_environment_contract.md`, § “Complexity policy (Phase VI)”].

---

## 7. Results

Scores use the **0–5 scale** in **§2.1** and **`serenav1audit.md` §0–§1**. **4.5 overall** is **strong but not flawless** alongside stated remaining opportunities [Source: `docs/serenav1audit.md`, §0–§1].

The table below reproduces **`docs/serenav1audit.md`** (baseline vs **M33**)—the primary scored outcome for **M00–M33**.

| Dimension | Baseline (pre-refactor audit) | Final (M33 post-refactor audit) | Delta |
| --------- | ----------------------------- | -------------------------------- | ----- |
| Architecture | 2.5 | 4.5 | +2.0 |
| Modularity | 2.0 | 4.5 | +2.5 |
| Code Health | 2.5 | 4.0 | +1.5 |
| Tests & CI | 2.0 | 5.0 | +3.0 |
| Security | 2.0 | 4.5 | +2.5 |
| Performance | 3.0 | 4.0 | +1.0 |
| DX | 2.0 | 4.5 | +2.5 |
| Docs | 2.0 | 5.0 | +3.0 |
| **Overall weighted** | **2.4** | **4.5** | **+2.1** |

[Source: `docs/serenav1audit.md`, §1 table]

Qualitative strengths: three-tier CI, runner boundary, runtime modules + provider injection, versioned extension API, locked CI artifacts [Source: `docs/serenav1audit.md`, §1 “Strengths”].

**Subsequent work (secondary):** A later audit records **4.8/5** after **M41** vs **M37** [Source: `docs/serenafinalaudit.md`, §1; `docs/serena.md`, Phase IX]—continuity, not a redefinition of M33 closure.

---

## 8. Limits and Non-Claims

Serena’s credibility comes from constraints stated as plainly as accomplishments.

**Not claimed:**

- **Better images**—no rubric category for aesthetic quality; no perceptual metrics (explicit **non-claim**).
- **Faster inference by default**—performance scores rose on the rubric; no end-user wall-clock wins unless tied to a benchmark outside core scope.
- **Complete elimination of global state**—**allowed legacy surfaces** in `serena_allowed_legacy_surfaces.md` document remaining `shared` touchpoints [Source: `docs/architecture/serena_allowed_legacy_surfaces.md`].
- **Universal extension compatibility**—compatibility is an invariant unless versioned; breaks need policy machinery [Source: `docs/serena.md`, §5–§6].
- **Zero vulnerabilities**—blocking `pip-audit` pairs with **governed** deferrals [Source: `docs/architecture/ci_environment_contract.md`].
- **Semantic equivalence of all outputs**—CI proves structural/contract properties, not pixel identity on every GPU/checkpoint.
- **Drop-in upstream replacement**—Serena is a **governed fork** with documented boundaries; not total parity with evolving upstream under all extensions.

**Claimed with evidence:**

- **Stronger audit posture** by rubric [Source: `docs/serenav1audit.md`].
- **Runner + runtime boundaries** with provider inversion [Source: `docs/architecture/serena_architecture_lock.md`; `modules/runtime/runner.py`].
- **More truthful CI measurement** than baseline for coverage and supply chain [Source: `docs/architecture/ci_environment_contract.md`; `docs/sdwebuirefactoraudit.md`, §1].

**Release language:** M33 **release-ready** is **program/governance** closeout, **not** blanket production certification [Source: `docs/serena.md`, M33 paragraph].

---

## 9. Lessons Learned

1. **Truthfulness before code movement**—Phase I bought measurement before big extractions; baseline CI was among the worst dimensions [Source: `docs/sdwebuirefactoraudit.md`, §1; `docs/serena.md`, Phase I].
2. **Seams precede extraction**—Phase II enables Phase IV [Source: `docs/serena.md`, M05–M09 vs. M16–M18].
3. **Stable entrypoint over perfect module graph**—`ProcessingRunner` enforces lifecycle, metrics, optional queue [Source: `modules/runtime/runner.py`; `docs/serena.md`, M10–M15].
4. **Small inversion API**—`ModelProvider` unlocks fake-model tests without pretending statelessness [Source: `docs/serena.md`, M19–M20].
5. **Mockability as proof**—without checkpoint-free pipeline skeleton tests, architecture stays GPU-hostage [Source: `docs/serenav1audit.md`, strengths; `docs/serena.md`, M20].
6. **Documentation hierarchy**—the lock budgets drive-by hook or policy edits [Source: `docs/architecture/serena_architecture_lock.md`, §6].
7. **Agents need governance**—milestones, invariants, **non-claims** bound acceleration [Source: `docs/serena.md`, §5–§6; `docs/whitepaper/serena_whitepaper_claims_register.md`].
8. **Deferrals must be named**—documented CVE ignores with recheck discipline beat secret workarounds [Source: `docs/architecture/ci_environment_contract.md`, § “pip-audit deferrals (M28)”]. **Subsequent:** **M37** notes post–M33 [Source: `docs/serena.md`, M37 note].
9. **Doc-only milestones are engineering**—locks and release language share the critical path with code [Source: `docs/serena.md`, M31–M33; `docs/architecture/serena_architecture_lock.md`, §6–§8].

---

## 10. Conclusion

Serena shows a legacy AI web UI reshaped into a **governed inference runtime** without fairy tales about purity or autonomy. The **M00–M33** outcome is **2.4 → 4.5** on one rubric, driven by **runtime seams**, **`ProcessingRunner`**, **runtime modules**, **`ModelProvider`**, **honest CI**, and explicit documentation of **allowed legacy**—including deferrals that stayed deferrals because PyPI lacked fixes [Source: `docs/serenav1audit.md`, §1; `docs/architecture/ci_environment_contract.md`]. The useful generalization for enterprises is not “fork stable-diffusion-webui,” but **audit-first AI-augmented refactoring**: treat invariants, evidence, and **non-claims** as deliverables co-equal with code when the codebase touches model weights and community extensions.

For teams considering a similar program, three closing questions are pragmatic filters. **Can you freeze a baseline** with an audit artifact outsiders can inspect? **Can you make CI fail honestly** before you “improve architecture,” so regressions are visible rather than narrated away? **Can you name what remains deliberately imperfect** (globals, deferrals, hook glue) without rebranding incompleteness as accident? If the answer is no, AI tools only compress the timeline between green builds and silent drift.

**Subsequent work** through **M41** reaches **4.8/5** on a later pass—continuity, not the **M33** thesis [Source: `docs/serenafinalaudit.md`, §1; `docs/serena.md`, Phase IX].

---

## Appendix — Evidence reference key

| ID | Document |
|----|-----------|
| S1 | `docs/serena.md` — program ledger |
| S2 | `docs/sdwebuirefactoraudit.md` — baseline audit |
| S3 | `docs/serenav1audit.md` — M33 audit (**4.5/5** endpoint) |
| S4 | `docs/architecture/serena_architecture_lock.md` — architecture lock |
| S5 | `docs/architecture/ci_environment_contract.md` — CI / supply chain |

---

## Appendix — Research and claim hygiene

- Source inventory, workspace limits (**`docs/milestones/` gitignored**), timelines: `docs/whitepaper/serena_whitepaper_research.md`.
- Claim typing and **non-claims**: `docs/whitepaper/serena_whitepaper_claims_register.md`.

---

## Appendix — Provenance and archival hashes

**M00 “Completed At” in the ledger:** `docs/serena.md` lists **2025-03-07** for **M00** while **M01** onward list **2026-03-08** and later, and the program body is otherwise documented in **March 2026**. That **one-year offset is almost certainly a ledger typo** (expected **2026-03-07**) but **this paper does not rewrite `docs/serena.md`**. The narrative does not depend on the absolute calendar day for M00 [Source: `docs/serena.md`, §4 milestone table].

**M33 post-refactor audit SHA vs release-lock tag:** The annotated tag **`v0.0.33-m33`** points to commit **`ebb44177`** (M33 release-ready program closeout, PR #88). The audit header in **`docs/serenav1audit.md`** cites **`8f65669e`**, which **`git`** shows as a **follow-on documentation commit** (PR #89, M33 provenance) **descended from** **`ebb44177`**. Both commits are **M33-era**; the **4.5/5 table** in `serenav1audit.md` remains the authoritative scored outcome. For archival packaging, keep audit document + ledger/tag together rather than collapsing “audit SHA” and “tag SHA” to one hash [Source: `docs/serenav1audit.md`, header; `docs/serena.md`, M33 row; `git` tag `v0.0.33-m33` at `ebb44177`; descendant `8f65669e` verified locally at publication-polish time].

---

*End of draft.*
