# M38 — CI run record 1 (PR)

**Milestone:** M38 — `processing.py` class and helper decomposition  
**PR:** https://github.com/m-cahill/serena/pull/94  
**Branch:** `m38-processing-class-helper-decomposition`

## Local vs CI

Local `pytest` was **not** used as binding proof for M38 (incomplete local dependency set, e.g. `einops` / `cv2` in some environments). **GitHub Actions** on this PR is the authoritative verification surface for Linter + Smoke.

---

## A. Refactor-only tip (merge-critical code)

**Commit:** `576b39354003aa3bc7a3b41cc38564c654b7b671`  
**Message:** `refactor(M38): split processing classes into processing_types/helpers/infotext`

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23697815570** | `pull_request` | `576b39354003aa3bc7a3b41cc38564c654b7b671` | **success** |
| **Smoke Tests** | **23697815572** | `pull_request` | `576b39354003aa3bc7a3b41cc38564c654b7b671` | **success** |

Mirror `push` on same SHA: Linter **23697806689**, Smoke **23697806695** — both **success**.

---

## B. PR tip ledger (historical — §B lagged before merge)

**Closeout note:** This section’s **last pre-merge table row** documented SHA **`85094659…`**, while **doc-only commits** had already advanced the PR head. **Merge approval** did **not** rely on §B alone; it used the **validated green `pull_request` tip** below.

**Authoritative approval basis (binding `pull_request` CI on the merge-ready head):**

| Item | Value |
|------|--------|
| **PR head SHA** | `3654f8a30433a1ecd7de54811da6a454f23db458` |
| **Linter** | **23700334490** — `pull_request` — **success** |
| **Smoke Tests** | **23700334489** — `pull_request` — **success** |

Validated via `gh run view <run_id> --repo m-cahill/serena --json headSha,conclusion,event`.

**Prior §B snapshot (stale vs approval head):** the table that ended with **`85094659…`** / Linter **23700286459** / Smoke **23700286460** was the last full row written before merge; **`3654f8a3…`** superseded it for approval.

---

## C. Merge to `main`

| Item | Value |
|------|--------|
| **Merge method** | GitHub **merge commit** (`gh pr merge 94 --merge`) |
| **Merge commit (`main`)** | `17c21be669942518ab4683ba504c87c1ad58900e` |
| **Merged at** | **2026-03-29T03:45:35Z** |

---

## Post-merge `main` (Linter + Quality)

**Merge commit:** `17c21be669942518ab4683ba504c87c1ad58900e` — event **`push`** to **`main`**.

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23700723142** | `push` | `17c21be669942518ab4683ba504c87c1ad58900e` | **success** |
| **Quality Tests** | **23700723134** | `push` | `17c21be669942518ab4683ba504c87c1ad58900e` | **success** |

**Quality run (reported):** **217** passed; **TOTAL** coverage **48%** (workflow log summary).

### Follow-up: doc closeout on `main` (binding tip after merge artifacts)

After **`17c21be6`**, a **documentation-only** commit recorded M38 closeout + M39 stubs:

| Item | Value |
|------|--------|
| **Commit (`main`)** | `e143a881ff11082cf35a2de701473081ffa6e72f` |
| **Message** | `docs(M38): closeout run1 summary audit ledger; seed M39 stubs` |

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23700844280** | `push` | `e143a881ff11082cf35a2de701473081ffa6e72f` | **success** |
| **Quality Tests** | **23700844278** | `push` | `e143a881ff11082cf35a2de701473081ffa6e72f` | **success** |

**Quality run (reported):** **217** passed; **TOTAL** coverage **48%** — same counts as merge commit run (doc-only delta).

---

**Status:** **Merged** — see **`M38_summary.md`**, **`M38_audit.md`**, **`docs/serena.md`**.
