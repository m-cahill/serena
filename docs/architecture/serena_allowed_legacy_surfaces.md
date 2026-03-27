# Serena — Allowed legacy surfaces

**Purpose:** List **tolerated** global and orchestration glue that remain **after** the M31 architecture lock so future work does not treat them as accidental bugs to “clean up” without a milestone.

**Relation to the lock:** **`docs/architecture/serena_architecture_lock.md`** defines the **locked** steady-state architecture. **This document** lists **known, allowed** deviations from a fully pure “no globals” design—by explicit program scope, not by oversight.

---

## 1. Locked vs tolerated (distinction)

| Concept | Meaning |
|---------|--------|
| **Locked architecture** | `ProcessingRunner` boundary; runtime modules using **`ModelProvider`** only for model access; extracted decode/sampler/processing runtime; UI registry + modular tabs; versioned extension API + deprecation channel; CI policies in **`ci_environment_contract.md`**. |
| **Tolerated legacy seams** | Remaining **`shared.*`** and **`processing.py`** orchestration paths that were **out of scope** for Phases IV–VI or explicitly documented as glue in milestone evidence. |

---

## 2. Remaining global-state touchpoints (documented)

### 2.1 `shared.sd_model` in `process_images` / `process_images_inner` orchestration (narrowed, M35)

**What (current):** **`modules/processing.py`** supported-path orchestration uses **`_orchestration_model(p)`**, which returns **`p.model_provider.get_model(p)`** when the runner has prepared the request (default **`SharedModelProvider`** still delegates to **`shared.sd_model`**). **Direct** reads of **`shared.sd_model`** in **`processing.py`** are limited to:

- the **`StableDiffusionProcessing.sd_model`** **compatibility property** (extensions / legacy callers; **not** the internal orchestration authority), and
- the **`_orchestration_model`** fallback when **`model_provider`** is absent (call sites outside the **`ProcessingRunner`** path).

**Extracted runtime modules** (`processing_runtime`, `sampler_runtime`, `decode_runtime`) take the model via **`p.model_provider.get_model(p)`** and do **not** use direct `shared.sd_model` / `p.sd_model` reads (M19 audit).

**Why any global touch remains:** **`SharedModelProvider`** is the default implementation and matches upstream “globally loaded model” behavior; **`p.sd_model`** remains a thin compatibility alias to **`shared.sd_model`**.

**What not to rewrite casually:** Do not “simplify” metadata by reading **`shared.sd_model`** in **`decode_runtime`** / **`sampler_runtime`** / **`processing_runtime`** to avoid **`processing.py`**—that would **violate** the locked **M19** boundary. Prefer changes that keep **one** orchestration owner for globals.

---

## 3. Other surfaces

Additional tolerated seams are **not** enumerated here unless they appear in **`docs/serena.md`**, the **evidence bundle**, milestone audits, or are verified deliberately during a future milestone. **Do not invent** new legacy lists from drive-by refactors.

Global hubs (**`shared.opts`**, **`shared.state`**, etc.) remain in the upstream design; Serena reduced coupling via **opts snapshot**, **runtime context**, and **runner** boundaries where milestones scoped work. Treat further migration as **milestone-governed**, not M31 cleanup.

---

## 4. Proof references

- **`docs/serena.md`** — Phase IV notes (M16–M20), M19 model provider scope.
- **`docs/milestones/M19/M19_audit.md`**, **`M19_plan.md`** — runtime modules vs `SharedModelProvider`.
- **`docs/milestones/M20/M20_audit.md`** — `shared.sd_model` aligned with provider for `process_images_inner` metadata.
- **`docs/architecture/serena_architecture_lock.md`** — locked boundaries and change-control rules.
