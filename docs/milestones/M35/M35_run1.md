# M35 — Run 1 (CI)

**Milestone:** M35 — Remove tolerated `shared.sd_model` orchestration coupling  
**Branch:** `m35-remove-shared-sd-model-orchestration`  
**Base SHA (branch point):** `5e7cc6656152940771e4b91af8eb8f334be078dc` (local `main` at branch creation)

---

## Local verification (developer machine)

- `test/quality/test_runtime_mock.py`: **not run green** on this Windows workspace due to pre-existing `transformers` / `huggingface-hub` import conflict during `initialize` / `import webui` (see pytest error: `huggingface-hub>=0.24.0,<1.0` vs `1.8.0`). **Authoritative proof remains PR + post-merge CI** per program rules.

---

## PR CI

*(Fill after PR creation.)*

| Check | Run ID | Result |
|-------|--------|--------|
| Linter | | |
| Smoke | | |

---

## Post-merge `main` Quality

*(Binding closeout gate — fill after merge.)*

| Run ID | Commit | Result |
|--------|--------|--------|
