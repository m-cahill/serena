# Phase I Summary — Baseline & Guardrails

**Phase:** Phase I — Baseline & Guardrails  
**Milestone Range:** M00–M04  
**Timeframe:** 2026-03-07 → 2026-03-09  
**Overall Outcome:** Baseline frozen, CI truthfulness established, test architecture introduced, coverage/security gates enforced

---

## 1. Why This Phase Existed

Phase I addressed the **foundational safety problem** for the Serena refactor program:

* No immutable baseline tag for audit verification
* No truthful CI (tests failing due to dependency/stub issues)
* No test tier separation (smoke vs quality vs nightly)
* No coverage gate or security scanning
* No reproducibility verification

**Architectural pressure relieved:** Made the codebase safe to refactor by establishing CI truthfulness, coverage enforcement, and reproducible verification flows.

---

## 2. Milestone-by-Milestone Progression

### M00 — Program Kickoff, Baseline Freeze, Phase Map, E2E Verification

**What changed:**
* Created immutable baseline tag `baseline-pre-refactor` at SHA `82a973c04367123ae98bd9abdf80d9eda9b910e2`
* Created `docs/serena.md` governance ledger
* Defined seven-phase roadmap (M00–M32)
* Documented CI architecture and E2E verification commands

**Why it mattered:**
* Established source of truth and audit anchor
* Locked baseline against drift

**Invariant added:**
* Immutable baseline tag for audit verification

---

### M01 — CI Truthfulness, SHA Pinning, Smoke Path

**What changed:**
* Fixed CLIP/pkg_resources failure with `--no-build-isolation`
* Introduced dynamic stub loader (`_StubFinder`, `_StubModule`) for `ldm.*` and `sgm.*` imports
* SHA-pinned all GitHub Actions
* Added `--skip-prepare-environment` for deterministic CI bootstrap
* Server startup verified (binds to port 7860)
* 17 tests passed; txt2img/img2img returned 500 (expected; stub model cannot perform inference)

**Why it mattered:**
* Eliminated external repository dependencies (no network, no clones)
* Made CI deterministic and truthful

**Invariant added:**
* CI runs deterministically without external network dependencies
* All GitHub Actions SHA-pinned

---

### M02 — API CI Truthfulness, Local Dev Guardrails

**What changed:**
* Introduced CI fake inference: `ci_fake_txt2img()` and `ci_fake_img2img()` return 1×1 deterministic PNG when `CI=true`
* API contract tests verify HTTP 200 and response schema without real model inference
* Created `CONTRIBUTING.md` with quickstart, local verification, CI parity documentation
* Coverage gate enforced at 33% baseline (current coverage − 2% margin)
* All 33 tests passed

**Why it mattered:**
* Enabled API contract testing without model loading
* Established local dev parity with CI

**Invariant added:**
* API response schema verified without model inference in CI
* Coverage gate enforced (baseline 33%)

---

### M03 — Test Architecture (Smoke / Quality / Nightly)

**What changed:**
* Migrated 6 test files to `test/smoke/` (33 tests, < 60 sec)
* Scaffolded `test/quality/` and `test/nightly/` with `.gitkeep`
* Created `pytest.ini` with markers (`smoke`, `quality`, `nightly`)
* Path-based marker application via `conftest.py`
* Introduced three CI workflows:
  * `run_smoke_tests.yaml` — PR only, no coverage gate
  * `run_quality_tests.yaml` — push to main, coverage gate 33%
  * `run_nightly_tests.yaml` — cron + workflow_dispatch
* Added pre-push hook (`prevent_upstream_push.sh`)

**Why it mattered:**
* Separated test tiers by purpose and speed
* Enabled fast PR feedback (smoke) and thorough post-merge verification (quality)

**Invariant added:**
* Test tier structure: smoke (PR), quality (push to main + coverage gate), nightly (informational)
* Pre-push hook prevents accidental push to upstream

---

### M04 — Coverage / Security / Reproducibility Guardrails

**What changed:**
* Raised coverage gate from 33% → 40%
* Integrated `pip-audit` in Quality Tests (informational; remediation deferred to M27)
* Added reproducibility verification: `verify_pinned_deps.sh`
* Configured coverage omit patterns in `pyproject.toml` (extensions-builtin, repositories, scripts, deepbooru)
* Added CI artifact capture: `coverage.xml`, `ci_environment.txt`
* Added quality unit tests: `test_util_modules`, `test_api_extended`

**Why it mattered:**
* Enforced coverage baseline and security scanning
* Locked reproducibility via pinned dependency verification

**Invariant added:**
* Coverage gate ≥40%
* `pip-audit` runs in Quality Tests (informational)
* Pinned dependencies verified via `verify_pinned_deps.sh`

---

## 3. Net Architectural Effect

