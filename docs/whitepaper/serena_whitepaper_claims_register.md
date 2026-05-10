# Serena White Paper — Claims Register

Purpose: bind each material statement to evidence and classify confidence. **Non-claims** and **deferred** rows prevent overclaiming.

| Claim | Type | Evidence source | Confidence | Allowed? | Notes |
| ----- | ---- | --------------- | ---------- | -------- | ----- |
| Serena’s baseline audit score was **2.4/5** | measured | `docs/sdwebuirefactoraudit.md` §1; `docs/serena.md` §2 | high | yes | Same rubric reused in post-refactor audits |
| Serena’s post–Phase VII (M33) audit score was **4.5/5** | measured | `docs/serenav1audit.md` §1 | high | yes | Distinct from M41 **4.8/5** (`docs/serenafinalaudit.md`); core case-study endpoint |
| Ledger M00 “Completed At” shows **2025-03-07** while M01+ are **2026-03-08** onward | interpreted | `docs/serena.md` §4 | medium | yes (document ambiguity) | Likely **YYYY typo** (expected **2026-03-07**); white paper does **not** silently edit ledger |
| M33 scored audit vs git refs: **`serenav1audit.md`** header **`8f65669e`**; tag **`v0.0.33-m33`** → **`ebb44177`** | observed | `docs/serenav1audit.md`; `docs/serena.md` M33; local `git` | high | yes | **`8f65669e`** descends from **`ebb44177`** (M33-era provenance chain); do not assert single canonical “audit SHA” without context |
| Audit score **improved** from baseline to M33 by **+2.1** on weighted overall | measured | `docs/serenav1audit.md` table §1 | high | yes | Category-level deltas in same table |
| Serena introduced a **`ProcessingRunner`** execution boundary (prepare / execute / finalize) | observed | `modules/runtime/runner.py`; `docs/serena.md` M10–M12 notes; `docs/architecture/serena_architecture_lock.md` §3 | high | yes | Hooks and queue seam optional; defaults preserve pass-through semantics per ledger |
| Primary txt2img and API paths are contract-tested to use the runner | observed | `docs/serena.md` M13, M14 narrative (tests named) | medium | yes | Test source files not opened this session |
| Runtime modules **`processing_runtime`**, **`sampler_runtime`**, **`decode_runtime`** exist and own extracted concerns | observed | `docs/architecture/serena_architecture_lock.md` §3; `docs/serena.md` M16–M18 | high | yes | — |
| Inner-loop runtime modules obtain the model only via **`ModelProvider.get_model(p)`** | interpreted | Lock §4 “Runtime orchestration modules” / “Model access path”; `docs/serena.md` M19 | high | yes | **Interpretation** ties lock rules to “must not bypass” |
| Serena added **mockable** runtime tests (**FakeModel** / **FakeModelProvider**) | observed | `docs/serena.md` M20 paragraph | high | yes | Does not claim full pipeline always runs without GPU in all environments |
| Serena uses **3-tier** tests: smoke / quality / nightly | observed | `pytest.ini`; `docs/serenav1audit.md` §1; workflow files under `.github/workflows/` | high | yes | — |
| Quality CI uses committed **`requirements-ci.txt`** and blocking **`pip-audit`** (post-M28a) | observed | `docs/architecture/ci_environment_contract.md` | high | yes | With **documented** `--ignore-vuln` only |
| Coverage gate is **pytest-only** and **≥42%** | observed | `docs/architecture/ci_environment_contract.md` § “Coverage policy (M27)” | high | yes | Server startup excluded from denominator |
| **Two** pip-audit deferrals persisted at M37 recheck: **diskcache**, **pygments** | observed | `docs/architecture/ci_environment_contract.md` § “pip-audit deferrals (M28)”; `docs/serena.md` M37 note | high | yes | Not a claim that no other advisories exist over time |
| M31 **architecture lock** and **allowed legacy** docs define steady-state and tolerated seams | observed | `docs/architecture/serena_architecture_lock.md`; `docs/architecture/serena_allowed_legacy_surfaces.md` | high | yes | Doc-only milestone |
| M33 is **release-ready** in **program/governance** sense, not blanket production certification | interpreted | `docs/serena.md` M33 paragraph (“**not** blanket production certification”) | high | yes | **Critical** wording from ledger |
| Extension API is **versioned** (`EXTENSION_API_VERSION`) with declared **`SUPPORTED_CALLBACKS`** | observed | `modules/extension_api.py` | high | yes | — |
| **Behavior-preserving by default** is a stated program principle | observed | `docs/serena.md` §1 “Serena Refactor Principles” | high | yes | Does not prove zero drift across all paths |
| Baseline had **no** test tiers / coverage gate per pre-refactor audit | observed | `docs/sdwebuirefactoraudit.md` §1 | high | yes | Describes baseline at audited SHA |
| **Global state** (`shared.opts`, `shared.sd_model`, etc.) remains in upstream design; Serena **reduced** coupling via snapshots, context, runner | interpreted | `docs/architecture/serena_allowed_legacy_surfaces.md` §3; `docs/serenav1audit.md` “Remaining Opportunities” | high | yes | **Not** “eliminated all globals” |
| **`processing.py`** remains large orchestration / hook owner after M33 | observed | `docs/serenav1audit.md` § “Remaining Opportunities”; allowed-legacy doc | high | yes | LOC counts may drift — avoid precise LOC in claims unless re-measured |
| M41 audit score **4.8/5** and Phase IX topics | measured / deferred | `docs/serenafinalaudit.md`; `docs/serena.md` Phase IX | high | **out of core arc** | Cite only in “subsequent work”; not the M33 thesis endpoint |
| Milestone folders `docs/milestones/MNN/` were **not** available in this workspace | observed | `.gitignore` `/docs/milestones/` | high | yes | Limits granular run-ID verification from local disk |
| Serena **improved generated image quality** or **model fidelity** | **non-claim** | — | — | **no** | **Explicit non-claim** per program scope |
| Serena **guarantees** semantic equivalence of all image outputs vs baseline | **non-claim** | — | — | **no** | CI uses stubs/fake paths in some tests per CONTRIBUTING — not full pixel-equivalence proof |
| Serena is a **drop-in replacement** for upstream on all extension surfaces | **non-claim** | Lock requires versioning for callback changes — implies **not** universal | — | **no** | Compatibility **unless explicitly versioned** (`docs/serena.md` §5) |
| Serena **eliminated all** `shared.sd_model` / **`shared.opts`** usage | **non-claim** | Allowed-legacy doc §2 | — | **no** |
| Serena has **zero** security vulnerabilities | **non-claim** | Deferrals + blocking audit policy | — | **no** | **Governed** residual risk |
| AI agents **autonomously** completed the refactor without human governance | **non-claim** | Process not fully evidenced in repo | — | **no** | Ledger describes milestone/PR discipline — implies human-in-loop |
| **Production-proven at scale** on customer workloads | **non-claim** | No evidence in reviewed docs | — | **no** |

---

### Claim types (legend)

- **observed:** Directly readable from code or primary doc text.
- **measured:** Numeric score, count, or threshold from an audit or CI artifact reference.
- **interpreted:** Combines multiple sources; judgment flagged in Notes.
- **deferred:** Explicitly left for later milestone / out of paper scope.
- **non-claim:** Statement the paper must **not** assert as fact.

---

*End of claims register.*
