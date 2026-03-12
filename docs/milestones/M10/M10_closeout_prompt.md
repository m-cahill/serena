# M10 Closeout Prompt for Cursor

**Use this once PR CI is green against m-cahill/serena.**

---

```
M10 PR CI is complete.

Proceed with M10 closeout.

Steps:

1. Verify CI status
   - Linter ✓
   - Smoke Tests ✓

2. Merge PR into main.

3. Monitor post-merge CI:
   - Quality Tests must pass.

4. Generate milestone artifacts:

docs/milestones/M10/M10_run2.md
docs/milestones/M10/M10_summary.md
docs/milestones/M10/M10_audit.md

5. Update ledger:

docs/serena.md

Add row:

| M10 | ProcessingRunner skeleton | Closed | m10-processing-runner | PR # | <merge_commit> | <quality_run_id> | 5.0 |

6. Create tag:

v0.0.10-m10

7. Push tag.

Follow the RefactorWorkflowPrompt and RefactorSummaryPrompt formats.
```
