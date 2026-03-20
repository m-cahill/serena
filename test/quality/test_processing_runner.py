"""Contract tests for ProcessingRunner (M10 runner skeleton, M11 lifecycle, M12 hooks)."""
from types import SimpleNamespace

from modules.runtime.runner import ProcessingRunner, ProcessingRequest


def _dummy_processing():
    """M19: processing must accept attribute injection (model_provider)."""
    return SimpleNamespace()


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
