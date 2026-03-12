"""ProcessingRunner — unified execution entrypoint for Serena pipeline.

M10: Thin adapter around process_images_inner. No behavior changes.
M11: Lifecycle surface (prepare → execute → finalize). Pass-through behavior.
"""


class ProcessingRequest:
    """Wraps StableDiffusionProcessing for runner boundary."""

    def __init__(self, processing):
        self.processing = processing


class ProcessingRunner:
    """
    Unified execution entrypoint for Serena processing pipeline.
    M11: Exposes lifecycle stages for future instrumentation.
    """

    def run(self, request):
        """Execute processing pipeline via lifecycle stages."""
        state = self.prepare(request)
        result = self.execute(state)
        return self.finalize(state, result)

    def prepare(self, request):
        """Lifecycle stage 1: prepare request. Pass-through in M11."""
        return request

    def execute(self, state):
        """Lifecycle stage 2: run processing. Delegates to process_images_inner."""
        from modules.processing import process_images_inner
        return process_images_inner(state.processing)

    def finalize(self, state, result):
        """Lifecycle stage 3: finalize. Pass-through in M11."""
        return result
