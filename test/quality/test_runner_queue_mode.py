"""M15 contract tests: queue mode preserves execution and lifecycle."""
from modules.runtime.runner import ProcessingRunner, ProcessingRequest
from modules.runtime.execution_queue import ExecutionQueue


class TrackingQueue(ExecutionQueue):
    """Tracks submit calls for test verification."""

    def __init__(self):
        self.submit_called = False
        self.submit_state = None

    def submit(self, state, fn):
        self.submit_called = True
        self.submit_state = state
        return fn(state)


def test_queue_mode_uses_queue(monkeypatch, initialize):
    """When use_queue=True, queue.submit is invoked and execution completes."""
    queue = TrackingQueue()
    runner = ProcessingRunner(queue=queue, use_queue=True)

    def fake_execute(state):
        return "done"

    monkeypatch.setattr(runner, "execute", fake_execute)

    request = ProcessingRequest(processing="dummy")
    result = runner.run(request)

    assert queue.submit_called is True
    assert result == "done"


def test_queue_mode_preserves_lifecycle_order(monkeypatch, initialize):
    """When use_queue=True, lifecycle order prepare→execute→finalize preserved."""
    calls = []
    queue = TrackingQueue()

    class TestRunner(ProcessingRunner):
        def __init__(self):
            super().__init__(queue=queue, use_queue=True)

        def prepare(self, request):
            calls.append("prepare")
            return request

        def execute(self, state):
            calls.append("execute")
            return "result"

        def finalize(self, state, result):
            calls.append("finalize")
            return result

    runner = TestRunner()
    runner.run(ProcessingRequest(processing="dummy"))

    assert calls == ["prepare", "execute", "finalize"]


def test_default_mode_unchanged(monkeypatch, initialize):
    """Default use_queue=False identical to pre-M15 (no queue path)."""
    import modules.processing

    called = {}

    def fake_process_images_inner(p):
        called["ok"] = True
        return "result"

    monkeypatch.setattr(
        modules.processing,
        "process_images_inner",
        fake_process_images_inner,
    )

    runner = ProcessingRunner()
    request = ProcessingRequest(processing="dummy")
    result = runner.run(request)

    assert called["ok"]
    assert result == "result"
