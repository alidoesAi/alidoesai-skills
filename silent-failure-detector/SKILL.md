---
name: silent-failure-detector
description: >-
  Detects when a heartbeat or log stream has gone SILENT unexpectedly — the failure
  mode where a process stops emitting without raising an error, so error-based
  monitoring misses it entirely. Use to verify a scheduled job, agent, logger, cron
  task, or data feed is still actually running, or to audit a list of timestamps for
  an unexpected stop. Triggers: "did this job stop", "silent failure", "stale
  heartbeat", "is my logger still running", "no errors but no output", "detect missing
  data". Deterministic, read-only, stdlib-only; ships with a reproducible eval
  (BENCHMARK.md) that proves its accuracy AND its limits.
license: Apache-2.0
metadata:
  version: 0.1.0
  author: Afsar Ali (alidoes.ai)
  risk_tier: L0
---

# silent-failure-detector

Catches the failure that monitoring-on-errors can't see: a process that just **goes quiet**. No exception, no crash — it simply stops emitting, and you find out days later.

## When to use
- You have a stream of emission timestamps (a logger, heartbeat, cron job, agent loop, data feed) and an expected cadence, and you want to know whether it has stopped.
- You want a verifiable, deterministic check you can wire into a daily integrity sweep.

## How it works (one knob)
SILENT when the most-recent signal is older than `expected_interval_sec * multiplier` (default `multiplier = 3.0` → roughly three missed beats). An empty stream is SILENT. The multiplier trades **detection latency** (lower = catch a real death faster) against **false alarms** on bursty cadences (higher = more tolerant). Set `expected_interval_sec` to the stream's typical gap; if the cadence is bursty, set it nearer the p95 gap and say so.

## Run it
```bash
echo '{"now": 1750000000, "expected_interval_sec": 60,
       "timestamps": [1749999940, 1749999990]}' > input.json
python3 detector.py input.json     # exit 0 = healthy, exit 1 = silent (alertable)
```
Or import it: `from detector import detect; detect(now, timestamps, expected_interval_sec, multiplier=3.0)`.

## Output
```json
{ "status": "silent", "reason": "last signal 19880s old vs threshold 180s",
  "last_age_sec": 19880, "threshold_sec": 180.0 }
```

## Known limits (measured, not claimed — see BENCHMARK.md)
On a 105-case labeled set it scores **83.8% accuracy (TPR 81.8% / TNR 86.0%)**. **Every error is in the 2–4× "grey zone" near the threshold; clear cases are 100% correct.** Two honest failure modes: (1) false alarms on alive-but-currently-slow streams that crossed 3× by chance; (2) a one-window detection latency on a stream that *just* died. Tune `multiplier` for your latency/false-alarm preference. The eval is reproducible — re-run it and check the numbers yourself.
