"""M15 contract tests: queue mode preserves execution and lifecycle."""
from types import SimpleNamespace

from modules.runtime.runner import ProcessingRunner, ProcessingRequest
from modules.runtime.execution_queue import ExecutionQueue


def _dummy_processing():
    """M19: processing must accept model_provider injection from prepare()."""
    return SimpleNamespace()


class TrackingQueue(ExecutionQueue):
    """Tracks submit calls for test verification."""

    def __init__(self):
        self.submit_called = False
        self.submit_state = None

    def submit(self, state, fn):
        self.submit_called = True
        self.submit_state = state
        return fn(state)


def test_queue_mode_uses_queue(monkeypatch):
    """When use_queue=True, queue.submit is invoked and execution completes."""
    queue = TrackingQueue()
    runner = ProcessingRunner(queue=queue, use_queue=True)

    def fake_execute(state):
        return "done"

    monkeypatch.setattr(runner, "execute", fake_execute)

    request = ProcessingRequest(_dummy_processing())
    result = runner.run(request)

    assert queue.submit_called is True
    assert result == "done"


def test_queue_mode_preserves_lifecycle_order(monkeypatch):
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
    runner.run(ProcessingRequest(_dummy_processing()))

    assert calls == ["prepare", "execute", "finalize"]


def test_default_mode_unchanged(monkeypatch):
    """Default use_queue=False synchronous path unchanged (no queue)."""
    called = {}

    def fake_execute(state):
        called["ok"] = True
        assert hasattr(state.processing, "model_provider")
        return "result"

    runner = ProcessingRunner()
    monkeypatch.setattr(runner, "execute", fake_execute)
    request = ProcessingRequest(_dummy_processing())
    result = runner.run(request)

    assert called["ok"]
    assert result == "result"


def test_execution_queue_submit_pass_through():
    """M15: ExecutionQueue.submit invokes fn(state) synchronously."""
    queue = ExecutionQueue()
    state = object()

    def fn(s):
        assert s is state
        return 99

    assert queue.submit(state, fn) == 99
