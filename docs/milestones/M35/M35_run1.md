# M35 — Run 1 (CI)

**Milestone:** M35 — Remove tolerated `shared.sd_model` orchestration coupling  
**PR:** https://github.com/m-cahill/serena/pull/91  
**Branch:** `m35-remove-shared-sd-model-orchestration`  
**Base SHA (branch point):** `5e7cc6656152940771e4b91af8eb8f334be078dc` (local `main` at branch creation)

---

## Authoritative PR head (current tip)

**SHA:** `5748201a7a7eb7595b5f3e2135d7c0e544dfaec3`  

Includes M35 implementation (`68f2718714ba67e147c7fd8bd072d381c581166a`) plus this `M35_run1.md` evidence file.

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

## PR CI — current tip (`5748201a`) — **authoritative for merge**

| Check | Run ID | Result | `headSha` |
|-------|--------|--------|-----------|
| Linter | `23672933376` | success | `5748201a7a7eb7595b5f3e2135d7c0e544dfaec3` |
| Smoke Tests | `23672933380` | success | `5748201a7a7eb7595b5f3e2135d7c0e544dfaec3` |

Same SHA also had **`push`**: Linter `23672932157`, Smoke `23672932166` — success (duplicate trigger).

---

## Local verification (developer machine)

- `test/quality/test_runtime_mock.py`: **not run green** on this Windows workspace due to pre-existing `transformers` / `huggingface-hub` import conflict during `initialize` / `import webui` (see pytest error: `huggingface-hub>=0.24.0,<1.0` vs `1.8.0`). **Binding proof for this milestone remains PR Linter + Smoke here; post-merge Quality on `main` at closeout.**

---

## Post-merge `main` Quality

*(Binding closeout gate — fill after merge.)*

| Run ID | Commit | Result |
|--------|--------|--------|
| | | |
