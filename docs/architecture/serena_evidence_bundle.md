# Serena — Evidence bundle (Phase I–VI)

**Purpose:** Single auditable narrative of what the Serena program is, what changed through **M29**, what stayed invariant, and where proof lives. **Runtime behavior is unchanged by this document.**

**Hierarchy:** `docs/serena.md` (ledger) → milestone folders `docs/milestones/MNN/` → this bundle.

---

## 1. Project identity

| Field | Value |
|-------|--------|
| **Program** | Serena — governed, behavior-preserving refactor |
| **Upstream** | [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) |
| **Workspace** | `m-cahill/serena` (fork) |
| **Baseline** | Tag `baseline-pre-refactor` @ audited SHA `82a973c04367123ae98bd9abdf80d9eda9b910e2` |
| **Initial audit (reference)** | ~2.4 / 5 (`docs/sdwebuirefactoraudit.md`) |

**Intent:** Move from a monolithic, globally coupled layout toward clear seams (runner, runtime modules, UI composition, extension API contracts) **without** silent behavior drift — enforced by CI, contracts, and milestone closeouts.

---

## 2. Phase map (completed through M29)

| Phase | Milestones | Primary thrust |
|-------|------------|----------------|
| **I** | M00–M04 | Baseline freeze, CI truthfulness, test architecture, coverage/security guardrails |
| **II** | M05–M09 | Runtime seams: temporary opts, prompt/seed prep, opts snapshot, execution context |
| **III** | M10–M15 | `ProcessingRunner`, lifecycle, hooks, API path, queue seam |
| **IV** | M16–M20 | Extract processing/sampler/decode/runtime; model provider; mockable tests |
| **V** | M21–M25 | UI tab registry, modular tabs, extension API v1, deprecation scaffolding |
| **VI** | M26–M29 | Locked CI manifests, pytest-only coverage policy, Radon visibility, blocking `pip-audit` + remediation, performance snapshot + runner metrics |

**M30** (QA / evidence publishing) consolidates documentation only; it does not change code paths.

---

## 3. Major architectural gains (substantive)

- **Execution boundary:** `ProcessingRunner` with prepare / execute / finalize; txt2img and API paths contract-tested through the runner.
- **Runtime extraction:** Batch orchestration, sampler execution, decode/save/postprocess pipelines moved behind `modules/runtime/*` with explicit `ModelProvider` injection for the inner loop.
- **UI composition:** Top-level tab bodies split into modules; registry-driven assembly preserved.
- **Extension surface:** Versioned callback contract + deprecation channel without changing `callback_map` semantics in-place.
- **CI / supply chain:** Committed Python lockfile for Quality, `npm ci` for lint tier, blocking `pip-audit` with **two** documented deferrals only (**diskcache**, **pygments**) — see `docs/architecture/ci_environment_contract.md`.
- **Coverage policy:** Pytest-only gate (M27) so the percentage reflects test execution, not server startup inflation.
- **Observability:** Runner `runtime_metrics`; DEBUG API timing; `performance_snapshot.txt` on binding Quality **23618918747** (`docs/architecture/performance_baseline.md`).

---

## 4. Invariants preserved (program rules)

From `docs/serena.md` — non-exhaustive:

- No silent behavior drift; document intentional changes.
- No CI weakening (thresholds, audit honesty).
- Extension and API compatibility unless explicitly versioned.
- Evidence-first milestone closeout.

**Invariant registry** (CLI, API JSON, file formats, public modules, extension API, generation semantics) — see ledger §6.

---

## 5. CI / security / coverage / performance evidence

| Area | Binding reference | Notes |
|------|-------------------|--------|
| **Quality (tests + coverage + pip-audit)** | **23618918747** | **199** passed, **~48%** line coverage (pytest), `pip-audit` blocking per M28 policy |
| **M27 coverage methodology** | **23513449859** | **198** passed, **47%** TOTAL pytest-only; **≥42%** gate |
| **M26 determinism** | **23467772232** | **112** passed, **40%** combined (pre–M27 measurement change) |
| **Performance artifact** | `performance_snapshot.txt` | Uploaded on **23618918747**; sample keys in `M29_run1.md` |
| **M28 isolated `main` run** | *None* | M28 + M29 delivered in **PR #64** squash; see `docs/milestones/M30/M30_run1.md` §3 |

---

## 6. Recovery and governance (M28–M29)

- **M28:** Dependency upgrades in controlled batches; Gradio 6 / Pydantic v2 compatibility shims where required; deferrals documented instead of hiding failures.
- **M29:** Instrumentation merged with **#64**; **Quality** on `main` then required **M29.1** (**PR #79**) and **M29.2** (**PR #80**, **#81**) for Gradio/Pydantic/`get_cmd_flags`/runner test alignment. **Binding** green: **23618918747**.

This demonstrates **fix-forward** under blocking gates rather than disabling audits.

---

## 7. What remains (post–M32)

- **M31 (Phase VII):** **Complete** — `docs/architecture/serena_architecture_lock.md`, `serena_allowed_legacy_surfaces.md` (documentation only; see ledger, `M31_run1.md`).
- **M32 (Phase VII):** **Complete** — Evidence/audit closure synthesis (`docs/milestones/M32/M32_run1.md`, `M32_summary.md`, `M32_audit.md`); documentation only; **no** new binding runtime gate (same posture as M30/M31).
- **M33 (Phase VII):** **Pending** — Release-ready 5/5 close (ledger); minimal stub only until planned.

---

## 8. Document index (M30+)

| Document | Role |
|----------|------|
| `docs/serena.md` | Authoritative ledger |
| `docs/architecture/serena_architecture_lock.md` | **M31:** Locked steady-state architecture (structural authority) |
| `docs/architecture/serena_allowed_legacy_surfaces.md` | **M31:** Tolerated legacy glue vs locked architecture |
| `docs/milestones/M30/M30_run1.md` | Cross-check log and M28/M29 CI clarification |
| `docs/milestones/M31/M31_run1.md` | M31 PR provenance; doc-only hygiene posture |
| `docs/milestones/M32/M32_run1.md` | M32 evidence/audit closure; binding evidence map pointers |
| `docs/architecture/serena_case_study_summary.md` | Shorter external-facing summary |
| `docs/architecture/serena_evidence_matrix.md` | Phase → gain → proof |
