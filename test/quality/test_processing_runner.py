"""Contract tests for ProcessingRunner (M10 runner skeleton, M11 lifecycle)."""
from modules.runtime.runner import ProcessingRunner, ProcessingRequest


def test_runner_lifecycle_order(monkeypatch, initialize):
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
    runner.run(ProcessingRequest(processing="dummy"))

    assert calls == ["prepare", "execute", "finalize"]


def test_processing_runner_delegates(monkeypatch, initialize):
    """ProcessingRunner.run delegates to process_images_inner."""
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
