# M08 Plan — Snapshot Threading into process_images_inner

## Intent

M07 introduced `p.opts_snapshot`. M08 threads it into the generation runtime by migrating safe read-only option access inside `process_images_inner()` from `shared.opts` to `p.opts_snapshot`.

## Scope

- **In scope:** Replace `opts.foo` with `p.opts_snapshot.foo` for save-related reads inside `process_images_inner()` only.
- **Out of scope:** save_samples(), sample_hr_pass(), create_infotext(), Processed.__init__(), fill_fields_from_opts(), modules/images.py.

## Migrated Options

- save_images_before_face_restoration
- save_images_before_color_correction
- samples_format
- return_mask, save_mask
- return_mask_composite, save_mask_composite
- grid_only_if_multiple, return_grid, grid_save
- grid_format, grid_extended_filename

## Invariants

Same inputs → same outputs. File paths and naming unchanged. Extension compatibility preserved.
