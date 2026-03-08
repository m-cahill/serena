# M01 CI Report — 2026-03-08

**Branch:** m01-ci-truthfulness  
**Latest commit:** 0bd566f5 (closeout)  
**Report generated:** 2026-03-08

---

## 1. CI Status — Closeout Run (Run 4)

| Workflow | Run ID | Status |
|----------|--------|--------|
| Linter | 22815773475 | ✓ PASS |
| Tests | 22815773481 | Partial (expected) |

**Commit:** `0bd566f5` — docs(M01): milestone closeout, audit, and M02 plan

---

## 2. Test Results — Run 4 (22815773481)

| Step | Result |
|------|--------|
| wait-for-it 127.0.0.1:7860 | ✓ Available after 6 seconds |
| test_extras | ✓ 3 pass |
| test_face_restorers | ✓ 2 pass |
| test_torch_utils | ✓ 2 pass |
| test_utils | ✓ 10 pass |
| test_img2img | ✗ 4 fail (500) |
| test_txt2img | ✗ 14 fail (500) |

**Total:** 17 pass, 18 fail (img2img/txt2img return 500 — stub model, no inference)

---

## 3. Failure Analysis

**img2img/txt2img:** API returns HTTP 500 because stub `LatentDiffusion` cannot perform real inference. Expected. M02 will address via fake inference (Option A).

**Coverage:** Warnings for config.py, config-3.py (couldn't parse). Non-blocking.

---

## 4. Dynamic Stub — Verified

**Server startup:** ✓ PASS — port 7860 binds, server runs.

- `_StubFinder` + `_StubModule` for `ldm.*` and `sgm.*`
- No external clones, deterministic
- Stub layout: ddpm.py, sgm, k_diffusion, BLIP

---

## 5. Run History

| Run | Commit | Linter | Tests |
|-----|--------|--------|-------|
| 3 | 5a76c617 | ✓ | Partial |
| 4 (closeout) | 0bd566f5 | ✓ | Partial |

CI remains consistent. No functional changes in closeout.

---

## 6. Links

- **Linter (Run 4):** https://github.com/m-cahill/serena/actions/runs/22815773475
- **Tests (Run 4):** https://github.com/m-cahill/serena/actions/runs/22815773481
