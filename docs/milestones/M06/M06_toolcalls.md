# M06 Toolcalls — Prompt / Seed Preparation Extraction

| Timestamp | Tool | Purpose | Files/Target | Status |
|-----------|------|---------|-------------|--------|
| 2026-03-09 | write | Create M06_plan.md, M06_toolcalls.md | docs/milestones/M06/ | done |
| 2026-03-09 | read | Inspect process_images_inner extraction block | modules/processing.py | done |
| 2026-03-09 | write | Create prompt_seed_prep.py | modules/prompt_seed_prep.py | done |
| 2026-03-09 | search_replace | Replace inline seed logic with prepare_prompt_seed_state | modules/processing.py | done |
| 2026-03-09 | run | ruff check (pre-existing F811 in processing.py) | modules/ | done |
| 2026-03-09 | run | pytest test/smoke (local env: base_url/pytorch_lightning missing; CI will run full suite) | test/ | done |
| 2026-03-09 | run | git push, gh pr create | PR #20 | done |
| 2026-03-09 | write | M06_run1.md CI analysis | docs/milestones/M06/M06_run1.md | done |
