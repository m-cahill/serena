# M40 — Run 1 (baseline and implementation record)

## A. Pre-M40 binding baseline (from ledger)

| Metric | Value | Source |
|--------|-------|--------|
| Quality tests (pass count) | 222 | `docs/serena.md` Phase IX (M39 binding `main`) |
| Total coverage (pytest-only) | ~48% | Same |
| Coverage gate (`--fail-under`) | 42% | `.github/workflows/run_quality_tests.yaml` |

Per-file coverage for target modules is recorded **after** the first full Quality run that includes M40 tests (post-merge on `main` is authoritative per program contract).

## B. Target modules (M40 scope)

| Priority | Module |
|----------|--------|
| A | `modules/processing_helpers.py` |
| A | `modules/processing_infotext.py` |
| A | `modules/processing_types.py` |
| B | `modules/runtime/processing_runtime.py` |

## C. Tests added (this branch)

New Quality tests:

- `test/quality/test_m40_processing_helpers.py` — pure helpers, `_EffOptsView` / `_eff_opts`, `_orchestration_model`, masks, overlay, uncrop, random tensors
- `test/quality/test_m40_processing_infotext.py` — `program_version`, `create_infotext` smoke
- `test/quality/test_m40_processing_runtime.py` — empty prompt batch exit; preview / Approx NN branch calls `sd_vae_approx.model`
- `test/quality/test_m40_processing_types.py` — `get_token_merging_ratio` (hr / non-hr)

**Note:** Each `test_m40_*.py` file uses `try: import modules.<target> … except ImportError: pytest.skip(…, allow_module_level=True)` so minimal local venvs without the full `requirements-ci.txt` tree skip the whole file without failing collection. **Quality CI** installs the full tree and executes all M40 tests.

## D. Post-merge slot (fill after binding Quality on `main`)

| Metric | Value |
|--------|-------|
| Quality workflow run ID | TBD |
| Pass count | TBD |
| Total % | TBD |
| Gate | 42% (unchanged unless earned) |

Per-file before/after for targets: TBD (from `coverage report` artifact).
