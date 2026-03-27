# M33 — Release-ready 5/5 close

**Phase VII** (per `docs/serena.md`). Follows **M32** (evidence/audit closure).

**Status:** Full plan (implements program closeout per approved scope).

---

## Title

Release-ready 5/5 close

---

## Objective

Close the **Serena** refactor **program** with a final **governance and documentation** milestone that:

1. Declares **Phase VII** and the **current milestone map** **closed** through **M33**.
2. States **release-readiness** in **program terms**: governed, auditable, publishable end state suitable for further development and case-study publication — **not** blanket production certification for the upstream web UI.
3. Consolidates the **authority stack**, **binding evidence pointers**, and **explicit deferrals** without reopening M31 (architecture lock) or M32 (evidence closure).
4. Produces **`M33_run1.md`**, **`M33_summary.md`**, **`M33_audit.md`**, and updates **`docs/serena.md`** in line with the ledger and evidence docs.

---

## Scope

### In scope

- Final program closeout documentation (milestone folder + ledger).
- Truthful **5.0 / 5** program posture as already established by prior milestones and audits; M33 **records** closure, does not re-score runtime proof.
- Optional **`docs/architecture/serena_release_ready_closeout.md`** — **omit by default** unless core artifacts leave a gap (per program direction: **not** created for M33 unless necessary).

### Out of scope

- Application code, workflow YAML, dependency manifests, lockfiles, CI thresholds.
- New architecture decisions or expansion of allowed legacy beyond existing docs.
- Reopening M31 lock or M32 evidence narrative.
- Annotated tag **`v0.0.33-m33`** during implementation — **only** after merge **and** post-merge CI, during **final closeout**, if clean.

---

## Authority (read first)

Treat as authoritative for M33 content:

- `docs/serena.md`
- `docs/architecture/serena_architecture_lock.md`
- `docs/architecture/serena_allowed_legacy_surfaces.md`
- `docs/architecture/serena_evidence_bundle.md`
- `docs/architecture/serena_evidence_matrix.md`
- `docs/milestones/M32/M32_run1.md`, `M32_summary.md`, `M32_audit.md`

---

## Explicit deferrals (no invention)

Carry forward **only** governed deferrals already documented for **M28**:

- **CVE-2025-69872** (`diskcache`)
- **CVE-2026-4539** (`pygments`)

No PyPI fix at closeout; **`--ignore-vuln`** only for those IDs per `ci_environment_contract.md` and milestone evidence. Do **not** add other “deferred” items unless explicitly recorded in ledger, bundle, or milestone docs.

---

## Deliverables

| Artifact | Role |
|----------|------|
| `M33_run1.md` | Main closeout record: purpose, authority stack, Phases I–VII summary, binding evidence map, why M33 is closeout not re-verification, release-ready interpretation **(A)**, deferrals, verdict, PR/merge provenance |
| `M33_summary.md` | Concise closeout; doc-only; Phase VII complete; program at 5.0/5 in governance terms |
| `M33_audit.md` | Truthfulness, scope, consistency, no invented claims, closeout readiness |
| `docs/serena.md` | M33 ledger row; Phase VII complete; M33 final milestone in current map; preserve prior history |
| `serena_evidence_bundle.md` / `serena_evidence_matrix.md` | Minimal alignment (M33 complete; no new runtime gate) |

---

## Verification

1. **Consistency** with ledger, lock, allowed-legacy companion, bundle, matrix, and M32 artifacts.
2. **Diff inspection:** no changes outside `docs/` (except if a path typo fix is explicitly required — not expected).
3. **Ledger:** M33 recorded; Phase VII complete; program map closed through M33.
4. **CI / PR:** If M33 is doc-only, PR checks and post-merge workflows are **hygiene/provenance only**, not new binding runtime proof (same as M30/M31/M32).

---

## Definition of done

- M33 milestone docs exist and are internally consistent.
- `docs/serena.md` reflects M33 and Phase VII complete; M33 is the **final** milestone in the **current** Serena program map.
- “Release-ready” is framed as **program/governance** closeout per clarification **(A)**.
- No code, workflow, dependency, or lockfile changes.
- Tag **`v0.0.33-m33`**: **not** created during implementation; only after merge + post-merge CI at final closeout if appropriate.

---

## Branch

**`m33-release-ready-close`** — PR to `main` per normal Serena workflow.
