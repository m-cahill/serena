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

### 2.1 `shared.sd_model` in `process_images` / `process_images_inner` orchestration (primary)

**What:** **`modules/processing.py`** still reads **`shared.sd_model`** (and related fields) for **orchestration** outside the inner-loop runtime modules—for example checkpoint naming/hash, dimension fixes, conditioning, and **metadata/infotext** alignment. The **extracted runtime modules** (`processing_runtime`, `sampler_runtime`, `decode_runtime`) take the model via **`p.model_provider.get_model(p)`** and do **not** use direct `shared.sd_model` / `p.sd_model` reads (M19 audit).

**Why it remains:** Phase IV explicitly scoped **model provider injection** to the **runtime extraction modules**; full removal of global model reads from **`processing.py`** was not required for the milestone chain through M20.

**Why it is not a release blocker:** Behavior is **preserved**, **contract-tested** paths go through the runner, and **M20** documents honest test glue: **`shared.sd_model`** is aligned with the provider return for **`process_images_inner`** metadata (`M20_audit.md` §3).

**M34 (Phase VIII) progress:** **`RuntimeContext`** now carries an explicit **`ModelIdentity`** (checkpoint name/hash) populated in **`process_images_inner`** from the same authoritative model object as before. Remaining **`shared.sd_model`** reads in **`processing.py`** (conditioning, caches, **`StableDiffusionProcessing.sd_model`** property, etc.) are **unchanged** and remain **in scope for M35**.

**What would justify addressing later:** A dedicated milestone to **thread model identity** through **`StableDiffusionProcessing`** / **`RuntimeContext`** for all metadata reads, with regression and extension checks—only if the program explicitly schedules it.

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
