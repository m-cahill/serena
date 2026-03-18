"""ExecutionQueue — M15 queue insertion seam.

Pass-through implementation. No threading, no async.
Future insertion point for async, retries, cancellation, batching.
"""


class ExecutionQueue:
    """Queue-capable execution boundary. Pass-through in M15."""

    def submit(self, state, fn):
        """Submit state for execution. Delegates to fn synchronously."""
        return fn(state)
