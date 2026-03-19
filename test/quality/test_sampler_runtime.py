"""M17 contract tests: sample() delegates to sampler_runtime."""


def test_sampler_runtime_module_exists(initialize):
    """sampler_runtime exposes run_sampler_txt2img and run_sampler_img2img."""
    from modules.runtime import sampler_runtime

    assert hasattr(sampler_runtime, "run_sampler_txt2img")
    assert callable(sampler_runtime.run_sampler_txt2img)
    assert hasattr(sampler_runtime, "run_sampler_img2img")
    assert callable(sampler_runtime.run_sampler_img2img)


def test_txt2img_sample_delegates_to_sampler_runtime(initialize):
    """Txt2Img.sample delegates to sampler_runtime.run_sampler_txt2img."""
    import inspect
    import modules.processing

    source = inspect.getsource(modules.processing.StableDiffusionProcessingTxt2Img.sample)
    assert "sampler_runtime.run_sampler_txt2img" in source


def test_sample_hr_pass_delegates_to_sampler_runtime(initialize):
    """sample_hr_pass delegates to sampler_runtime.run_sampler_img2img."""
    import inspect
    import modules.processing

    source = inspect.getsource(modules.processing.StableDiffusionProcessingTxt2Img.sample_hr_pass)
    assert "sampler_runtime.run_sampler_img2img" in source


def test_img2img_sample_delegates_to_sampler_runtime(initialize):
    """Img2Img.sample delegates to sampler_runtime.run_sampler_img2img."""
    import inspect
    import modules.processing

    source = inspect.getsource(modules.processing.StableDiffusionProcessingImg2Img.sample)
    assert "sampler_runtime.run_sampler_img2img" in source
