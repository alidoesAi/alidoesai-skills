#!/usr/bin/env python3
"""silent-failure-detector — flag when a heartbeat/log stream has gone SILENT unexpectedly.

The failure mode this catches: a process that stops emitting without erroring — the
"it just went quiet" failure that monitoring-on-errors misses entirely.

Design constraints (verified-skill bar): deterministic, stdlib-only, READ-ONLY,
no network, no shell, no writes. The verdict depends only on the timestamps you pass in.
"""
from __future__ import annotations
import argparse
import json
import sys


def detect(now: float,
           timestamps: list[float],
           expected_interval_sec: float,
           multiplier: float = 3.0) -> dict:
    """Return a verdict dict.

    SILENT when the most-recent signal is older than expected_interval_sec * multiplier
    (i.e. roughly `multiplier` expected beats have been missed). An empty stream is SILENT.

    The multiplier is the single tuning knob: it trades detection latency (lower = faster
    to flag a real death) against false positives on high-variance cadences (higher = more
    tolerant of legitimate long gaps). Set expected_interval_sec to the stream's typical
    gap; if the cadence is bursty, set it nearer the p95 gap and document that.
    """
    threshold = expected_interval_sec * multiplier
    if not timestamps:
        return {"status": "silent",
                "reason": "no signals at all",
                "last_age_sec": None,
                "threshold_sec": threshold}
    last = max(timestamps)
    age = now - last
    status = "silent" if age > threshold else "healthy"
    return {"status": status,
            "reason": f"last signal {age:.0f}s old vs threshold {threshold:.0f}s",
            "last_age_sec": age,
            "threshold_sec": threshold}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Detect silent failure in a heartbeat/log stream.")
    p.add_argument("input", help='JSON file: {"now":…, "expected_interval_sec":…, '
                                 '"multiplier":3.0, "timestamps":[…]}')
    a = p.parse_args(argv)
    with open(a.input) as f:
        d = json.load(f)
    v = detect(d["now"], d["timestamps"], d["expected_interval_sec"], d.get("multiplier", 3.0))
    print(json.dumps(v, indent=2))
    return 0 if v["status"] == "healthy" else 1  # nonzero exit = silent (alertable)


if __name__ == "__main__":
    sys.exit(main())
