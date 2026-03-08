# M02 Plan — Local Developer Guardrails

**Milestone:** M02  
**Title:** Local dev guardrails, CONTRIBUTING, repeatable verification  
**Status:** Not Started  
**Depends on:** M01 (complete)

---

## Intent

Extend CI truthfulness to the **API layer** so that txt2img/img2img tests pass in CI without requiring a real model. Add local developer guardrails (CONTRIBUTING, repeatable verification).

---

## Scope

1. **API-layer CI truthfulness** — Make txt2img/img2img return 200 in CI
2. **CONTRIBUTING.md** — Document local setup, CI flow, stub behavior
3. **Repeatable verification** — Ensure `make verify` or equivalent works locally

---

## Approach: Lightweight Fake Inference (Option A)

**Recommendation:** Return a deterministic 1×1 PNG for generation endpoints when running with stub model.

### Rationale

- Keeps API contract intact (200, valid PNG in response)
- Tests verify request/response shape, not image quality
- No `--test-mode` flag proliferation
- No test skipping (all tests run)

### Implementation Options

**A1. Stub model returns placeholder tensor**

- Extend `LatentDiffusion` stub so `forward` / decode path returns a minimal valid tensor
- Processing pipeline produces 1×1 PNG
- Requires understanding of `process_images` → decode → save flow

**A2. Early exit in API with fake image**

- Detect stub model (e.g. `isinstance(sd_model, ...)` or env flag)
- In txt2img/img2img handlers, return pre-built 1×1 PNG before calling `process_images`
- Simpler but bypasses more of the pipeline

**A3. CondFunc / hijack for CI**

- Use existing `CondFunc` or similar to replace `process_images` output in CI
- Return fake images when `--skip-prepare-environment` or `CI=true`

### Preferred

**A1** if feasible with minimal stub changes; otherwise **A2** for speed.

---

## Non-goals

- No real model inference in CI
- No architecture changes to processing pipeline
- No test tiering (M03)

---

## Definition of Done

- [ ] txt2img API returns 200 in CI
- [ ] img2img API returns 200 in CI
- [ ] CONTRIBUTING.md added with local/CI setup
- [ ] Coverage threshold enforced (60%)
- [ ] docs/serena.md updated with M02 status

---

## Handoff from M01

M01 delivered:
- Deterministic CI, no external clones
- Dynamic stub loader (ldm, sgm)
- Server startup, 17 tests pass
- img2img/txt2img return 500 (stub model)

M02 closes the API-layer gap.
