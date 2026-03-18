# M15 Run 2 — Post-Merge CI Analysis

**Milestone:** M15 — Queue / background runner preparation  
**Merge commit:** a4b9a622  
**PR:** [#33](https://github.com/m-cahill/serena/pull/33) (merged)

---

## 1. Post-Merge Workflows

| Workflow | Run ID | Trigger | Result | Duration |
|----------|--------|---------|--------|----------|
| Linter | (PR run) | PR #33 | ✓ success | — |
| Smoke Tests | (PR run) | PR #33 | ✓ success | — |
| Quality Tests | [23232040072](https://github.com/m-cahill/serena/actions/runs/23232040072) | push to main | ✓ success | 4m 0s |

---

## 2. Quality Tests Job Details

| Step | Result |
|------|--------|
| Verify repository, ref | ✓ |
| Checkout Code | ✓ |
| Set up Python 3.10 | ✓ |
| Install dependencies | ✓ |
| Dependency vulnerability scan | ✓ (continue-on-error; pip-audit deferred to M27) |
| Verify pinned dependencies | ✓ |
| Setup environment | ✓ |
| Start test server | ✓ |
| **Run quality tests** (smoke + quality) | ✓ |
| **Show coverage** | ✓ (≥40% enforced) |
| Upload artifacts | ✓ |

---

## 3. Post-Merge Fixes

Quality Tests failed on initial merge (Run 23231812010) due to pre-existing `test_api_txt2img_uses_runner` failure: Api constructor requires `scripts_txt2img`/`scripts_img2img` but initialize fixture did not run full `initialize.initialize()`.

**Fixes applied:**
- `fix(test): ensure scripts loaded before Api()` — reverted (insufficient)
- `fix(test): run full initialize in conftest` — conftest now calls `init_mod.initialize()` so quality tests get full env for Api construction

---

## 4. Evidence Summary

| Check | Expected | Actual |
|-------|----------|--------|
| Smoke Tests (PR) | ✓ | ✓ Run 1 |
| Linter (PR) | ✓ | ✓ Run 1 |
| Quality Tests (post-merge) | ✓ | ✓ Run 2 (after fix) |
| Coverage | ≥ 40% | ✓ (gate passed) |

---

## 5. Annotations (Informational)

* Node.js 20 actions deprecation — informational; not merge-blocking
* pip-audit vulnerabilities — deferred to M27 per M04_audit.md

---

## 6. Conclusion

**Run 2 status: ✓ GREEN.** Post-merge Quality Tests passed after conftest fix. Coverage gate met. M15 closeout complete.
