"""ProcessingRunner — unified execution entrypoint for Serena pipeline.

M10: Thin adapter around process_images_inner. No behavior changes.
"""


class ProcessingRequest:
    """Wraps StableDiffusionProcessing for runner boundary."""

    def __init__(self, processing):
        self.processing = processing


class ProcessingRunner:
    """
    Unified execution entrypoint for Serena processing pipeline.
    """

    def run(self, request):
        """Execute processing pipeline."""
        from modules.processing import process_images_inner
        return process_images_inner(request.processing)
