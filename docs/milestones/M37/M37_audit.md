# M37 — Audit

**Milestone:** Security deferral closure and final 5/5 re-audit  
**Scope:** Phase VIII — final milestone (`docs/serenav1audit.md`)

---

## Conclusion

**Pass (fallback posture).** M37 **re-validated** the two **governed** **`pip-audit`** deferrals against **current PyPI**:

| CVE | Package | M37 finding |
|-----|---------|---------------|
| **CVE-2026-4539** | **pygments** | Fix versions cited in advisories (**≥2.19.3**) are **not** published on PyPI at inspection time — **`pip download pygments==2.19.3`** fails; lock remains **`2.19.2`**. |
| **CVE-2025-69872** | **diskcache** | **No** newer fixed wheel on PyPI vs **5.6.3**; ecosystem still describes **no** simple version bump remediation for the default pickle path. |

**No** dependency churn, **no** workflow relaxation, **no** new **`--ignore-vuln`** IDs.

**Program-level:** Serena **Phase VIII** internal objectives (M34–M37) are **closed**. The **only** remaining barrier to an **unconditional** “all advisories cleared without ignores” posture is **external upstream package releases**, not unfinished internal refactors.

**Final score stance:** Maintain **4.5 / 5** overall (per **`docs/serenav1audit.md`** baseline), with explicit **residual** pip-audit deferrals — **not** claimed as **5.0/5** on security until PyPI provides installable fixes.

---

## CI

*(Binding PR and post-merge run IDs recorded in **`M37_run1.md`**.)*

**pip-audit:** Remains **blocking**; expected green run = **0 unresolved** + **2 documented ignores**.

---

## Risks / follow-ups

- Remove **`--ignore-vuln`** entries **only when** fixed wheels exist on PyPI and **`requirements-ci.txt`** is regenerated with **`uv pip compile`** per contract — **future** maintenance, not M37 scope creep.
