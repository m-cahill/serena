# Serena — Architecture lock (M31)

**Status:** Authoritative steady-state architecture after Phases I–VI (through M30).  
**Milestone:** M31 — Architecture lock (documentation only; no runtime or CI behavior change).

---

## 1. Purpose

Serena’s **post-refactor architecture** is considered **locked** as of M31: Phases I–VI delivered the substantive runtime seams, `ProcessingRunner` boundary, extracted runtime modules, UI composition pattern, extension API contract and deprecation channel, and Phase VI hardening (locked CI install, pytest-only coverage, blocking `pip-audit`, performance evidence). M31 records that approved shape in one place so future work can be judged against an explicit baseline.

**After M31, structural or cross-cutting changes that alter the locked boundaries below require an explicit milestone plan** (and ledger update), not drive-by edits.

This document does **not** replace `docs/serena.md`; it specializes **what** the steady-state architecture **is**, while the ledger remains the program’s timeline, decisions, and milestone facts.

---

## 2. Authority order

For **conflicts or ambiguity** about Serena’s architecture after M31, resolve in this order:

1. **`docs/serena.md`** — Program ledger: phases, milestones, invariants, and explicit milestone decisions.
2. **`docs/architecture/serena_architecture_lock.md`** (this file) — Approved **steady-state structure**: execution boundary, runtime modules, UI assembly, extension surface, CI/evidence posture, and locked boundaries.
3. **`docs/architecture/serena_evidence_bundle.md`** — Phase I–VI **proof narrative** (what was proven and where); subordinate to the ledger and this lock for *structural* authority.
4. **Milestone docs, run records, audits** — Per-milestone detail (`docs/milestones/MNN/`), CI run references, audits/summaries.

**Historical baseline audits** (`docs/sdwebuirefactoraudit.md`, `docs/sdwebuiaudit.md`) describe the **pre-refactor** state and strategy; they do **not** override the ledger or this lock for the **current** approved architecture.

---

## 3. Locked architecture summary

Approved operating shape (consumers → core → evidence):

| Concern | Locked shape |
|--------|----------------|
| **Consumers** | UI (`modules/ui*.py` assembly), HTTP API (`modules/api/*`), and queue-capable paths that ultimately call `process_images` / `ProcessingRunner`. |
| **Execution boundary** | **`ProcessingRunner`** (`modules/runtime/runner.py`): prepare → execute → finalize; optional hooks and optional queue wrapper around execute (M10–M15). |
| **Runtime layer** | **`modules/runtime/processing_runtime.py`** (batch orchestration), **`sampler_runtime.py`** (sampler execution), **`decode_runtime.py`** (decode/postprocess/save for the inner loop), **`model_provider.py`** (`ModelProvider` / `SharedModelProvider`) (M16–M19). |
| **UI composition** | **Tab registry** (`modules/ui_tab_registry.py`) + **modular top-level tab builders** (txt2img, img2img, settings, extensions) preserving extension and load order contracts (M21–M23). |
| **Extension surface** | **Versioned callback contract** (`modules/extension_api.py`, `docs/architecture/extension_api_contract_v1.md`) + **deprecation channel** (`modules/deprecation.py`, `script_callbacks.deprecate_callback`, `docs/architecture/extension_api_deprecation_policy.md`) without silent `callback_map` rewrites (M24–M25). |
| **Hardening / evidence** | **Locked Quality Python install** (`requirements-ci.txt` / `requirements-ci.in`, CLIP install rule) per **`docs/architecture/ci_environment_contract.md`**; **pytest-only coverage** gate (M27); **blocking `pip-audit`** with **documented deferrals only** (M28); **Radon** visibility on `modules/` (non-blocking per contract); **runner `runtime_metrics`**, DEBUG API timing, **`performance_snapshot.txt`** on binding Quality (M29). |

**Orchestration and script hooks:** Script hook **call sites** and ordering for the generation pipeline remain in **`modules/processing.py`** as established through M18 (hooks not relocated into runtime modules).

---

## 4. Locked boundaries

