# M20 Run 1 — PR CI Analysis

**Milestone:** M20 — Runtime tests with mockable boundaries  
**Phase:** Phase IV — Runtime Extraction  
**Run type:** PR (pre-merge)  
**Branch:** m20-runtime-mock-tests  
**PR:** [#39](https://github.com/m-cahill/serena/pull/39)  
**Commit:** d666e090

---

## 1. Workflow identity

| Field | Value |
|-------|-------|
| Trigger | pull_request |
| Branch | m20-runtime-mock-tests |
| Base | main |
| Run date | 2026-03-20 (UTC) |

---

## 2. Workflow inventory (PR phase)

[Quality Tests](https://github.com/m-cahill/serena/blob/main/.github/workflows/run_quality_tests.yaml) run only on `push` to `main`. PR validation is **Linter** + **Smoke**.

| Job / Check | Run ID | Required? | Purpose | Result | Duration |
|-------------|--------|-----------|---------|--------|----------|
| Linter (ruff + eslint) | [23331851493](https://github.com/m-cahill/serena/actions/runs/23331851493) | Yes | Python + JS lint | ✓ SUCCESS | ~18s |
| Smoke Tests | [23331851499](https://github.com/m-cahill/serena/actions/runs/23331851499) | Yes | Server startup + smoke | ✓ SUCCESS | 2m38s |

**Job URLs (detail):**

- ruff: [67864938320](https://github.com/m-cahill/serena/actions/runs/23331851493/job/67864938320) (~7s)
- eslint: [67864938326](https://github.com/m-cahill/serena/actions/runs/23331851493/job/67864938326) (~14s)
- smoke tests: [67864938352](https://github.com/m-cahill/serena/actions/runs/23331851499/job/67864938352) (~2m38s)

---

## 3. Runtime-mock tests (PR phase)

`test/quality/test_runtime_mock.py` is **not** executed in Linter or Smoke. It runs in **Quality** (`pytest test/smoke test/quality`) after merge to `main`.

**Local developer note:** Full `initialize` / webui stack may be missing pieces (e.g. torchvision) on some machines; **CI is the source of truth** for quality + coverage.

---

## 4. Refactor signal integrity

### A) Tests (this phase)

- **Smoke:** Server startup; existing smoke paths (txt2img / img2img, etc.).
- **Coverage / `test_runtime_mock`:** Deferred to post-merge Quality.

### B) Static gates

- **Ruff:** Passed.
- **ESLint:** Passed.

### C) Change impact

- **Modified surface:** `test/fixtures/fake_model.py`, `test/quality/test_runtime_mock.py`, `docs/milestones/M20/*`.
- **Runtime modules:** Unchanged (validation-only milestone).

---

## 5. Conclusion

| Gate | Status |
|------|--------|
| Linter | ✓ |
| Smoke | ✓ |
| Quality | Pending (post-merge to `main`) |

**Verdict:** PR CI green for Linter and Smoke. Record Quality run ID, test count, and coverage in `M20_run2.md` after PR #39 merges and **Quality Tests** completes on `main`.

---

## 6. Annotations

- Node.js 20 deprecation warnings on GitHub Actions (informational; not blocking).

---

## 7. Post-merge note

After PR #39 merged, **Quality** on `main` initially failed on `test_runtime_mock` (dataclass `scripts` init, then CI-specific glue). **Test-only** commits on `main` resolved this; see **`M20_run2.md`** for the authoritative green run (**23333740069**) and SHA **`9c7e693a`**.
