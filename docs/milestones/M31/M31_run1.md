# M31 — PR provenance and closeout (run 1)

**Milestone:** M31 — Architecture lock  
**Mode:** Documentation-only; **no** binding runtime gate (same truthful posture as M30)  
**Date (UTC):** 2026-03-26

---

## 1. Scope

| Source | Use |
|--------|-----|
| `docs/architecture/serena_architecture_lock.md` | Locked steady-state architecture and boundaries |
| `docs/architecture/serena_allowed_legacy_surfaces.md` | Tolerated legacy glue vs locked architecture |
| `docs/serena.md` | Ledger authority hierarchy and M31 row |

---

## 2. PR and merge record

| Item | Value |
|------|--------|
| **PR** | **[#83](https://github.com/m-cahill/serena/pull/83)** — `docs(M31): architecture lock and allowed legacy surfaces` |
| **Branch** | `m31-architecture-lock` → `origin/m31-architecture-lock` |
| **Head SHA (pre-merge)** | **`ffb97c144cc2d3a083fb4b25cdb258d49274a959`** |
| **Base** | `main` @ **`8131e0ed`** (immediately before M31 merge) |
| **Merge** | Squash merge to **`main`** |
| **Merge commit (`main`)** | **`09f1d785677df7400ed21d45ebb7bf3c96c7c979`** (short **`09f1d785`**) |
| **Merged at** | **2026-03-26T22:49:34Z** (GitHub `mergedAt`) |
| **Binding CI for M31** | **N/A** — documentation-only milestone; no code-path or Quality gate required for architectural truth |

---

## 3. What changed vs what did not

**Changed (M31 PR #83):**

- New: `docs/architecture/serena_architecture_lock.md`, `docs/architecture/serena_allowed_legacy_surfaces.md`
- Updated: `docs/serena.md` (post-M31 hierarchy, Phase VII progress, M31 ledger row), `serena_evidence_bundle.md` §7–8, `serena_evidence_matrix.md` (Phase VII row), `docs/milestones/M31/*`, `docs/milestones/M32/*` stubs

**Did not change:**

- Application modules, workflow YAML, `requirements*.txt` / lockfiles, CI policy definitions
- Runtime behavior, extension callback contracts, API schemas

**Diff verification:** PR #83 touched **only** paths under `docs/` (9 files). No `modules/`, `.github/`, or dependency manifests in that merge.

---

## 4. Authority order now in force

Per `docs/serena.md` and `serena_architecture_lock.md`:

1. `docs/serena.md`
2. `docs/architecture/serena_architecture_lock.md` (structural steady state)
3. `docs/architecture/serena_evidence_bundle.md` (proof narrative)
4. Milestone docs / run records / audits

Companion: `serena_allowed_legacy_surfaces.md` — **not** above the lock; clarifies tolerated seams.

---

## 5. Locked architecture vs allowed legacy (explicit)

| Topic | Where |
|-------|--------|
| **Locked** | Runner boundary, runtime modules + `ModelProvider`, UI registry/builders, extension contract + deprecation, CI measurement and security policies as documented |
| **Tolerated legacy** | e.g. `shared.sd_model` / `processing.py` orchestration and metadata glue **outside** provider-only runtime modules — see `serena_allowed_legacy_surfaces.md` and M19/M20 milestone evidence |

---

## 6. PR #83 checks — provenance / hygiene only

These are **PR workflow results** on the M31 branch. They are **not** a substitute for runtime architecture proof; M31 remains **documentation-only**.

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** (eslint + ruff jobs) | **23621850359** | **success** | [view run](https://github.com/m-cahill/serena/actions/runs/23621850359) |
| **Smoke Tests** | **23621850343** | **success** | [view run](https://github.com/m-cahill/serena/actions/runs/23621850343) |

*Individual job links appear in GitHub’s PR checks UI for the same runs.*

---

## 7. Post-merge workflows on `main` (optional provenance only)

Push of merge commit **`09f1d785`** triggered **Linter** and **Quality Tests** on `main`. These are **routine CI after a docs-only merge** — **not** claimed as a binding M31 proof surface; they provide **optional** hygiene signal only.

| Workflow | Run ID | Result | URL |
|----------|--------|--------|-----|
| **Linter** | **23621856813** | **success** | [view run](https://github.com/m-cahill/serena/actions/runs/23621856813) |
| **Quality Tests** | **23621856875** | **success** | [view run](https://github.com/m-cahill/serena/actions/runs/23621856875) |

Quality run may show **warnings** (e.g. Radon D/E/F visibility per contract); job **conclusion** was **success** at closeout verification.

---

## 8. `gh pr create` note (environment)

Initial `gh pr create` **without** `--repo m-cahill/serena` targeted the **default** GitHub CLI repository (**`AUTOMATIC1111/stable-diffusion-webui`** in this environment), producing errors such as **“No commits between main and m31-architecture-lock”** / **“Head sha can't be blank”**. Creating the PR with **`gh pr create --repo m-cahill/serena ...`** resolved the issue. This is an **environment configuration** matter, not a branch problem.

---

## 9. Closeout artifacts

| File | Role |
|------|------|
| `M31_run1.md` | This file — provenance and verification |
| `M31_summary.md` | Short summary |
| `M31_audit.md` | Milestone audit verdict |
