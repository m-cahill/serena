# M38 — `processing.py` class and helper decomposition

**Status:** In progress  
**Branch:** `m38-processing-class-helper-decomposition`

## Intent

Reduce structural concentration in `modules/processing.py` by extracting **class definitions** (`StableDiffusionProcessing`, `Processed`, `StableDiffusionProcessingTxt2Img`, `StableDiffusionProcessingImg2Img`) into dedicated modules, with **indefinite re-exports** from `modules.processing`. No deprecation warnings. Script hook call sites remain in `processing.py` (`process_images_inner`).

## Scope

- **In:** Extract classes; shared helpers used only by classes or re-exported (`processing_helpers.py`, `processing_infotext.py`); compatibility imports from `modules.processing`.
- **Out:** Hook relocation; legacy-read migration (M39); CI changes; deprecation of import paths.

## Invariants

- `process_images` / `process_images_inner` unchanged in behavior.
- `ProcessingRunner` boundary unchanged.
- `decode_runtime` and other importers of `apply_color_correction` / `apply_overlay` keep working via `modules.processing`.

## Verification

- PR: Linter + Smoke green.
- `main`: Quality green post-merge.
- New/updated tests for import surfaces and class stability.

## Deliverables

- `modules/processing_helpers.py`, `modules/processing_infotext.py`, `modules/processing_types.py` (or equivalent split).
- Slimmed `modules/processing.py` with re-exports.
- `M38_run1.md`, `M38_summary.md`, `M38_audit.md` at closeout; M39 stubs seeded.
