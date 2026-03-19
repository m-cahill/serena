"""M16 contract tests: processing path delegates to processing_runtime."""


def test_process_images_inner_delegates_to_run_generation_batches(initialize):
    """process_images_inner delegates batch orchestration to processing_runtime.run_generation_batches."""
    import inspect
    import modules.processing

    source = inspect.getsource(modules.processing.process_images_inner)
    assert "processing_runtime.run_generation_batches" in source
    assert "for n, samples_ddim in" in source


def test_processing_runtime_module_exists(initialize):
    """processing_runtime module exists and exposes run_generation_batches."""
    from modules.runtime import processing_runtime

    assert hasattr(processing_runtime, "run_generation_batches")
    assert callable(processing_runtime.run_generation_batches)
