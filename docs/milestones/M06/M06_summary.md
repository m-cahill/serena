# M06 Summary — Prompt / Seed Preparation Extraction

**Project:** Serena  
**Phase:** Phase II — Runtime Seam Preparation  
**Milestone:** M06 — Prompt / seed prep extraction  
**Status:** Closed  
**Branch:** m06-prompt-seed-prep  
**PR:** #20  
**Commit:** 6744152a (merge)  
**Quality Run:** 22890285319 ✓

---

## Accomplished

| Item | Status |
|------|--------|
| Created `modules/prompt_seed_prep.py` | ✓ |
| Extracted `prepare_prompt_seed_state(p)` | ✓ |
| Replaced inline all_seeds/all_subseeds logic in process_images_inner | ✓ |
| Left `setup_prompts()` on StableDiffusionProcessing | ✓ |
| Left `fill_fields_from_opts()` in process_images_inner | ✓ |
| Mutate p.seed/p.subseed before call; write to p | ✓ |
| Preserved behavior (prompt lists, seed lists, extension compatibility) | ✓ |

---

## CI Layout After M06

| Workflow | Trigger | Coverage | Security |
|----------|---------|----------|----------|
| Smoke Tests | pull_request (main) | No gate | None |
| Linter | pull_request | — | — |
| Quality Tests | push to main | ≥40% | pip-audit (informational) |

---

## Invariants Preserved

- Prompt lists identical
- Negative prompt behavior unchanged
- Seed generation identical (subseed, variation, batch)
- Extension compatibility (p.all_seeds, p.all_subseeds on p)
- API compatibility (txt2img/img2img)
- Generation determinism

---

## Blast Radius

| File | Change |
|------|--------|
| modules/prompt_seed_prep.py | New |
| modules/processing.py | Modified |

---

## Refactor Result

Prompt and seed preparation isolated behind a clean function boundary. Second Phase II runtime seam; prepares for M07 opts snapshot and M09 execution context.
