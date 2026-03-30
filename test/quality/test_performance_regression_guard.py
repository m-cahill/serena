"""M41: performance snapshot regression helper (warn-only in CI)."""

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "check_performance_regression",
    _ROOT / "scripts" / "ci" / "check_performance_regression.py",
)
assert _SPEC and _SPEC.loader
_mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_mod)
parse_snapshot_text = _mod.parse_snapshot_text
regression_warnings = _mod.regression_warnings


def test_parse_snapshot_extracts_metrics():
    text = """# header
sample_runner_execute_time_s=0.001
sample_runner_total_time_s=0.002
ignore=me
"""
    d = parse_snapshot_text(text)
    assert d["sample_runner_execute_time_s"] == 0.001
    assert d["sample_runner_total_time_s"] == 0.002


def test_regression_warnings_when_slower():
    current = {
        "sample_runner_execute_time_s": 0.002,
        "sample_runner_total_time_s": 0.002,
    }
    baseline = {
        "sample_runner_execute_time_s": 0.001,
        "sample_runner_total_time_s": 0.001,
    }
    msgs = regression_warnings(current, baseline, ratio=1.2)
    assert len(msgs) == 2


def test_regression_warnings_clear_when_within_ratio():
    current = {
        "sample_runner_execute_time_s": 0.0011,
        "sample_runner_total_time_s": 0.0011,
    }
    baseline = {
        "sample_runner_execute_time_s": 0.0010,
        "sample_runner_total_time_s": 0.0010,
    }
    assert regression_warnings(current, baseline, ratio=1.2) == []
