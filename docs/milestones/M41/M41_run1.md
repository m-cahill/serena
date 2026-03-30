# M41 — Run 1 (preflight)

## Baseline (pre-implementation)

- **Binding Quality (post–M40 doc closeout):** run **`23722553628`** — **243** pass, **49%** TOTAL, gate **42%** unchanged (`docs/serena.md`).
- **Performance:** `scripts/ci/write_performance_snapshot.py` produces **`performance_snapshot.txt`**; no regression check before M41.
- **Workflows:** No explicit `permissions:` blocks; Nightly used **`pip-audit || true`** before full install.
- **Targets this run:** warn-first check, permissions, Nightly/Smoke artifacts, README, `opts_snapshot.py`, `processing.py` ValueError.

## CI results

*(Fill after PR / merge: Linter / Smoke / Quality run IDs and outcomes.)*
