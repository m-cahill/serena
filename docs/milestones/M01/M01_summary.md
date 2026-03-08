# M01 Summary — CI Truthfulness & Guardrails

**Milestone:** M01  
**Branch:** m01-ci-truthfulness  
**Status:** In Progress (stub iteration)

---

## Accomplished

| Item | Status |
|------|--------|
| Same-repo PR CI | ✓ Removed skip condition |
| CLIP/pkg_resources fix | ✓ `--no-build-isolation` in launch_utils |
| `--skip-prepare-environment` | ✓ CI uses deterministic bootstrap |
| `--exit` handling | ✓ Early exit when skip-prepare + --exit |
| Install runtime deps | ✓ torch, clip, open_clip, requirements_versions |
| pip-audit | ✓ Non-blocking |
| SHA-pinned actions | ✓ |
| .gitattributes | ✓ |
| Smoke step | ✓ |
| Coverage threshold | ✓ --cov-fail-under=60 |
| Stub repositories | ✓ scripts/dev/create_stub_repos.py |

---

## Remaining Blocker

**Server startup fails** due to deep import chain from `ldm` and `sgm` packages.

With `--skip-prepare-environment`, no repos are cloned. The app expects `repositories/` to exist and imports from them at runtime.

**Solution:** Stub repositories (deterministic, no network).

**Progress:** Iterative stub addition. Each CI run reveals one more missing import. Stubs added so far:

- paths.py assertion (ddpm.py)
- LatentDiffusion, LatentDepth2ImageDiffusion
- ldm.util.default
- ldm.modules.attention, diffusionmodules (model, openaimodel), midas, distributions
- ldm.models.diffusion.ddim
- sgm.modules.encoders, attention, diffusionmodules
- sgm.models.diffusion (DiffusionEngine)
- sgm.modules.diffusionmodules.denoiser_scaling, discretizer
- sgm.modules.GeneralConditioner, openaimodel
- k_diffusion (utils, external, sampling)

**Fix applied:** Dynamic stub module (MetaPathFinder) for ldm and sgm.

---

## CI Flow (Current)

```
install deps → pip-audit → create stub repositories → setup env → smoke → start server → pytest → coverage
```

---

## Definition of Done (Status)

- [x] CI runs on push and pull_request
- [x] Linter: PASS
- [ ] Tests: PASS (blocked: server startup)
- [ ] Coverage threshold enforced
- [x] pip-audit runs
- [x] All actions pinned to SHAs
- [x] .gitattributes present
- [ ] docs/serena.md updated (when M01 closes)

---

## When M01 Closes

1. Stub iteration completes (server starts, pytest passes)
2. Update docs/serena.md ledger
3. Generate M01_audit.md
4. Merge m01-ci-truthfulness
5. Tag milestone
