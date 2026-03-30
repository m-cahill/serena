#!/usr/bin/env python3
"""M41: Compare performance_snapshot.txt to a committed baseline; warn on regression (non-blocking)."""

from __future__ import annotations

import re
from pathlib import Path

# Warn if current metric exceeds baseline by this factor (e.g. 1.2 = >20% slower).
REGRESSION_RATIO = 1.2

_METRIC_RE = re.compile(r"^(sample_runner_(?:execute|total)_time_s)=(.+)$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_snapshot_text(text: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _METRIC_RE.match(line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        if raw.lower() in ("none", ""):
            continue
        try:
            out[key] = float(raw)
        except ValueError:
            continue
    return out


def load_snapshot(path: Path) -> dict[str, float]:
    if not path.is_file():
        return {}
    return parse_snapshot_text(path.read_text(encoding="utf-8"))


def regression_warnings(
    current: dict[str, float],
    baseline: dict[str, float],
    *,
    ratio: float = REGRESSION_RATIO,
) -> list[str]:
    msgs: list[str] = []
    for key, base_val in baseline.items():
        if base_val <= 0:
            continue
        if key not in current:
            msgs.append(f"missing metric {key} in current snapshot")
            continue
        cur = current[key]
        if cur > base_val * ratio:
            pct = (cur / base_val - 1.0) * 100.0
            msgs.append(
                f"{key} regression: current={cur:.6g}s baseline={base_val:.6g}s (~{pct:.0f}% slower than baseline)"
            )
    return msgs


def main() -> int:
    root = _repo_root()
    current_path = root / "performance_snapshot.txt"
    baseline_path = root / "scripts" / "ci" / "performance_snapshot_baseline.txt"

    current = load_snapshot(current_path)
    baseline = load_snapshot(baseline_path)

    if not baseline:
        print(
            "::warning title=M41 performance guardrail::No baseline at "
            f"{baseline_path.relative_to(root)} — skipping regression comparison."
        )
        return 0

    if not current:
        print(
            f"::warning title=M41 performance guardrail::Missing or empty {current_path.name} — skipping comparison."
        )
        return 0

    for msg in regression_warnings(current, baseline):
        print(f"::warning title=M41 performance regression::{msg}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
