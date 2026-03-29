# M39 — CI run record 1 (PR + `main`)

**Milestone:** M39 — Remaining legacy surface narrowing  
**PR:** https://github.com/m-cahill/serena/pull/95  
**Branch:** `m39-remaining-legacy-surface-narrowing`

## Merge

| Item | Value |
|------|--------|
| **Merge method** | GitHub **merge commit** (not squash) |
| **Merge commit (`main`)** | `d4551e6d55c31c5f6b1efd0a5d04956a19d0ea53` |
| **Merged at** | **2026-03-29T21:45:43Z** |

---

## A. PR merge approval (authoritative green tip)

**Pre-merge §A lag:** `M39_run1.md` on the PR branch recorded an earlier table row (**`d0bb6afa…`**). **Merge approval** used the **later** green **`pull_request`** tip documented by the user:

| Item | Value |
|------|--------|
| **PR head SHA** | `0aa0d93d4df894aaef841c0c0f425c75ab3ba8d6` |
| **Linter** | **`23719443302`** — **success** |
| **Smoke Tests** | **`23719443311`** — **success** |

---

## B. Post-merge `main` — merge commit `d4551e6d` (first `push`)

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23719815686** | `push` | `d4551e6d55c31c5f6b1efd0a5d04956a19d0ea53` | **success** |
| **Quality Tests** | **23719815660** | `push` | `d4551e6d55c31c5f6b1efd0a5d04956a19d0ea53` | **failure** |

**Failure:** Quality **`test_runtime_mock`** — `AttributeError: 'types.SimpleNamespace' object has no attribute 'live_previews_enable'` at **`processing_runtime.py`** via **`_eff_opts(p)`** when **`opts_snapshot`** is a **sparse** test double (missing keys present in full **`opts.data`**).

---

## C. Post-merge `main` — follow-up fix (binding `main` tip)

| Item | Value |
|------|--------|
| **Commit** | `1b9f304efef050b107435d526bade735bf762bcc` |
| **Message** | `fix(M39): _eff_opts view falls back to shared.opts for missing snapshot keys` |

| Workflow | Run ID | Event | `headSha` | Conclusion |
|----------|--------|-------|-----------|------------|
| **Linter** | **23719932253** | `push` | `1b9f304efef050b107435d526bade735bf762bcc` | **success** |
| **Quality Tests** | **23719932254** | `push` | `1b9f304efef050b107435d526bade735bf762bcc` | **success** |

**Quality run (reported):** **222** passed; **TOTAL** coverage **48%** (pytest-only report line).

---

## D. Implementation note

- **`_eff_opts(p)`** returns **`_EffOptsView(snapshot, shared.opts)`** when **`p.opts_snapshot`** is set: attributes present on the snapshot object are used; **missing** keys fall back to **`shared.opts`** so full **`create_opts_snapshot(shared.opts)`** behavior is unchanged and **sparse** Quality fixtures match pre-M39 semantics.
- **Eliminated** direct **`shared.opts`** reads in **`processing_types.py`**, **`processing_infotext.py`**, **`processing.py`** (overlay branch), **`processing_runtime.py`** (preview gate). **`processing.py`** still calls **`create_opts_snapshot(shared.opts)`** — intentional capture point (M07).

---

## E. Doc closeout on `main` (optional provenance)

After **`1b9f304e`**, **`docs(M39): closeout…`** @ **`05b0dcbaa6747458a30de37cb42a03a2b6b9f676`**:

| Workflow | Run ID | Event | Conclusion |
|----------|--------|-------|------------|
| **Linter** | **23720050208** | `push` | **success** |
| **Quality Tests** | **23720050207** | `push` | **success** |
