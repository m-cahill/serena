# M35 — Run 1 (CI)

**Milestone:** M35 — Remove tolerated `shared.sd_model` orchestration coupling  
**PR:** https://github.com/m-cahill/serena/pull/91  
**Branch:** `m35-remove-shared-sd-model-orchestration`  
**Base SHA (branch point):** `5e7cc6656152940771e4b91af8eb8f334be078dc` (local `main` at branch creation)

---

## Authoritative PR CI (`pull_request` workflows)

**Current PR head:** use `gh pr view 91 -R m-cahill/serena --json headRefOid` (must match merge tip before approval).

**Snapshot (2026-03-28 UTC)** — validated with `gh run view <id> -R m-cahill/serena --json headSha,conclusion`:

| Role | Check | Run ID | Result | `headSha` |
|------|-------|--------|--------|-----------|
| **PR head at snapshot (doc + M35 code)** | Linter | `23673160005` | success | `db94c546d2fc4a8b5747d28e610202d99a2186d2` |
| **PR head at snapshot (doc + M35 code)** | Smoke Tests | `23673159991` | success | `db94c546d2fc4a8b5747d28e610202d99a2186d2` |

M35 **implementation** first landed in **`68f2718714ba67e147c7fd8bd072d381c581166a`** — **`pull_request`** Linter **`23672862647`**, Smoke **`23672862609`** (both success; same `headSha`).

---

## Duplicate / superseded runs

Workflows fire on both **`push`** and **`pull_request`** for the same branch tip; **`push`** duplicates are **not** used as the PR gate. **Failed / superseded:** none observed on the recorded SHAs (all **success**).

Doc-only iteration on the branch produced additional green runs on intermediate tips (`5748201a`, `a7d8b288`, etc.); the **snapshot** table above is the authoritative pair for tip **`db94c546`** at the time of recording.

---

## Local verification (developer machine)

- `test/quality/test_runtime_mock.py`: **not run green** on this Windows workspace due to pre-existing `transformers` / `huggingface-hub` import conflict during `initialize` / `import webui` (see pytest error: `huggingface-hub>=0.24.0,<1.0` vs `1.8.0`). **Binding proof for this milestone remains PR Linter + Smoke here; post-merge Quality on `main` at closeout.**

---

## Post-merge `main` Quality

*(Binding closeout gate — fill after merge.)*

| Run ID | Commit | Result |
|--------|--------|--------|
| | | |
