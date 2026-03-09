# M04 Plan — Coverage / Security / Reproducibility Guardrails

**Milestone:** M04  
**Title:** Coverage / security / reproducibility guardrails  
**Status:** Not started  
**Depends on:** M03 (complete)

---

## 1. Intent / Target

Harden Phase I guardrails before Phase II structural refactors:

* Raise coverage gate toward 60%
* Add pip-audit enforcement
* Add dependency lock validation
* Add deterministic build verification
* Add CI artifact retention

---

## 2. Scope (Provisional)

### In scope

* Coverage gate: raise from 33% toward 60% (incremental)
* pip-audit: make blocking (currently `|| true`)
* Dependency lock validation
* Deterministic build verification
* CI artifact retention policy

### Out of scope

* Runtime behavior changes
* New test logic (beyond coverage improvement)
* Phase II refactors

---

## 3. Definition of Done

* [ ] Coverage gate raised (per phase map)
* [ ] pip-audit blocking
* [ ] Lock validation in place
* [ ] Build verification documented
* [ ] Artifact retention configured
* [ ] Ledger updated
* [ ] M04 audit and summary

---

## 4. References

* Phase map: docs/serena.md
* M03 handoff: docs/milestones/M03/M03_summary.md
