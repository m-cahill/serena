"""M38: processing module split — import surface and constants re-export."""

from __future__ import annotations


def test_processing_reexports_classes_and_entrypoints():
    import modules.processing as proc

    assert proc.StableDiffusionProcessing is not None
    assert proc.Processed is not None
    assert proc.StableDiffusionProcessingTxt2Img is not None
    assert proc.StableDiffusionProcessingImg2Img is not None
    assert proc.process_images is not None
    assert proc.process_images_inner is not None


def test_processing_reexports_helpers_used_by_decode_runtime():
    import modules.processing as proc

    assert proc.apply_color_correction is not None
    assert proc.apply_overlay is not None


def test_processing_reexports_opt_constants():
    import modules.processing as proc

    assert proc.opt_C == 4
    assert proc.opt_f == 8


def test_processing_types_imports_class_without_processing_cycle():
    from modules.processing_types import StableDiffusionProcessing

    assert StableDiffusionProcessing.__name__ == "StableDiffusionProcessing"
