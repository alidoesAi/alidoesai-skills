#!/usr/bin/env python3
"""Generate a synthetic, honestly-labeled gold set for the silent-failure-detector eval.

Ground truth = the generator's INTENT (is this stream still alive, or did it stop?),
set independently of the detector's 3x rule. Clear cases are well separated; a deliberate
"grey zone" (last gap 2x-4x of expected) is included so the eval surfaces the detector's
REAL limits (boundary latency + variance sensitivity) instead of a contrived 100%.

SYNTHETIC DATA — honestly labeled. This is a reference test set, not anyone's private logs.
Deterministic (fixed seed) so a third party re-runs and gets the same gold set.
"""
import json
import os
import random

SEED = 20260625
NOW = 1_750_000_000.0  # fixed reference 'now' (epoch seconds)


def stream_ending_at(last_ts: float, interval: float, n: int, jitter: float, rng) -> list[float]:
    """A regular-ish stream of n timestamps ending at last_ts, spaced ~interval back in time."""
    ts = [last_ts]
    t = last_ts
    for _ in range(n - 1):
        step = interval * (1 + (rng.uniform(-jitter, jitter) if jitter else 0))
        t -= max(step, 1.0)
        ts.append(t)
    return sorted(ts)


def make(rng) -> list[dict]:
    cases = []
    cid = 0

    def add(label, interval, last_age, jitter, kind):
        nonlocal cid
        cid += 1
        last_ts = NOW - last_age
        ts = stream_ending_at(last_ts, interval, n=20, jitter=jitter, rng=rng)
        cases.append({
            "id": f"c{cid:03d}",
            "kind": kind,
            "label": label,                       # ground truth: "alive" | "stopped"
            "input": {"now": NOW, "expected_interval_sec": interval, "timestamps": ts},
            "age_ratio": round(last_age / interval, 3),  # for analysis only
        })

    # 1. Clearly ALIVE: latest beat well within threshold (age 0–2x)
    for _ in range(30):
        iv = rng.choice([60, 300, 900])
        add("alive", iv, last_age=iv * rng.uniform(0.05, 2.0), jitter=0.05, kind="clear")

    # 2. Clearly STOPPED: died long ago (age 5x–40x)
    for _ in range(30):
        iv = rng.choice([60, 300, 900])
        add("stopped", iv, last_age=iv * rng.uniform(5.0, 40.0), jitter=0.05, kind="clear")

    # 3. GREY-ZONE alive: still alive, but the current gap landed at 2x–4x by chance
    #    (a legitimate long-but-not-dead gap). Detector flags >3x → honest FALSE POSITIVES.
    for _ in range(20):
        iv = rng.choice([60, 300])
        add("alive", iv, last_age=iv * rng.uniform(2.0, 4.0), jitter=0.4, kind="grey")

    # 4. GREY-ZONE stopped: truly died, but only recently (gap 2x–4x).
    #    Detector flags only >3x → honest FALSE NEGATIVES (detection latency).
    for _ in range(20):
        iv = rng.choice([60, 300])
        add("stopped", iv, last_age=iv * rng.uniform(2.0, 4.0), jitter=0.05, kind="grey")

    # 5. Empty stream (never started / fully silent) → stopped
    for _ in range(5):
        iv = rng.choice([60, 300])
        cid += 1
        cases.append({
            "id": f"c{cid:03d}", "kind": "clear", "label": "stopped",
            "input": {"now": NOW, "expected_interval_sec": iv, "timestamps": []},
            "age_ratio": None,
        })
    return cases


def main():
    rng = random.Random(SEED)
    cases = make(rng)
    out = os.path.join(os.path.dirname(__file__), "gold.jsonl")
    with open(out, "w") as f:
        for c in cases:
            f.write(json.dumps(c) + "\n")
    n_alive = sum(c["label"] == "alive" for c in cases)
    n_stop = sum(c["label"] == "stopped" for c in cases)
    print(f"wrote {len(cases)} cases to {out}  (alive={n_alive}, stopped={n_stop}, seed={SEED})")


if __name__ == "__main__":
    main()
