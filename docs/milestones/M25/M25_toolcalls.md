# M25 Tool call log — Deprecation & compatibility scaffolding

**Milestone:** M25  
**Branch:** `m25-deprecation-compat-scaffolding`  
**Started:** 2026-03-22 UTC

Log format: timestamp (UTC), tool, purpose, files/target, status.

---

| Timestamp (UTC) | Tool | Purpose | Files / target | Status |
|-----------------|------|---------|----------------|--------|
| 2026-03-22 | (init) | Stub folder at M24 closeout | this file | done |
| 2026-03-22 | git | Create M25 branch | `m25-deprecation-compat-scaffolding` | done |
| 2026-03-22 | write | Add `modules/deprecation.py` | deprecation utilities | done |
| 2026-03-22 | apply_patch | M25 block + `deprecate_callback` in `script_callbacks.py` | `modules/script_callbacks.py` | done |
| 2026-03-22 | write | Architecture policy doc | `docs/architecture/extension_api_deprecation_policy.md` | done |
| 2026-03-22 | write | Quality tests | `test/quality/test_deprecation_scaffolding.py` | done |
| 2026-03-22 | apply_patch | Ledger M25 in progress | `docs/serena.md` | done |
| 2026-03-22 | pytest | Run new quality tests | `test/quality/test_deprecation_scaffolding.py` | done |
| 2026-03-23 | gh / write | CI monitor PR #44; write run report | `docs/milestones/M25/M25_run1.md` | done |
| 2026-03-23 | git / write | M25 closeout: ledger, summary, audit; M26 stubs; tag `v0.0.25-m25` on merge SHA | `docs/serena.md`, `M25_*`, `M26/*` | done |
