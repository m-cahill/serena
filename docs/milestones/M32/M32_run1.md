# M32 — Evidence / audit closure (run 1)

**Milestone:** M32 — Evidence/audit closure  
**Mode:** Documentation-only; **no** new binding runtime gate (consistent with M30/M31 for doc milestones)  
**Date (UTC):** 2026-03-26

---

## 1. Scope and purpose

M32 **closes the evidence/audit story** for the Serena refactor **body of work** through **M31** by synthesizing—without changing executables or CI policy—what is already established in:

- `docs/serena.md` (ledger)
- `docs/architecture/serena_architecture_lock.md` (locked steady-state architecture)
- `docs/architecture/serena_allowed_legacy_surfaces.md` (tolerated legacy, visible)
- `docs/architecture/serena_evidence_bundle.md`, `serena_evidence_matrix.md` (Phase I–VI proof narrative and phase → proof map)
- Milestone evidence, especially `docs/milestones/M30/M30_run1.md` (M28/M29/`main`/PR **#64** honesty) and `docs/milestones/M31/M31_run1.md` (M31 doc-only provenance)

**M32 does not** substitute documentation for runtime proof. Where proof is **binding**, this record **points to** the ledger, bundle, matrix, and cited runs—principally **M29** Quality **`23618918747`** (coverage, tests, **`pip-audit`**, **`performance_snapshot.txt`**).

---

## 2. Authority stack now in force

| Order | Document |
|-------|----------|
| 1 | `docs/serena.md` — phases, milestones, decisions, ledger rows |
| 2 | `docs/architecture/serena_architecture_lock.md` — **structural** steady state after Phases I–VI |
| 3 | `docs/architecture/serena_evidence_bundle.md` — Phase I–VI proof narrative (subordinate to 1–2 for structure) |
| 4 | Milestone folders `docs/milestones/MNN/`, run records, audits |

**Companion (not above the lock):** `docs/architecture/serena_allowed_legacy_surfaces.md` — tolerated seams vs locked architecture.

---

## 3. What is substantively complete (Phases I–VI through M31)

| Area | Status (per ledger + lock + bundle) |
|------|-------------------------------------|
| **Baseline & CI guardrails** | M00–M04: baseline freeze, smoke/quality/nightly structure, coverage/security entry points (ledger §4, bundle §2). |
| **Runtime seams & runner** | M05–M15: opts/context seams, **`ProcessingRunner`**, lifecycle/hooks, txt2img + API through runner, queue seam (lock §3; ledger milestone notes). |
| **Runtime extraction & testability** | M16–M20: `processing_runtime` / `sampler_runtime` / `decode_runtime`, **`ModelProvider`**, mockable pipeline tests (**M20** Quality **`23333740069`** @ **`9c7e693a`** per matrix). |
| **UI & extensions** | M21–M25: tab registry, modular tabs, extension API v1 + deprecation channel (lock §3; ledger). |
| **Hardening & reproducibility** | M26–M29: locked Quality install, pytest-only coverage policy (**M27**), blocking **`pip-audit`** with **two** documented deferrals (**M28**), performance snapshot + runner metrics (**M29** binding **Quality `23618918747`**). |
| **Evidence publishing** | M30: bundle, matrix, case study summary; **doc-only** (no new runtime gate). |
| **Architecture lock** | M31: **`serena_architecture_lock.md`** + **`serena_allowed_legacy_surfaces.md`**; **doc-only** (**PR #83** merge **`09f1d785`** per ledger / `M31_run1.md`). |

---

## 4. Binding evidence map

### 4.1 Runtime / runner / mockable runtime proof

- **Runner boundary and contracts:** M10–M15 narratives; M13/M14 contract tests (ledger, lock §4).
- **Inner-loop extraction + provider:** M16–M19; runtime modules use **`p.model_provider.get_model(p)`** only (lock §4).
- **Mockable end-to-end inner pipeline without a real model:** **M20** — Quality **`23333740069`**, tag **`v0.0.20-m20`** per ledger/matrix.
- **Orchestration glue outside provider-only modules:** Documented as **tolerated**, not hidden — §5 below and **`serena_allowed_legacy_surfaces.md`**.

### 4.2 UI / extension stability proof

- **UI composition and registry** — M21–M23 (ledger; lock §3).
- **Extension API v1 + deprecation scaffolding** — M24–M25; contract tests (ledger; lock §3–4).

### 4.3 CI / coverage / supply-chain proof

- **Pytest-only coverage gate (≥42%)** — **M27** binding Quality **`23513449859`** (198 pass, 47% pytest-only per matrix/bundle).
- **Blocking `pip-audit`** + governed deferrals (**diskcache**, **pygments**) — **M28**; **no** isolated green Quality on **`main`** for M28 alone; stack proof on **`23618918747`** — see **`M30_run1.md`** §3 and bundle §5–6.
- **Locked install contract** — **`ci_environment_contract.md`**, **M26** Quality **`23467772232`** (bundle/matrix).

### 4.4 Performance / artifact proof

- **Binding:** **M29** Quality **`23618918747`** — **199** pass, **~48%** coverage, **`performance_snapshot.txt`** artifact (keys per **`M29_run1.md`** / **`performance_baseline.md`** per bundle).

---

## 5. Known tolerated legacy

- **Single authoritative list:** `docs/architecture/serena_allowed_legacy_surfaces.md` — e.g. **`shared.sd_model`** / **`processing.py`** orchestration **outside** M19 provider-only runtime modules; **do not** expand legacy seams in M32 beyond what that doc and prior milestone audits already allow.
- **Global hubs** (`shared.opts`, `shared.state`, etc.): Further migration is **milestone-governed**, not M31/M32 cleanup (allowed-legacy doc §3).

---

## 6. Remaining gap to M33

- **M33** is reserved for the **final “release-ready 5/5 close”** named in the ledger—**governance / closeout** framing only in M32; **no** detailed engineering backlog invented here.
- M32 **does not** claim full product release certification; it claims **audit/evidence closure** for the **documented refactor program** through M31, with binding technical proof cited where it **actually** attached (esp. M20, M27, M29, M28 stack on **`23618918747`**).

---

## 7. Verdict

| Question | Answer |
|----------|--------|
| Is Serena **evidence-closed** for the **refactor body of work** as documented? | **Yes**, in the sense that **ledger + lock + bundle + matrix + milestone runs** form a **consistent, auditable** account; **no new** undocumented architecture drift is introduced in M32. |
| What is **M33** for? | **Final release-ready 5/5 close** per Phase VII map — scope to be defined **minimally** in `docs/milestones/M33/M33_plan.md` when scheduled. |
| Do doc-only milestones (M30, M31, M32) add **binding** new runtime proof? | **No** — PR CI for doc milestones remains **hygiene/provenance** where recorded (`M30_run1.md`, `M31_run1.md`). |

---

## 8. PR and merge record

| Item | Value |
|------|--------|
| **PR** | **[#86](https://github.com/m-cahill/serena/pull/86)** — `docs(M32): evidence/audit closure and M33 stubs` |
| **Merge method** | **Squash merge** to `main` |
| **Merged at (GitHub)** | **2026-03-27T00:06:13Z** |
| **Branch** | `m32-evidence-audit-closure` (deleted on merge) |
| **Squash merge commit on `main`** | **`3f6f6a2eadd5b2aa0e79a635af0c98c7e7ee6fd9`** (short **`3f6f6a2e`**) |
| **`main` tip after merge** | **`3f6f6a2e`** (same as squash commit) |
| **Base** | Prior `main` at merge-base **`03a2e6ea`** |
| **Binding CI for M32** | **N/A** — documentation-only milestone; evidence synthesis is not proven by CI below |

### Post-merge workflows on `main` (optional provenance only)

Push of **`3f6f6a2e`** triggered **Linter** and **Quality Tests** on `main`. These are **routine CI after a docs-only merge** — **not** claimed as binding M32 proof; same posture as M30/M31.

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** | **23624248870** | **success** | [view run](https://github.com/m-cahill/serena/actions/runs/23624248870) |
| **Quality Tests** | **23624248875** | **success** | [view run](https://github.com/m-cahill/serena/actions/runs/23624248875) |
