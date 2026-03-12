"""Contract tests for ProcessingRunner (M10 runner skeleton)."""
from modules.runtime.runner import ProcessingRunner, ProcessingRequest


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
