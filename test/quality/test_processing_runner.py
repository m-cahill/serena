"""Contract tests for ProcessingRunner (M10 runner skeleton, M11 lifecycle, M12 hooks)."""
from types import SimpleNamespace

from modules.runtime.runner import ProcessingRunner, ProcessingRequest


def _dummy_processing():
    """M19: processing must accept attribute injection (model_provider)."""
    return SimpleNamespace()


def test_processing_request_wraps_processing():
    proc = object()
    req = ProcessingRequest(proc)
    assert req.processing is proc


def test_runner_hooks_called(monkeypatch):
    """ProcessingRunner invokes on_prepare, on_execute, on_finalize in order."""
    calls = []

    class TestRunner(ProcessingRunner):
        def on_prepare(self, state):
            calls.append("prepare_hook")

        def on_execute(self, state, result):
            calls.append("execute_hook")

        def on_finalize(self, state, result):
            calls.append("finalize_hook")

        def execute(self, state):
            return "result"

    runner = TestRunner()
    runner.run(ProcessingRequest(_dummy_processing()))

    assert calls == ["prepare_hook", "execute_hook", "finalize_hook"]


def test_runner_lifecycle_order(monkeypatch):
    """ProcessingRunner invokes prepare → execute → finalize in order."""
    calls = []

    class TestRunner(ProcessingRunner):
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


def test_processing_runner_delegates(monkeypatch):
    """ProcessingRunner.run invokes execute with prepared state (M19: p has model_provider)."""
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


def test_runner_replaces_non_dict_runtime_metrics():
    """M29: non-dict runtime_metrics is normalized before execute_time / total_time."""

    class TestRunner(ProcessingRunner):
        def execute(self, state):
            state.processing.runtime_metrics = "not-a-dict"
            return "ok"

    runner = TestRunner()
    proc = _dummy_processing()
    proc.runtime_metrics = ["wrong-type"]
    runner.run(ProcessingRequest(proc))
    assert isinstance(proc.runtime_metrics, dict)
    assert "execute_time" in proc.runtime_metrics
    assert "total_time" in proc.runtime_metrics
