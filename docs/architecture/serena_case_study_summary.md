# Serena — Case study summary

**Audience:** Technical readers, senior engineers, architects, and technically literate reviewers evaluating how a large open-source UI codebase can be refactored under discipline.

**What this is:** A factual summary of the **Serena** program — a milestone-governed refactor of **AUTOMATIC1111/stable-diffusion-webui** in a fork (**m-cahill/serena**). It is not a product pitch.

---

## The problem

The upstream project accumulated **tight coupling** (global `shared.*` state), **very large modules**, and **limited automated verification**. Refactors without guardrails risk silent regressions, especially where **extensions** and a **JSON API** depend on stable behavior.

---

## The method

Serena uses **small milestones**, each with a clear scope, **documented evidence** (CI runs, audits), and a **ledger** (`docs/serena.md`) that records commits, branches, and binding workflow runs where applicable.

Core rules:

- **Preserve behavior** unless a milestone explicitly changes it.
- **Do not weaken CI** to “get green”; when measurement was misleading (e.g. combined coverage), the **policy** was fixed explicitly (M27).
- **Security and supply chain:** move from informational `pip-audit` to **blocking** enforcement (M28), with **documented** exceptions only where PyPI offers no fix.

---

## What changed (high level)

Across **Phase I–VI** (through **M29**), the codebase gained:

- A **runner boundary** around generation (`ProcessingRunner`) with lifecycle and optional hooks.
- **Extracted runtime** modules (batch orchestration, sampler execution, decode/save) and **dependency injection** for the model in the inner loop (`ModelProvider`).
- **Modular UI** construction (tab registry and per-tab modules) while preserving extension hook order where required.
- A **versioned extension API** surface and a **deprecation** path that does not silently rewrite callback registration.
- **Reproducible CI installs** (locked Python manifest, pinned CLIP install path, `npm ci`), **pytest-only coverage** gating, **Radon** visibility, **blocking `pip-audit`**, and **performance snapshots** from CI (`performance_snapshot.txt` on binding Quality **23618918747**).

---

## What stayed the same

- **Intent** of generation parameters and public API contracts unless a milestone documented an intentional adjustment (e.g. compatibility shims for upgraded dependencies).
- **Extension ecosystem expectations** — addressed through explicit API versioning and tests, not ad hoc edits to loading order.
- **Honest CI:** failures were addressed with fixes or documented deferrals, not by turning off gates.

---

## Measurable outcomes (examples)

- **Audit scores** on completed milestones are recorded in the ledger (typically **5.0 / 5** from M03 onward in the documented closeouts).
- **Coverage gate:** **≥42%** on pytest-only measurement post–M27 (**23513449859** established methodology; **23618918747** shows **~48%** on the binding stack).
- **Security:** blocking `pip-audit` with **two** governed deferrals at M28 closeout (**diskcache**, **pygments**) — see `docs/architecture/ci_environment_contract.md`.

---

## Why this is a strong refactor case study

1. **Traceability:** Decisions tie back to **commits, PRs, and CI run IDs** in the ledger and milestone docs.
2. **Honesty about recovery:** **M29** required follow-up PRs (**#79–#81**) after dependency and UI stack upgrades; the program documented failing runs and fixes rather than rewriting history.
3. **Separation of concerns:** Technical work (runtime/UI/API) is paired with **governance** (coverage policy, audit policy, evidence publishing).

---

## Limits of this summary

- It does not replace **`docs/serena.md`** or per-milestone **`MNN_run1.md`** files for audit detail.
- **M28** did not produce a standalone green **Quality** run on `main` by itself; it shipped with **M29** in **PR #64** — see `docs/milestones/M30/M30_run1.md` §3.

---

## Where to read next

| Document | Purpose |
|----------|---------|
| `docs/serena.md` | Full ledger and milestone table |
| `docs/architecture/serena_evidence_bundle.md` | Internal evidence bundle |
| `docs/architecture/serena_evidence_matrix.md` | Phase → gain → proof matrix |
