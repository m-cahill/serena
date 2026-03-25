#!/usr/bin/env python3
"""Emit performance_snapshot.txt for Quality CI (M29). Artifact only — do not commit."""

from __future__ import annotations

import os
import platform
import sys
import time

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
from datetime import datetime, timezone
from types import SimpleNamespace


def main() -> int:
    lines: list[str] = []
    lines.append("# Serena performance_snapshot (M29)")
    lines.append(f"generated_utc={datetime.now(timezone.utc).isoformat()}")
    lines.append(f"python={sys.version.split()[0]}")
    lines.append(f"platform={platform.platform()}")
    lines.append("")

    from modules.runtime.runner import ProcessingRequest, ProcessingRunner

    class _ProbeRunner(ProcessingRunner):
        def execute(self, state):
            time.sleep(0.001)
            return "ok"

    p = SimpleNamespace()
    _ProbeRunner().run(ProcessingRequest(p))
    m = getattr(p, "runtime_metrics", {})
    lines.append(f"sample_runner_execute_time_s={m.get('execute_time')}")
    lines.append(f"sample_runner_total_time_s={m.get('total_time')}")
    lines.append("")
    lines.append(
        "# Note: sample times are indicative only (CPU load, virtualization, CI runners vary)."
    )

    out = "performance_snapshot.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
