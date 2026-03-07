# M01 Tool Calls Log

| Timestamp | Tool | Purpose | Files/Target | Status |
|-----------|------|---------|--------------|--------|
| 2025-03-07 | run | git checkout -b m01-ci-truthfulness | Create M01 branch from main | done |
| 2025-03-07 | write | Create M01_plan.md, M01_toolcalls.md | Milestone docs | done |
| 2025-03-07 | search_replace | Remove same-repo PR condition | .github/workflows/on_pull_request.yaml, run_tests.yaml | done |
| 2025-03-07 | search_replace | Add setuptools, pip-audit, --do-not-download-clip, smoke step, coverage threshold | .github/workflows/run_tests.yaml | done |
| 2025-03-07 | search_replace | Pin actions to SHAs | .github/workflows/*.yaml | done |
| 2025-03-07 | write | Create .gitattributes | .gitattributes | done |
| 2025-03-07 | search_replace | Update milestone ledger | docs/serena.md | done |
| 2025-03-07 | run | git push, CI run 22809624907 | Tests failed at Setup env (CLIP pkg_resources) | done |
| 2025-03-07 | search_replace | Add PIP_NO_BUILD_ISOLATION for CLIP build | .github/workflows/run_tests.yaml | done (reverted - env not passed to pip subprocess) |
| 2025-03-07 | search_replace | Add --no-build-isolation to clip install in launch_utils | modules/launch_utils.py | done |
