# M41 — Final performance guardrails and release polish

## Objective

Add a **truthful, warn-first** performance regression signal on Quality (M29 snapshot + baseline comparison), align workflow security and `pip-audit` posture with governance docs, improve onboarding (README, `opts_snapshot.py` comment), and keep code-health edits to **Serena-governed** surfaces only (`processing.py`).

## In scope

- `scripts/ci/check_performance_regression.py` + `scripts/ci/performance_snapshot_baseline.txt`; Quality step after `write_performance_snapshot.py`.
- Explicit workflow permissions (`contents: read`, `actions: write` for artifact uploads).
- Nightly: blocking `pip-audit` with same `--ignore-vuln` as Quality; report artifact; JUnit upload.
- Smoke: JUnit artifact upload.
- README Serena identity block; `modules/opts_snapshot.py` header.
- `raise ValueError` for missing refiner checkpoint in `processing.py` (was `Exception`).

## Out of scope

- Bare `except:` in upstream training modules.
- `raise Exception` cleanup outside Serena-governed surfaces (e.g. not `sd_models.py` / `sd_vae.py` in this milestone).
- Blocking performance gate, branch coverage gate, `processing_types.py` split.

## Definition of done

- PR: Linter + Smoke green; post-merge Quality green on `main`.
- Closeout: `M41_summary.md`, `M41_audit.md`, ledger update in `docs/serena.md` with UTC completion time.
