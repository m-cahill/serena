# M06 Plan — Processing Context Extraction

**Project:** Serena
**Phase:** Phase II — Runtime Seam Preparation
**Milestone:** M06
**Title:** Processing Context Extraction
**Branch:** `m06-processing-context`
**Posture:** Behavior-Preserving Refactor
**Target:** Introduce a ProcessingContext object to encapsulate state threaded through process_images() / process_images_inner().

---

## 1. Intent / Target

Introduce a **ProcessingContext object** to encapsulate state currently threaded through `process_images()` and `process_images_inner()`.

**Goals:**
* Prepare for opts snapshot injection (M07)
* Enable deterministic runtime execution
* Improve testability of processing stages

---

## 2. Scope (To Be Defined)

* In scope: TBD
* Out of scope: TBD

---

## 3. Dependencies

* M05 complete (temporary_opts seam)

---

## 4. Next Steps

1. Define ProcessingContext fields and boundaries
2. Identify state to encapsulate
3. Implement minimal extraction
4. Preserve behavior; add tests
