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
| M17 CI | gh pr create | Create PR #35 | — | done |
| M17 CI | gh run watch | Monitor Smoke Tests 23284575264 | — | done |
| M17 CI | write | Create M17_run1.md CI analysis | docs/milestones/M17/M17_run1.md | done |
| M17 closeout | gh pr merge | Merge PR #35 to main | — | done |
| M17 closeout | write | Post-merge CI analysis | docs/milestones/M17/M17_run2.md | done |
| M17 closeout | write | M17 summary | docs/milestones/M17/M17_summary.md | done |
| M17 closeout | write | M17 audit | docs/milestones/M17/M17_audit.md | done |
| M17 closeout | search_replace | Update docs/serena.md ledger + Phase IV | docs/serena.md | done |
| M17 closeout | write | Seed M18 plan + toolcalls | docs/milestones/M18/ | done |

---

## Notes

- M17 extracts sampler invocation from Txt2Img.sample, sample_hr_pass, Img2Img.sample
- Txt2Img: creation + invocation extracted; Img2Img: invocation only (creation stays in init)
- Two runtime functions: run_sampler_txt2img, run_sampler_img2img
