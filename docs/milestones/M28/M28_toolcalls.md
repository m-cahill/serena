# M28 — Tool calls log

**Branch:** `m28-security-supply-chain`  
**Started:** 2026-03-24 (M28a kickoff)

| Timestamp (UTC) | Tool / action | Purpose | Targets |
|-----------------|---------------|---------|---------|
| 2026-03-24T22:30Z | git (fetch/status/checkout/branch) | Sync `main`, create `m28-security-supply-chain` for M28a | repo root |
| 2026-03-24T22:31Z | pip / pip-audit (local baseline) | Capture `baseline_audit.txt` after CI-equivalent install | `requirements-ci.txt`, CLIP, `baseline_audit.txt` |
| 2026-03-24T22:32Z | edit | M28a: Quality `pip-audit` blocking; contract + guardrails | `.github/workflows/run_quality_tests.yaml`, `docs/architecture/ci_environment_contract.md`, `docs/PR_guardrail_checklist.md` |
| 2026-03-24T22:33Z | write | M28a evidence: `M28_run1.md` baseline + enforcement note | `docs/milestones/M28/M28_run1.md` |
| 2026-03-24T22:40Z | git | Commit M28a (workflow + contract + baseline + run log) | branch `m28-security-supply-chain` |
| 2026-03-25T00:00Z | edit | M28b batch 1: HTTP stack constraints in `requirements-ci.in` | `requirements-ci.in` |
| 2026-03-25T00:01Z | uv | Regenerate `requirements-ci.txt` (manylinux 3.10) | `requirements-ci.in` → `requirements-ci.txt` |
| 2026-03-25T00:02Z | bash | Determinism: `verify_pinned_deps.sh` | `requirements-ci.txt`, `dependency_snapshot.txt` |
| 2026-03-25T00:03Z | pytest | Sanity: smoke + quality (skipped locally — no full CI venv) | — |
| 2026-03-25T00:04Z | pip-audit | Compare audit vs baseline (HTTP cluster) | `requirements-ci.txt` |
| 2026-03-25T00:06Z | git | Commit M28b batch 1 | `requirements-ci.*`, `ci_environment_contract.md`, `M28_run1.md` |
| 2026-03-25T12:00Z | edit | M28b batch 2: Pillow pin `>=10.3,<11` in `requirements-ci.in` | `requirements-ci.in` |
| 2026-03-25T12:01Z | uv | Recompile lock (HTTP + pillow `--upgrade-package`) | `requirements-ci.txt` |
| 2026-03-25T12:02Z | pip-audit | Measure findings after pillow bump | `requirements-ci.txt` |
| 2026-03-25T12:03Z | read / search | Pillow touchpoints: `modules/images.py`, `modules/extras.py`, tests | — |
| 2026-03-25T12:04Z | git | Commit M28b batch 2 | `requirements-ci.*`, `M28_run1.md`, `M28_toolcalls.md` |

*(Append entries before significant tool invocations per `.cursorrules`.)*
