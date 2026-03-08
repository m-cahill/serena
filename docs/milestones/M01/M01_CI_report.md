# M01 CI Report — 2026-03-08

**Branch:** m01-ci-truthfulness  
**Latest commit:** 5a76c617  
**Report generated:** 2026-03-08

---

## 1. CI Status

| Workflow | Run ID | Status |
|----------|--------|--------|
| Linter | 22814396752 | ✓ PASS |
| Tests | 22814850488 | Partial |

---

## 2. Dynamic Stub — Success

**Server startup:** ✓ PASS — port 7860 binds, server runs.

**Dynamic stub approach:**
- `_StubFinder` + `_StubModule` for `ldm.*` and `sgm.*`
- Resolves any nested import without individual files
- Stub classes: `forward`, `ATTENTION_MODES`, `ISL_PATHS`, etc.
- `__file__` set for `inspect.getfile`
- `ddpm.py`: DDPM, LatentDiffusion with `__init__(*a, **k)`

---

## 3. Test Results (Run 22814850488)

| Category | Result |
|----------|--------|
| wait-for-it | ✓ 127.0.0.1:7860 available |
| test_extras | ✓ PASS (3) |
| test_face_restorers | ✓ PASS (2) |
| test_torch_utils | ✓ PASS (2) |
| test_utils | ✓ PASS (10) |
| test_img2img | ✗ 500 (4) |
| test_txt2img | ✗ 500 (14) |

**img2img/txt2img:** Return 500 — stub model lacks real inference. Expected with stub-only setup.

---

## 4. Stub Layout (Minimal)

```
repositories/
  stable-diffusion-stability-ai/ldm/__init__.py (dynamic stub)
  stable-diffusion-stability-ai/ldm/models/diffusion/ddpm.py (DDPM, LatentDiffusion)
  generative-models/sgm/__init__.py (dynamic stub)
  k-diffusion/ (file-based: utils, sampling, external)
  BLIP/, stable-diffusion-webui-assets/
```

---

## 5. Links

- **Linter run:** https://github.com/m-cahill/serena/actions
- **Tests run:** 22814850488
