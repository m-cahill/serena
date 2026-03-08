# M01 CI Report — 2026-03-08

**Branch:** m01-ci-truthfulness  
**Latest commit:** 9a83c70e  
**Report generated:** 2026-03-08

---

## 1. CI Status

| Workflow | Run ID | Status |
|----------|--------|--------|
| Linter | 22812569761 | ✓ PASS |
| Tests | 22812569762 | ✗ FAIL |

---

## 2. Test Failure

**Root cause:** Server startup fails before binding to port 7860.

**Error (from output.txt):**
```
ModuleNotFoundError: No module named 'ldm.models.diffusion.plms'
  File "modules/sd_hijack.py", line 15, in <module>
    import ldm.models.diffusion.plms
```

**Effect:** `wait-for-it` times out (20s); pytest never runs.

---

## 3. Stub Progression

| Step | Blocker | Fix applied |
|------|---------|-------------|
| 1 | paths.py assert | ddpm.py |
| 2 | LatentDiffusion | ddpm classes |
| 3 | ldm.util | default() |
| 4 | ldm.modules.midas | midas/ |
| 5 | ldm.modules.distributions | DiagonalGaussianDistribution |
| 6 | ldm.modules.diffusionmodules.openaimodel | openaimodel.py |
| 7 | sgm.* | sgm stubs |
| 8 | k_diffusion.* | external, utils, sampling |
| 9 | ldm.models.diffusion.ddim | ddim.py |
| 10 | **ldm.models.diffusion.plms** | **Next fix** |

---

## 4. Fix Applied

**Dynamic stub module** (commit in progress): MetaPathFinder + _StubModule for ldm and sgm. Resolves any nested import without individual files.

---

## 5. Links

- **PR:** (create when ready to merge)
- **Linter run:** https://github.com/m-cahill/serena/actions/runs/22812569761
- **Tests run:** https://github.com/m-cahill/serena/actions/runs/22812569762
