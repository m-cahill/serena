# M28 — Audit verdict

**Milestone:** M28 — Security & supply-chain evidence  
**Verdict:** **5.0 / 5**

---

## Criteria

| Criterion | Assessment |
|-----------|------------|
| **Security enforcement active** | **Yes** — Quality **`pip-audit`** is **blocking** (**M28a+**); job **fails** on any advisory **except** the **two** documented **`--ignore-vuln`** IDs. |
| **Vulnerabilities resolved or explicitly deferred** | **Yes** — M28b upgrades cleared **resolvable** CVEs; **diskcache** / **pygments** are **named**, **reasoned**, and **time-limited** deferrals (**no PyPI fix**). |
| **No CI weakening** | **Yes** — No `continue-on-error` on audit, coverage floor **≥42%** unchanged, **`set -o pipefail`** on the audit step. |
| **Behavior preserved** | **Yes** — Changes are **dependency alignment** and **minimal adapters** where required (documented in **`M28_run1.md`**); no milestone scope for generation/API semantics drift. |
| **Determinism intact** | **Yes** — Locked **`requirements-ci.txt`**, **verify_pinned_deps**, **CLIP** install contract unchanged in intent. |

---

## Governance note

This milestone follows the enterprise pattern: **fix what you can**, **document what you cannot** (with removal criteria), **enforce everything else**. The audit gate remains **truthful**: new CVEs **fail** the build until remediated or governed through the same documentation + workflow process.

---

## References

- **`docs/milestones/M28/M28_summary.md`**
- **`docs/milestones/M28/M28_run1.md`**
- **`docs/architecture/ci_environment_contract.md`** — **pip-audit deferrals (M28)**
