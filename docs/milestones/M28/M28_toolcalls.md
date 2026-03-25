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
| 2026-03-25T14:00Z | edit | M28b batch 3: FastAPI / Starlette / h11 pins in `requirements-ci.in` | `requirements-ci.in` |
| 2026-03-25T14:01Z | uv | Recompile lock (prior batches + fastapi/starlette/h11) | `requirements-ci.txt` |
| 2026-03-25T14:02Z | pip-audit / read | Audit delta; skim `api.py`, `test_api_extended.py` | — |
| 2026-03-25T14:03Z | git | Commit M28b batch 3 | `requirements-ci.*`, `M28_run1.md`, `M28_toolcalls.md` |
| 2026-03-25T16:00Z | edit | M28b batch 4: setuptools / wheel / filelock / GitPython in `requirements-ci.in` | `requirements-ci.in` |
| 2026-03-25T16:01Z | uv | Recompile lock (+ `--upgrade-package` for batch 4) | `requirements-ci.txt` |
| 2026-03-25T16:02Z | pip-audit | Audit count after tooling bump | `requirements-ci.txt` |
| 2026-03-25T16:03Z | git | Commit M28b batch 4 | `requirements-ci.*`, `M28_run1.md`, `M28_toolcalls.md` |
| 2026-03-25T18:00Z | edit | M28b batch 5a: Pillow 12 + required graph (numpy2, blendmodes 2025, gradio 6.5) | `requirements-ci.in` |
| 2026-03-25T18:01Z | uv | Recompile lock (full `--upgrade-package` list incl. numpy/gradio/blendmodes) | `requirements-ci.txt` |
| 2026-03-25T18:02Z | pip-audit | Audit after Pillow 12 line | `requirements-ci.txt` |
| 2026-03-25T18:03Z | git | Commit M28b batch 5a | `requirements-ci.*`, `M28_run1.md`, `M28_toolcalls.md` |
| 2026-03-26T00:00Z | pytest / import | M28b 5a stabilization: surface Gradio 6 / NumPy 2 failures | `test/quality`, `modules/ui*.py` |
| 2026-03-26T00:01Z | edit | Minimal compatibility fixes (no broad UI rewrite) | TBD from failures |
| 2026-03-26T00:02Z | git | Commit stabilization (Gradio 6 shim + tempdir guard) | `gradio_extensons.py`, `ui_tempdir.py`, `script_callbacks.py` |
| 2026-03-26T12:00Z | edit + uv | M28b 5b step 1: `protobuf>=5,<6` | `requirements-ci.in`, `requirements-ci.txt` |
| 2026-03-26T12:01Z | git | `m28b: upgrade protobuf` | — |
| 2026-03-26T12:02Z | edit + uv | M28b 5b step 2: `pytorch_lightning>=2.2,<3` | `requirements-ci.in`, `requirements-ci.txt` |
| 2026-03-26T12:03Z | git | `m28b: upgrade pytorch-lightning` | — |
| 2026-03-26T12:04Z | edit + uv | M28b 5b step 3: `transformers>=4.57,<5` + **`safetensors>=0.4.3`** (required by transformers 4.57.x) + **`gradio>=6.7`** (CVE fixes; resolved **6.10.0**) | `requirements-ci.in`, `requirements-ci.txt` |
| 2026-03-26T12:05Z | pip-audit | Audit after ML stack: **2** remaining (**diskcache**, **pygments** — no fix on PyPI yet) | `requirements-ci.txt` |
| 2026-03-26T12:06Z | git | `m28b: upgrade transformers` (+ co-bumps) + `M28_run1.md` deferrals | — |
| 2026-03-26T14:00Z | read / edit | M28 finalization: contract **pip-audit deferrals (M28)**, `M28_run1.md` gate section, PR checklist, **`M28_summary.md`**, **`M28_audit.md`**, **`docs/serena.md`** | governance docs |
| 2026-03-26T14:01Z | git | `m28: finalize M28 (deferrals, docs, tag v0.0.28-m28)` | — |
| 2026-03-26T14:02Z | git | `m28: serena M28 ledger short hash` | `docs/serena.md` |
| 2026-03-26T14:03Z | git | `git tag -a v0.0.28-m28`; `git push origin v0.0.28-m28` | `c97c4067820210f9c55e8fa56d363ddb21fdb547` |

*(Append entries before significant tool invocations per `.cursorrules`.)*
