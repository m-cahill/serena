"""M29: baseline performance — runner records metrics; no strict thresholds."""

import time
from types import SimpleNamespace

from modules.runtime.runner import ProcessingRequest, ProcessingRunner


def test_runner_records_runtime_metrics_txt2img_path():
    """After run(), p.runtime_metrics has execute_time and total_time."""

    class QuickRunner(ProcessingRunner):
        def execute(self, state):
            time.sleep(0.002)
            return "processed"

    runner = QuickRunner()
    p = SimpleNamespace()
    out = runner.run(ProcessingRequest(p))

    assert out == "processed"
    assert hasattr(p, "runtime_metrics")
    assert isinstance(p.runtime_metrics, dict)
    assert "execute_time" in p.runtime_metrics
    assert "total_time" in p.runtime_metrics
    assert p.runtime_metrics["execute_time"] >= 0
    assert p.runtime_metrics["total_time"] >= p.runtime_metrics["execute_time"]
