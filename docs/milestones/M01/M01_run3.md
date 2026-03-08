# M01 CI Run 3 — Stub Repositories (Iterative)

**Date:** 2026-03-08  
**Branch:** m01-ci-truthfulness  
**Trigger:** Stub repository approach (ac965561 → f013e553)

---

## 1. Workflow Identity

| Workflow | Latest Run | Status |
|----------|------------|--------|
| Linter | 22814396752 | ✓ success |
| Tests | 22814850488 | Partial (server ✓, img2img/txt2img 500) |

---

## 2. Approach

**Stub repositories** instead of cache/submodules:

- `scripts/dev/create_stub_repos.py` creates minimal `repositories/` layout
- Satisfies `paths.py` assertion and import chain
- Deterministic, no network, no cloning

---

## 3. Stub Progression (by run)

| Blocker | Fix |
|---------|-----|
| `paths.py` assert (ddpm.py) | Add ddpm.py stub |
| `LatentDiffusion` import | Add LatentDiffusion, LatentDepth2ImageDiffusion |
| `ldm.util` | Add ldm.util.default |
| `ldm.modules.midas` | Add ldm.modules.midas |
| `ldm.modules.distributions` | Add distributions, DiagonalGaussianDistribution |
| `ldm.modules.diffusionmodules.openaimodel` | Add openaimodel, explicit __init__ imports |
| `sgm.models`, `sgm.modules.*` | Add sgm stubs (attention, diffusionmodules, encoders, conditioner) |
| `k_diffusion.external`, `k_diffusion.utils` | Add external, utils, sampling stubs |
| `k_diffusion.sampling.get_sigmas_*` | Add get_sigmas_karras, exponential, polyexponential |

---

## 4. Current Stub Layout

```
repositories/
  stable-diffusion-stability-ai/
    ldm/
      models/diffusion/ddpm.py
      util.py
      modules/
        __init__.py (imports distributions, diffusionmodules)
        encoders/modules.py
        attention/, diffusionmodules/ (model, openaimodel)
        distributions/distributions.py (DiagonalGaussianDistribution)
        midas/
  generative-models/
    sgm/
      models/diffusion/ (DiffusionEngine)
      modules/ (attention, diffusionmodules, encoders, conditioner)
  k-diffusion/
    k_diffusion/
      __init__.py (imports utils, sampling, external)
      utils.py, external.py, sampling.py
  BLIP/
  stable-diffusion-webui-assets/
```

---

## 5. Dynamic Stub Approach (Commit 5a76c617)

Replaced manual file-by-file stubs with **dynamic stub modules**:

- `_StubFinder` (MetaPathFinder): catches any `ldm.*` or `sgm.*` import the default finder misses
- `_StubLoader`: creates `_StubModule` with `__path__`, `__file__` for inspect
- `_StubModule`: resolves attributes as submodules, stub classes, or dicts (UPPER_CASE)
- Stub classes: metaclass returns no-op for missing attrs, `{}` for ATTENTION_MODES
- UPPER_CASE on modules → dict (e.g. `midas.api.ISL_PATHS`)
- `__file__` = `<stub:name>` so `inspect.getfile` works
- Keeps `ddpm.py` for paths.py assertion; DDPM, LatentDiffusion with `__init__(*a,**k)`
- Keeps k_diffusion file-based (needs real get_sigmas_*, torch, etc.)

Eliminates whack-a-mole import chain.
