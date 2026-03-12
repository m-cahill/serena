"""ProcessingRunner — unified execution entrypoint for Serena pipeline.

M10: Thin adapter around process_images_inner. No behavior changes.
M11: Lifecycle surface (prepare → execute → finalize). Pass-through behavior.
M12: Instrumentation hooks (on_prepare, on_execute, on_finalize). No-op by default.
"""


class ProcessingRequest:
    """Wraps StableDiffusionProcessing for runner boundary."""

    def __init__(self, processing):
        self.processing = processing


class ProcessingRunner:
    """
    Unified execution entrypoint for Serena processing pipeline.
    M11: Exposes lifecycle stages for future instrumentation.
    M12: Optional instrumentation hooks (no-op by default).
    """

    def run(self, request):
        """Execute processing pipeline via lifecycle stages."""
        state = self.prepare(request)
        self.on_prepare(state)
        result = self.execute(state)
        self.on_execute(state, result)
        result = self.finalize(state, result)
        self.on_finalize(state, result)
        return result

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

    def on_prepare(self, state):
        """Instrumentation hook after prepare. No-op by default."""

    def on_execute(self, state, result):
        """Instrumentation hook after execute. No-op by default."""

    def on_finalize(self, state, result):
        """Instrumentation hook after finalize. No-op by default."""
