"""Runtime execution boundary for Serena.

M10: ProcessingRunner skeleton. Thin adapter around process_images_inner.
M16: processing_runtime.run_generation_batches — execution-phase batch orchestration.
M17: sampler_runtime.run_sampler_txt2img, run_sampler_img2img — sampler invocation.
M18: decode_runtime — VAE decode, face/color/overlay postprocess, per-row and grid save for process_images_inner.
M19: model_provider — ModelProvider / SharedModelProvider; runtime uses get_model(p) only.
"""
