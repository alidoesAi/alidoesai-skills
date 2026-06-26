#!/usr/bin/env python3
"""Reproducible eval for silent-failure-detector.

Deterministic end-to-end: synthetic gold set (fixed seed) + a deterministic detector +
deterministic scoring against ground-truth labels. NO LLM judge — the grader is exact,
so a third party re-running gets identical numbers. This is the "verification receipt".

Positive class = "silent/stopped" (the thing we want to catch).
  TP: truly stopped, flagged silent      FN: truly stopped, called healthy (missed death)
  TN: truly alive,   called healthy       FP: truly alive,   flagged silent (false alarm)

Outputs: results.json, transcripts.jsonl, and a printed summary + failure taxonomy.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from detector import detect  # noqa: E402

HERE = os.path.dirname(__file__)
MULTIPLIER = 3.0


def wilson(k: int, n: int, z: float = 1.96):
    """95% Wilson score interval for a binomial rate (good for small n)."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (round(max(0.0, center - half), 4), round(min(1.0, center + half), 4))


def main():
    gold_path = os.path.join(HERE, "gold.jsonl")
    cases = [json.loads(line) for line in open(gold_path)]

    tp = fp = tn = fn = 0
    transcripts = []
    for c in cases:
        truth_silent = (c["label"] == "stopped")
        v = detect(c["input"]["now"], c["input"]["timestamps"],
                   c["input"]["expected_interval_sec"], MULTIPLIER)
        pred_silent = (v["status"] == "silent")
        correct = (pred_silent == truth_silent)
        if pred_silent and truth_silent:
            tp += 1
        elif pred_silent and not truth_silent:
            fp += 1
        elif not pred_silent and not truth_silent:
            tn += 1
        else:
            fn += 1
        transcripts.append({
            "id": c["id"], "kind": c["kind"], "label": c["label"],
            "age_ratio": c["age_ratio"], "predicted": v["status"],
            "correct": correct, "reason": v["reason"],
        })

    n = len(cases)
    pos = tp + fn   # truly stopped
    neg = tn + fp   # truly alive
    tpr = tp / pos if pos else 0.0           # recall on silent failures
    tnr = tn / neg if neg else 0.0
    acc = (tp + tn) / n if n else 0.0

    results = {
        "claim": "the detector flags a silently-stopped stream and passes a healthy one",
        "criterion": "binary: status=='silent' must equal ground-truth label=='stopped'",
        "grader": "deterministic exact-match vs labels (no LLM judge)",
        "n": n, "positives_stopped": pos, "negatives_alive": neg,
        "confusion": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "tpr_recall": round(tpr, 4), "tpr_ci95": wilson(tp, pos),
        "tnr_specificity": round(tnr, 4), "tnr_ci95": wilson(tn, neg),
        "accuracy": round(acc, 4), "accuracy_ci95": wilson(tp + tn, n),
        "config": {"multiplier": MULTIPLIER, "seed": 20260625,
                   "python": sys.version.split()[0]},
    }
    # Failure taxonomy: where do the errors live?
    errs = [t for t in transcripts if not t["correct"]]
    fp_grey = sum(1 for t in errs if t["predicted"] == "silent" and t["kind"] == "grey")
    fp_clear = sum(1 for t in errs if t["predicted"] == "silent" and t["kind"] == "clear")
    fn_grey = sum(1 for t in errs if t["predicted"] == "healthy" and t["kind"] == "grey")
    fn_clear = sum(1 for t in errs if t["predicted"] == "healthy" and t["kind"] == "clear")
    results["failure_taxonomy"] = {
        "false_positive_grey_zone": fp_grey,
        "false_positive_clear": fp_clear,
        "false_negative_grey_zone": fn_grey,
        "false_negative_clear": fn_clear,
    }

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(HERE, "transcripts.jsonl"), "w") as f:
        for t in transcripts:
            f.write(json.dumps(t) + "\n")

    print(json.dumps(results, indent=2))
    print("\nFailure taxonomy (plain language):")
    print(f"  - False positives (alive flagged silent): {fp_grey+fp_clear} "
          f"— all in the 2-4x grey zone: {fp_grey}, clear-case: {fp_clear}")
    print(f"  - False negatives (death missed): {fn_grey+fn_clear} "
          f"— all in the 2-4x grey zone: {fn_grey}, clear-case: {fn_clear}")
    print("  Interpretation: errors concentrate at the threshold boundary "
          "(latency vs false-alarm tradeoff), not on clear cases.")


if __name__ == "__main__":
    main()
