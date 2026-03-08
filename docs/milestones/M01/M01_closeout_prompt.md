# M01 Closeout Prompt — Cursor

**Use this prompt to formally close M01 and update the Serena ledger.**

---

## Paste this into Cursor

```
# M01 Closeout — CI Truthfulness & Guardrails

M01 is complete. Governance assessment: **COMPLETE** (audit score 4.7/5).

## Actions Required

1. **Update docs/serena.md Milestone Ledger**
   - Set M01 Status: `Completed`
   - Set M01 Branch: `m01-ci-truthfulness`
   - Set M01 PR: (create PR when ready to merge)
   - Set M01 Commit: latest on m01-ci-truthfulness (e.g. 2f664049)
   - Set CI Run(s): Linter 22814396752 ✓; Tests 22814850488 (server ✓, 17 tests pass, img2img/txt2img 500 expected)
   - Set Audit Score: 4.7 / 5
   - Set Completed At: 2026-03-08

2. **Create PR** (optional, when ready)
   - Branch: m01-ci-truthfulness → main
   - Title: "M01: CI truthfulness, stub repositories, deterministic CI"
   - Body: Reference M01_summary.md, M01_audit.md

3. **Tag milestone** (after merge)
   - `git tag -a m01-complete -m "M01: CI truthfulness, stub repos, deterministic CI"`

## Evidence

- Linter: PASS
- Server startup: PASS (port 7860)
- Tests: 17 pass (extras, face_restorers, torch_utils, utils)
- img2img/txt2img: 500 (expected — stub model, no inference)
- No external clones, deterministic stub repositories
```

---

## Context

M01 achieved:
- Deterministic CI without external repo clones
- Dynamic stub loader for ldm/sgm (no whack-a-mole imports)
- Server boots and binds to 7860
- Test runner executes; failures are semantic (stub model), not infrastructure

Remaining img2img/txt2img failures are **intentional** for M01 scope. M02 will address API-layer truthfulness (e.g. fake inference).
