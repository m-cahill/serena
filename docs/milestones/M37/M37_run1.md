# M37 — Run 1 (CI & inspection)

**Milestone:** M37 — Security deferral closure and final 5/5 re-audit  
**PR:** https://github.com/m-cahill/serena/pull/93  
**Depends on:** M36 binding Quality **`23677054515`** @ merge **`ab4c4679`**

---

## 1. Configuration verified (pre-change)

| Item | Location / value |
|------|------------------|
| **`pip-audit` ignores** | `.github/workflows/run_quality_tests.yaml` — **`--ignore-vuln CVE-2025-69872`**, **`--ignore-vuln CVE-2026-4539`** |
| **Contract** | `docs/architecture/ci_environment_contract.md` — pip-audit deferrals (M28) |
| **Historical evidence** | `docs/milestones/M28/M28_run1.md` |
| **Lock pins** | `requirements-ci.txt` — **`diskcache==5.6.3`**, **`pygments==2.19.2`** |

---

## 2. Upstream fix availability (2026-03-28)

### CVE-2026-4539 — **pygments**

- Advisory text and community sources cite a fix in **pygments ≥ 2.19.3**.
- **PyPI check (binding for this milestone):** `pip index versions pygments` reports **LATEST 2.19.2**; `pip download pygments==2.19.3 --no-deps` **fails** — **no matching distribution** (versions enumerate through **2.19.2** only).
- **Conclusion:** **No installable fixed wheel** on PyPI at inspection time — **cannot** remove **`--ignore-vuln CVE-2026-4539`** without a speculative pin or vendoring.

### CVE-2025-69872 — **diskcache**

- **PyPI:** **`diskcache`** latest remains **5.6.3** (same as lock).
- Ecosystem databases continue to list **no fixed release** that clears the pickle-deserialization class of issue for the default code path.
- **Conclusion:** **Deferral remains** — **cannot** remove **`--ignore-vuln CVE-2025-69872`**.

---

## 3. Dependency / workflow changes

**None.** No lockfile bump, no **`--ignore-vuln`** removal — **blocking `pip-audit`** unchanged; **no CI weakening**.

---

## 4. PR CI (doc-only PR)

**PR head:** **`b9166a0dd62056421d0c4617f8f091080dfce5a3`**

| Role | Workflow | Run ID | Result | `headSha` |
|------|----------|--------|--------|-----------|
| **PR gate** | **Linter** | **`23677809650`** | **success** | **`b9166a0dd62056421d0c4617f8f091080dfce5a3`** |
| **PR gate** | **Smoke Tests** | **`23677809662`** | **success** | **`b9166a0dd62056421d0c4617f8f091080dfce5a3`** |

---

## 5. Post-merge `main`

**Merge commit:** **`18c13a59b73de16f85c7dacd57162ac55713b1aa`** (**2026-03-28T04:54:15Z** UTC). Merge method: **merge commit** (`gh pr merge 93 --merge`).

| Check | Run ID | Result | `headSha` |
|-------|--------|--------|-----------|
| **Linter** | **`23677884602`** | **success** | **`18c13a59b73de16f85c7dacd57162ac55713b1aa`** |
| **Quality Tests** | **`23677884594`** | **success** | **`18c13a59b73de16f85c7dacd57162ac55713b1aa`** |

**Quality (log):** **213** passed; **TOTAL** coverage **48%**; **`--fail-under=42`** unchanged.

**pip-audit (log):** **`No known vulnerabilities found, 2 ignored`** — same **two** governed CVEs (**CVE-2025-69872**, **CVE-2026-4539**); **no** new **`--ignore-vuln`** lines.

---

## 6. Outcome

**Fallback path:** Internal Serena Phase VIII goals are complete; **two governed deferrals** remain because **PyPI** does not offer **installable** fixed versions for both packages at closeout inspection. Final program posture: **release-ready and internally complete**; **unconditional** “zero ignored advisories” **blocked by upstream**.
