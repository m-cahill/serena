# M01 CI Run 3 — Stub Repositories (Iterative)

**Date:** 2026-03-08  
**Branch:** m01-ci-truthfulness  
**Trigger:** Stub repository approach (ac965561 → 1d3c4dcb)

---

## 1. Workflow Identity

| Workflow | Run ID | Status |
|----------|--------|--------|
| Linter | 22810292142 | ✓ success |
| Tests | 22810292144 | ✗ failure |

---

## 2. Approach

**Stub repositories** instead of cache/submodules:

- `scripts/dev/create_stub_repos.py` creates minimal `repositories/` layout
- Satisfies `paths.py` assertion and import chain
- Deterministic, no network, no cloning

---

## 3. Stub Progression (by run)

| Run | Blocker | Fix |
|-----|---------|-----|
| 22810169638 | `paths.py` assert (ddpm.py) | Add ddpm.py stub |
| 22810208301 | `LatentDiffusion` import | Add LatentDiffusion, LatentDepth2ImageDiffusion to ddpm |
| 22810246639 | `ldm.util` | Add ldm.util.default |
| 22810246639 | `ldm.modules.midas` | Add ldm.modules.midas |
| 22810292144 | `sgm.models` | Add sgm.models.diffusion |
| 22810326719 | `sgm.modules.diffusionmodules.denoiser_scaling` | Add denoiser_scaling, discretizer, DiffusionEngine, GeneralConditioner |

---

## 4. Current Stub Layout

```
repositories/
  stable-diffusion-stability-ai/
    ldm/
      models/diffusion/ddpm.py (LatentDiffusion, LatentDepth2ImageDiffusion)
      util.py (default)
      modules/
        encoders/modules.py (FrozenCLIPEmbedder, FrozenOpenCLIPEmbedder, CLIPTextModel)
        attention/ (CrossAttention)
        diffusionmodules/model.py (AttnBlock)
        midas/
  generative-models/
    sgm/
      models/diffusion/ (DiffusionEngine)
      modules/
        encoders/modules.py
        attention/ (CrossAttention, SDP_IS_AVAILABLE, XFORMERS_IS_AVAILABLE)
        diffusionmodules/ (model, denoiser_scaling, discretizer, openaimodel)
        conditioner.py (GeneralConditioner)
  k-diffusion/
  BLIP/
  stable-diffusion-webui-assets/
```

---

## 5. Remaining Blocker (Run 22810326719)

```
ModuleNotFoundError: No module named 'sgm.modules.diffusionmodules.denoiser_scaling'
```

Fix applied in next commit: add denoiser_scaling, discretizer, DiffusionEngine, GeneralConditioner, openaimodel stubs.

---

## 6. Next Steps

- Push stub additions
- Run CI
- If more import errors: add stubs iteratively
- When server starts: verify pytest and coverage pass