| Boundary | Approved owner | What may change internally | What may **not** change without milestone approval | Evidence source |
|----------|----------------|----------------------------|--------------------------------------------------|----------------|
| **Processing entrypoint** | `process_images` / `process_images_inner` as the pipeline orchestrator; delegation into `ProcessingRunner` and runtime modules | Refactors that preserve semantics and hook order; additional logging | Removing or bypassing **`ProcessingRunner`** for primary txt2img/img2img/API paths; changing **observable** generation semantics | M10–M15 ledger; M13/M14 contract tests |
| **Runner lifecycle** | `ProcessingRunner`: prepare / execute / finalize; optional hooks; optional queue | Internal implementation details; instrumentation that preserves order | Reordering lifecycle stages; changing default **no-op** semantics of hooks in a user-visible way | M11–M12 ledger; `test_runner_*` |
| **Runtime orchestration modules** | `processing_runtime`, `sampler_runtime`, `decode_runtime` | Internal factoring within modules; tests | Introducing **direct** `shared.sd_model` / `p.sd_model` reads in these modules (M19 invariant); moving **script hook** invocations into runtime modules without a milestone | M16–M18 ledger; M19 audit |
| **Model access path** | `p.model_provider.get_model(p)` for inner-loop runtime | Provider implementations; test doubles | Bypassing provider for model access **inside** `processing_runtime` / `sampler_runtime` / `decode_runtime` | M19–M20 ledger; `model_provider.py` |
| **Script hook call sites** | `processing.py` (and existing script callback wiring) | Local refactors preserving **order** and names | Moving hook call sites or changing **invocation order** without a milestone | M18 summary; extension policy |
| **UI registry / builders** | `ui_tab_registry` + per-tab modules | Layout refactors preserving registry contract and side-effect order | Breaking **tab registration order** or extension `ui_tabs_callback` semantics without versioning | M21–M23 ledger |
| **Extension callback contract** | `extension_api.py` + `script_callbacks.py` policy blocks | Additive **versioned** changes; deprecations via `deprecate_callback` | Silent edits to **`callback_map`** semantics; removing callbacks without deprecation policy | M24–M25 ledger; contract tests |
| **CI measurement policy** | `ci_environment_contract.md` (pytest-only coverage; no `coverage run launch.py` inflation) | Tightening thresholds if milestone-approved | **Lowering** coverage floor or reverting to misleading **combined** coverage without a milestone | M27 ledger; PR #63 |
| **Security / supply-chain policy** | Blocking **`pip-audit`** on Quality; **`--ignore-vuln`** only for **documented** gaps | Remediating advisories; removing ignores when fixes ship | New **undocumented** audit suppressions; disabling **`pip-audit`** failure on Quality | M28 ledger; `ci_environment_contract.md` |
| **Performance evidence surface** | `performance_snapshot.txt`, runner `runtime_metrics`, documented baselines | Additional metrics if non-breaking | Removing binding **artifact** expectations from agreed **release/audit** milestones without ledger update | M29; `performance_baseline.md` |

---

## 5. Explicitly allowed legacy surfaces

Not every historical global coupling was removed in Phases I–VI. The following are **not** M31 defects: they are **documented, tolerated** seams. Detail and rationale: **`docs/architecture/serena_allowed_legacy_surfaces.md`**.

At minimum (see allowed-legacy doc and M19/M20 evidence):

- **`modules/processing.py`** still coordinates **`shared.sd_model`** for **orchestration and metadata** (e.g. dimensions, checkpoint identity, conditioning paths) outside the provider-only inner-loop runtime modules. **Runtime modules** (`processing_runtime`, `sampler_runtime`, `decode_runtime`) do **not** read `shared.sd_model` / `p.sd_model` directly; **`SharedModelProvider`** centralizes global access for **`get_model`**. Tests align **`shared.sd_model`** with the provider return for **`process_images_inner`** metadata (M20 audit).

---

## 6. Change-control rules after lock

The following require an **explicit milestone** (plan + ledger entry) before implementation:

- Moving **script hook** call sites or changing **hook order**.
- Bypassing **`ProcessingRunner`** for primary generation entrypoints (UI/API/queue).
- Changing **extension callback** semantics, **`SUPPORTED_CALLBACKS`**, or deprecation policy without versioning.
- Changing **coverage measurement method** (e.g. non–pytest-only gate) or **lowering** quality gates.
- Changing **pip-audit** enforcement or adding **non-documented** vulnerability ignores.
- Introducing **new direct global model reads** inside **`modules/runtime/processing_runtime.py`**, **`sampler_runtime.py`**, or **`decode_runtime.py`** (reaffirming M19).
- Substantial **CI install contract** changes (`requirements-ci.txt` generation rules, CLIP install exception, `npm ci` policy for lint).

Cosmetic doc edits, typo fixes, and cross-links that **do not** change the above may proceed under normal contribution hygiene.

---

## 7. Proof references

| Anchor | Role |
|--------|------|
| **Phases I–VI** | Milestone narratives and scores in **`docs/serena.md`** (§3–§4, milestone notes). |
| **Evidence bundle** | **`docs/architecture/serena_evidence_bundle.md`** — consolidated Phase I–VI narrative. |
| **Evidence matrix** | **`docs/architecture/serena_evidence_matrix.md`** — phase → gain → proof. |
| **Case study summary** | **`docs/architecture/serena_case_study_summary.md`** — external-facing summary. |
| **M30 run record** | **`docs/milestones/M30/M30_run1.md`** — CI cross-checks, M28/M29/`main` Quality history honesty. |
| **Ledger rows (architectural anchors)** | **M20** — mockable runtime proof; **M25** — extension deprecation scaffolding; **M29** — performance evidence; **M30** — evidence publishing / QA docs only. |
| **CI contract** | **`docs/architecture/ci_environment_contract.md`** — install, coverage, pip-audit, Radon. |
| **Extension docs** | **`docs/architecture/extension_api_contract_v1.md`**, **`extension_api_deprecation_policy.md`**. |

---

## 8. M31 verification note

M31 is **documentation-only**. Verification is by **consistency** with the ledger and evidence docs and by **diff inspection** (no changes to application code, workflows, or dependency manifests). **PR checks** on an M31 PR are **hygiene/provenance** only, not a substitute for runtime proof of architecture (same posture as M30 for doc-only milestones).
