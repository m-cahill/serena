# PR guardrail checklist (Serena)

Use before opening or merging a PR. This complements CI and `docs/serena.md` invariants.

## Repository and target

- [ ] PR targets **`main`** on **`m-cahill/serena`** (not upstream).
- [ ] No unintended changes under **`modules/runtime/`**, **`process_images`**, extension callback semantics, or extension API contracts unless the milestone explicitly allows it.

## Dependencies and lockfiles (M26+)

- [ ] **`package-lock.json`** is present, committed, and consistent with `package.json` (run **`npm ci`** locally when possible).
- [ ] CI / docs use **`npm ci`**, not ad-hoc **`npm install`** in workflows.
- [ ] **Quality CI** installs the locked tree from **`requirements-ci.txt`** and uses the **documented pinned CLIP URL + `pip` flags** from `run_quality_tests.yaml` (do not ad‑hoc change or drop the CLIP step without a milestone).
- [ ] If you change Python deps for CI, regenerate **`requirements-ci.txt`** from **`requirements-ci.in`** per `docs/architecture/ci_environment_contract.md`.

## CI truthfulness

- [ ] Do not add **`continue-on-error`**, skipped checks, or lowered thresholds to “get green” without a milestone decision.
- [ ] Coverage gate remains **≥ 40%** until a later milestone changes it.

## Evidence

- [ ] Smoke / Linter / Quality (as applicable) are green on the PR branch.
- [ ] Milestone toolcalls / run notes updated when required by `.cursorrules`.
