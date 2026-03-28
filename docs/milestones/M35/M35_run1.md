# M35 — Run 1 (CI)

**Milestone:** M35 — Remove tolerated `shared.sd_model` orchestration coupling  
**PR:** https://github.com/m-cahill/serena/pull/91  
**Branch:** `m35-remove-shared-sd-model-orchestration`  
**Base SHA (branch point):** `5e7cc6656152940771e4b91af8eb8f334be078dc` (local `main` at branch creation)

---

## Merge to `main`

| Field | Value |
|-------|--------|
| **Merge method** | GitHub **merge commit** (`gh pr merge 91 -R m-cahill/serena --merge`) — **not** squash |
| **Merge commit SHA** | `45e6f4fbfb8f6ed2dfc336423d1f414f66c77549` |
| **Merged at (GitHub)** | **2026-03-28T00:59:00Z** UTC |

**Approval basis (pre-merge):** merge-ready PR head **`564ebd2799cb5e90410de21a15a7f5e3295b4598`** — **`pull_request`** Linter **`23673315409`** (success), Smoke Tests **`23673315420`** (success); `headSha` verified via `gh run view --json headSha`.

**Pre-merge `M35_run1.md` snapshot table:** the table below under “Authoritative PR CI” recorded an earlier doc snapshot tip **`db94c546…`** with runs **`23673160005`** / **`23673159991`**. **Final merge approval** used the later green tip **`564ebd27…`** above (no additional pre-merge commit was made solely to restate the snapshot).

---

## Authoritative PR CI (`pull_request` workflows) — historical snapshot

**Snapshot (2026-03-28 UTC, pre-closeout)** — validated with `gh run view <id> -R m-cahill/serena --json headSha,conclusion`:

| Role | Check | Run ID | Result | `headSha` |
|------|-------|--------|--------|-----------|
| **PR head at snapshot (doc + M35 code)** | Linter | `23673160005` | success | `db94c546d2fc4a8b5747d28e610202d99a2186d2` |
| **PR head at snapshot (doc + M35 code)** | Smoke Tests | `23673159991` | success | `db94c546d2fc4a8b5747d28e610202d99a2186d2` |

M35 **implementation** first landed in **`68f2718714ba67e147c7fd8bd072d381c581166a`** — **`pull_request`** Linter **`23672862647`**, Smoke **`23672862609`** (both success; same `headSha`).

---

## Duplicate / superseded runs

Workflows fire on both **`push`** and **`pull_request`** for the same branch tip; **`push`** duplicates are **not** used as the PR gate. **Failed / superseded:** none observed on the recorded SHAs (all **success**).

Doc-only iteration on the branch produced additional green runs on intermediate tips (`5748201a`, `a7d8b288`, etc.).

---

## Local verification (developer machine)

- `test/quality/test_runtime_mock.py`: **not run green** on this Windows workspace due to pre-existing `transformers` / `huggingface-hub` import conflict during `initialize` / `import webui` (see pytest error: `huggingface-hub>=0.24.0,<1.0` vs `1.8.0`). **Binding proof for this milestone:** PR Linter + Smoke (approval tip) and **post-merge Quality on `main`** below.

---

## Post-merge `main` CI (binding closeout)

Triggered by **`push`** to **`main`** after merge commit **`45e6f4fbfb8f6ed2dfc336423d1f414f66c77549`**.

| Check | Run ID | Result | `headSha` (workflow) |
|-------|--------|--------|----------------------|
| **Linter** | `23673838902` | success | `45e6f4fbfb8f6ed2dfc336423d1f414f66c77549` |
| **Quality Tests** | `23673838908` | success | `45e6f4fbfb8f6ed2dfc336423d1f414f66c77549` |

**Quality summary (run `23673838908`, log):** **203** tests passed; **TOTAL** coverage **48%** (pytest coverage report as printed in CI). No CI policy or threshold changes in M35.
