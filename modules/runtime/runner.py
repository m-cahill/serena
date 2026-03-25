"""ProcessingRunner — unified execution entrypoint for Serena pipeline.

M10: Thin adapter around process_images_inner. No behavior changes.
M11: Lifecycle surface (prepare → execute → finalize). Pass-through behavior.
M12: Instrumentation hooks (on_prepare, on_execute, on_finalize). No-op by default.
M15: Queue insertion seam. Optional queue wraps execute only; default synchronous.
M19: Injects model_provider onto processing; runtime uses get_model(p) only.
M29: Stores execute_time and total_time on processing.runtime_metrics (perf_counter).
"""

import time


class ProcessingRequest:
    """Wraps StableDiffusionProcessing for runner boundary."""

    def __init__(self, processing):
        self.processing = processing


class ProcessingRunner:
    """
    Unified execution entrypoint for Serena processing pipeline.
    M11: Exposes lifecycle stages for future instrumentation.
    M12: Optional instrumentation hooks (no-op by default).
    M15: Optional queue wraps execute only; use_queue=False by default.
    """

    def __init__(self, queue=None, use_queue=False, model_provider=None):
        from modules.runtime.execution_queue import ExecutionQueue
        from modules.runtime.model_provider import SharedModelProvider

        self.queue = queue or ExecutionQueue()
        self.use_queue = use_queue
        self.model_provider = model_provider if model_provider is not None else SharedModelProvider()

    def run(self, request):
        """Execute processing pipeline via lifecycle stages."""
        t_run_start = time.perf_counter()
        state = self.prepare(request)
        self.on_prepare(state)
        if self.use_queue:
            result = self.queue.submit(state, self._execute)
        else:
            result = self._execute(state)
        self.on_execute(state, result)
        result = self.finalize(state, result)
        self.on_finalize(state, result)
        total = time.perf_counter() - t_run_start
        p = state.processing
        metrics = getattr(p, "runtime_metrics", None)
        if not isinstance(metrics, dict):
            metrics = {}
        metrics["total_time"] = total
        p.runtime_metrics = metrics
        return result

    def _execute(self, state):
        """Internal execution hook. Future insertion point for async, retries, cancellation."""
        t0 = time.perf_counter()
        result = self.execute(state)
        dt = time.perf_counter() - t0
        p = state.processing
        metrics = getattr(p, "runtime_metrics", None)
        if not isinstance(metrics, dict):
            metrics = {}
        metrics["execute_time"] = dt
        p.runtime_metrics = metrics
        return result

    def prepare(self, request):
        """Lifecycle stage 1: prepare request. M19: attach model_provider to processing."""
        request.processing.model_provider = self.model_provider
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