**Before Phase I:**
* No baseline tag
* CI failing or flaky
* No test tiers
* No coverage gate
* No security scanning
* No reproducibility checks

**After Phase I:**
* Immutable baseline tag (`baseline-pre-refactor`)
* CI truthful and deterministic (dynamic stubs, fake inference)
* Test architecture established (smoke / quality / nightly)
* Coverage gate enforced (≥40%)
* Security scanning integrated (`pip-audit`)
* Reproducibility verified (`verify_pinned_deps.sh`)

---

## 4. Guardrails / Invariants Established

| Invariant | Enforcement |
|-----------|-------------|
| Immutable baseline tag | `baseline-pre-refactor` at SHA `82a973c0` |
| CI determinism | Dynamic stubs; no external network dependencies |
| GitHub Actions SHA-pinned | All actions use SHA, not tags |
| API response schema stability | CI fake inference; contract tests |
| Test tier separation | smoke (PR), quality (main + coverage), nightly (cron) |
| Coverage gate | ≥40% combined (server + pytest) |
| Security scanning | `pip-audit` (informational) |
| Reproducibility | `verify_pinned_deps.sh` |
| Pre-push hook | Prevents accidental upstream push |

---

## 5. Key Files / Modules Introduced or Changed

**Introduced:**
* `docs/serena.md` — Governance ledger and source of truth
* `docs/milestones/M00/*` — Baseline docs (preflight, e2e, ci_inventory)
* `CONTRIBUTING.md` — Local dev and CI parity guide
* `scripts/ci/verify_pinned_deps.sh` — Reproducibility verification
* `scripts/dev/create_stub_repos.py` — Dynamic stub loader for CI
* `modules/ci_fake_inference.py` — Fake inference for API contract tests
* `pytest.ini` — Test markers (smoke, quality, nightly)
* `.github/workflows/run_smoke_tests.yaml` — PR smoke tests
* `.github/workflows/run_quality_tests.yaml` — Main push quality tests + coverage
* `.github/workflows/run_nightly_tests.yaml` — Scheduled/manual nightly tests
* `pyproject.toml` — Coverage configuration

**Changed:**
* `.github/workflows/` — All actions SHA-pinned
* `modules/launch_utils.py` — `--no-build-isolation` for CLIP
* `webui.py` — `--skip-prepare-environment` support
* `modules/api/api.py` — CI fake inference guards

---

## 6. Deferred Work Handed to Phase II

* Runtime seam preparation (temporary opts, prompt/seed prep, opts snapshot, execution context)
* ProcessingRunner introduction
* Shared state reduction
* Extension API versioning

---

## 7. Agent Context / How to Think About the Repo Now

### Where the safe seams are

These guardrails are **refactor safety invariants**, not merely CI mechanics. Weakening them is architecturally significant.

* **CI workflows:** Smoke (PR), Quality (main), Nightly (cron) — do not weaken coverage gate or checks
* **Test tiers:** `test/smoke/` for fast PR feedback; `test/quality/` for post-merge depth
* **Coverage enforcement:** ≥40% combined (server + pytest) — do not relax without explicit milestone approval
* **Reproducibility:** `verify_pinned_deps.sh` ensures pinned dependencies match lockfiles

### What not to disturb

* Immutable baseline tag (`baseline-pre-refactor`)
* SHA-pinned GitHub Actions
* CI fake inference guards (must preserve API contract testing without model loading)
* Dynamic stub loader (`scripts/dev/create_stub_repos.py`)
* Test tier separation (smoke/quality/nightly)

### Which patterns are now established

* **Behavior-preserving by default:** All refactors must preserve existing runtime behavior unless explicitly approved
* **Evidence-based closeout:** Every milestone closes with CI evidence (linter, smoke, quality)
* **Small milestones:** Minimal surface change per milestone
* **Coverage gate enforcement:** ≥40% combined coverage; no relaxation

### What Phase II is expected to build on

Phase II will introduce **runtime seam preparation**:
* Override isolation (temporary opts)
* Prompt/seed prep extraction
* Opts snapshot introduction and threading
* Execution context (RuntimeContext)

Phase I established the **safety foundation** (CI truthfulness, coverage, reproducibility). Phase II will introduce the **runtime seams** needed for Phase III ProcessingRunner and Phase IV runtime extraction.

---

## 8. Phase-end Truth State

Facts a future agent may assume after Phase I:

* Immutable baseline tag exists at `baseline-pre-refactor`
* CI is truthful and deterministic (dynamic stubs, fake inference)
* Test tiers: smoke (PR), quality (main + coverage gate), nightly (cron)
* Coverage gate enforced at ≥40% combined
* Security scanning (`pip-audit`) and reproducibility (`verify_pinned_deps`) run in Quality tier
