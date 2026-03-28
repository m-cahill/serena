# M35 — Run 1 (CI)

**Milestone:** M35 — Remove tolerated `shared.sd_model` orchestration coupling  
**PR:** https://github.com/m-cahill/serena/pull/91  
**Branch:** `m35-remove-shared-sd-model-orchestration`  
**Base SHA (branch point):** `5e7cc6656152940771e4b91af8eb8f334be078dc` (local `main` at branch creation)

---

## Authoritative PR head (current tip)

**SHA:** `a7d8b288a90425b743158311da7a6d9ea1cd8447`  

Includes M35 implementation (`68f2718714ba67e147c7fd8bd072d381c581166a`) plus `M35_run1.md` (doc-only amend of the first `M35_run1` commit; no code changes).

Validated via `gh run view <id> -R m-cahill/serena --json headSha` on the **`pull_request`** workflows below (`headSha` matches PR tip).

---

## Duplicate / superseded runs

Workflows fire on both **`push`** and **`pull_request`** for the same branch tip; both use the same `headSha` for that tip. **Authoritative PR gate evidence** uses the **`pull_request`** runs.

**Failed / superseded:** none observed for the SHAs below (all listed runs **success**).

---

## PR CI — implementation commit only (`68f27187`)

First open / push; **`pull_request`**:

| Check | Run ID | Result | `headSha` |
|-------|--------|--------|-----------|
| Linter | `23672862647` | success | `68f2718714ba67e147c7fd8bd072d381c581166a` |
| Smoke Tests | `23672862609` | success | `68f2718714ba67e147c7fd8bd072d381c581166a` |

Same SHA also had **`push`**: Linter `23672856969`, Smoke `23672856984` — success (duplicate trigger).

---

## PR CI — current tip (`a7d8b288`) — **authoritative for merge**

| Check | Run ID | Result | `headSha` |
|-------|--------|--------|-----------|
| Linter | `23673004531` | success | `a7d8b288a90425b743158311da7a6d9ea1cd8447` |
| Smoke Tests | `23673004512` | success | `a7d8b288a90425b743158311da7a6d9ea1cd8447` |

Same SHA also had **`push`**: see run list for branch (duplicate trigger; success).

**Note:** An intermediate branch tip (`5748201a`) was validated by **`pull_request`** Linter `23672933376` / Smoke `23672933380` before a doc-only **amend** rewrote history to `a7d8b288` (same tree + updated `M35_run1` narrative); **authoritative** gate for the open PR is the **`pull_request`** runs on **`a7d8b288`** above.

---

## Local verification (developer machine)

- `test/quality/test_runtime_mock.py`: **not run green** on this Windows workspace due to pre-existing `transformers` / `huggingface-hub` import conflict during `initialize` / `import webui` (see pytest error: `huggingface-hub>=0.24.0,<1.0` vs `1.8.0`). **Binding proof for this milestone remains PR Linter + Smoke here; post-merge Quality on `main` at closeout.**

---

## Post-merge `main` Quality

*(Binding closeout gate — fill after merge.)*

| Run ID | Commit | Result |
|--------|--------|--------|
| | | |
