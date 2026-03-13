# M13 — txt2img Execution via Runner

Phase: Phase III — Runner & Service Boundary  
Status: Planned

---

# 1. Intent / Target

Route the **txt2img execution path** through `ProcessingRunner` explicitly.

Right now the runner exists but is still only used by the internal `process_images` wrapper. M13 makes the runner the **true execution surface** for txt2img while preserving behavior.

### Architectural impact

Before:

```
UI/API
   │
process_images
   │
runner
```

After:

```
UI/API
   │
Runner
   │
Pipeline
```

This begins the **UI/runtime separation** that Serena is aiming for.

---

# 2. Scope Boundaries

## In scope

• Route txt2img path via runner  
• Preserve existing request objects  
• No UI or API behavior changes

## Out of scope

• API runner  
• queue runner  
• cancellation  
• progress reporting

---

# 3. Invariants

| Surface       | Requirement   | Verification |
|---------------|---------------|--------------|
| CLI behavior  | unchanged     | smoke tests  |
| API responses | unchanged     | smoke tests  |
| Output images | identical     | quality tests|
| Extensions    | unaffected    | extension tests |

---

# 4. Verification Plan

CI must remain green.

Expected checks:

| Check | Expected |
|-------|----------|
| Linter | pass |
| Smoke Tests | pass |
| Quality Tests | pass (post-merge) |
| Coverage | ≥ 40% |

---

# 5. Implementation Steps

1. **Verify routing** — txt2img path calls `process_images` only; no direct `process_images_inner` in `modules/txt2img.py`. ✓
2. **Confirm delegation** — `process_images` delegates to `ProcessingRunner().run(ProcessingRequest(p))` inside profiler block. ✓
3. **Add contract test** — `test/quality/test_txt2img_runner_contract.py` verifies txt2img path invokes runner. ✓
4. **No routing changes required** — Runner already sits behind `process_images` (M10–M12). Verification milestone.

Key principle: txt2img call path must flow through `ProcessingRunner.run()` while preserving identical behavior.

---

# 6. Risk & Rollback Plan

Risk level: **Low** (routing verification milestone; runner already used by process_images)

Rollback: revert txt2img routing commit; restore direct process_images path.

---

# 7. Deliverables

Code:

```
modules/runtime/runner.py
modules/processing.py
```

Tests:

```
test/quality/test_processing_runner.py
test/quality/test_txt2img_runner_contract.py  # M13 contract test
```

Docs:

```
docs/milestones/M13/M13_plan.md
docs/milestones/M13/M13_toolcalls.md
docs/milestones/M13/M13_run1.md
docs/milestones/M13/M13_summary.md
docs/milestones/M13/M13_audit.md
```

Ledger:

```
docs/serena.md
```

Tag:

```
v0.0.13-m13
```

---

# 8. Exit Criteria

M13 closes when:

• PR CI passes  
• post-merge Quality Tests pass  
• txt2img routed through runner merged  
• ledger updated  
• tag created
