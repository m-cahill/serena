# M26 — Locked Manifests & CI Environment Stabilization

**Branch:** `m26-locked-manifests-ci-env`  
**Status:** In progress

## 1. Intent

Establish **reproducible, deterministic Quality CI** (Python) and **locked npm installs** (Linter) by:

- Locking Python dependency resolution for the **Quality workflow only** via `requirements-ci.txt`
- Committing `package-lock.json` and using **`npm ci`** in Linter
- Strengthening CI truthfulness (no `continue-on-error` on supply-chain scan where policy allows hard fail)
- Documenting the environment contract and PR guardrails

**Phase VI foundation:** CI moves from “truthful” toward **provably reproducible** for the Quality tier.

## 2. Scope

### In scope

- `requirements-ci.txt` (+ `requirements-ci.in` as maintainable input for `uv pip compile`)
- Quality workflow: single `pip install -r requirements-ci.txt` (plus documented exception for `pip-audit` installer)
- `verify_pinned_deps.sh` extended for lockfile + `dependency_snapshot.txt`
- Artifacts: `pip_freeze.txt`, `dependency_snapshot.txt`, `npm_ls.json` (Linter)
- `docs/architecture/ci_environment_contract.md`
- Update `docs/PR_guardrail_checklist.md`
- `.gitignore`: stop ignoring `package-lock.json`

### Out of scope (locked by user)

- **Smoke / Linter / Nightly Python paths** — unchanged install sequence (M26 = Quality Python only)
- Runtime: `modules/runtime/*`, `process_images`, callbacks, extension API
- Coverage threshold changes (M27)
- Pinning Node via `.nvmrc` (use `setup-node` as today)

## 3. Invariants

| Surface | Invariant |
|--------|-----------|
| Runtime / API | No functional changes to generation pipeline or extensions |
| Coverage | Combined report **≥ 40%** unchanged |
| Test layout | smoke / quality / nightly structure unchanged |
| Lockfiles | Committed; CI fails if missing; fixes go to lockfile/manifest, not gates |

## 4. Verification

- Smoke (PR): pass
- Quality (push `main`): pass with ≥ 40% coverage
- Linter: `npm ci`, eslint pass
- `verify_pinned_deps.sh` passes against `requirements-ci.txt`
- Reproducibility claims documented in `ci_environment_contract.md`

## 5. Rollback

Revert: `requirements-ci.txt`, `requirements-ci.in`, `package-lock.json`, workflow edits, script changes, new docs. CI returns to pre-M26 install paths.

## 6. Definition of done

- Quality installs **only** from `requirements-ci.txt` for application/test runtime deps (with documented `pip-audit` bootstrap)
- `npm ci` + committed lockfile for JS lint
- No `continue-on-error` on `pip-audit` in Quality
- Governance: `docs/serena.md` updated after green CI + permission
- Audit / summary per prompts (post-closeout)
