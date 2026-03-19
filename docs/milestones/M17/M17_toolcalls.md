# M17 Toolcalls

## Context

Milestone: M17 — Sampler Runner Extraction
Phase: Phase IV — Runtime Extraction

## Actions

| Timestamp | Tool | Purpose | Files | Status |
|-----------|------|---------|-------|--------|
| M17 init | write | Replace M17_plan.md stub with full plan | docs/milestones/M17/M17_plan.md | done |
| M17 impl | write | Create sampler_runtime.py with run_sampler_txt2img, run_sampler_img2img | modules/runtime/sampler_runtime.py | done |
| M17 impl | search_replace | Extract sampler invocations in processing.py | modules/processing.py | done |
| M17 impl | write | Add M17 delegation tests | test/quality/test_sampler_runtime.py | done |
| M17 impl | search_replace | Update runtime __init__.py docstring | modules/runtime/__init__.py | done |

---

## Notes

- M17 extracts sampler invocation from Txt2Img.sample, sample_hr_pass, Img2Img.sample
- Txt2Img: creation + invocation extracted; Img2Img: invocation only (creation stays in init)
- Two runtime functions: run_sampler_txt2img, run_sampler_img2img
