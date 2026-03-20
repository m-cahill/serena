# M19 Summary — Model provider interface

**Milestone:** M19  
**Status:** Completed  
**Audit score:** 5.0 / 5

---

## What changed

- Introduced **`ModelProvider`** / **`SharedModelProvider`** in `modules/runtime/model_provider.py`; default implementation returns `shared.sd_model` via lazy import inside `get_model(p)`.
- **`ProcessingRunner`** accepts optional `model_provider` (default `SharedModelProvider`) and sets **`processing.model_provider`** in **`prepare()`**.
- Runtime modules use **`p.model_provider.get_model(p)`** only for model access:
  - `processing_runtime.py` — `ema_scope`, latent channels, `apply_alpha_schedule_override`
  - `sampler_runtime.py` — `create_sampler(..., model)`
  - `decode_runtime.py` — VAE decode path and `lowvram.is_enabled`
- **`test/quality/test_model_provider.py`** — delegation, runner wiring, sampler tests (patched **`modules.sd_samplers.create_sampler`** for deterministic CI).
- **PR #38** — test-only fix after post-merge Quality failure (no production changes).

---

## Why it mattered

- Completes **dependency inversion** for the inner-loop runtime: **`runtime → model_provider → model`**, not direct **`shared.sd_model`** / **`p.sd_model`** in runtime modules.
- Unblocks **M20** (mockable runtime, unit tests without full model stack).
- Preserves behavior: same model object and semantics as before; no checkpoint / `sd_models` / extension surface changes.

---

## What remains

- **M20** — Runtime tests with mockable boundaries (fake models, deterministic pipeline tests).
- **`ProcessingRunner.prepare()`** contract: subclasses must call **`super().prepare(request)`** or set **`model_provider`** explicitly.

---

## PRs and evidence

| PR | Role |
|----|------|
| [#37](https://github.com/m-cahill/serena/pull/37) | M19 implementation |
| [#38](https://github.com/m-cahill/serena/pull/38) | Quality test isolation fix |

Quality (passing): run **23326003636**.
