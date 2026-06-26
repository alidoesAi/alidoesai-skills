# BENCHMARK — silent-failure-detector (the verification receipt)

This is the brand's signature artifact: a reproducible eval so a stranger can re-run it and verify the correctness claim. It maps 1:1 to the 9-part receipt in `research/playbooks/evals-verification.md §5`. **No LLM judge — the grader is exact, so re-running gives identical numbers.**

![Eval receipt: confusion matrix — 45 caught, 10 missed, 7 false alarms, 43 correct; accuracy 83.8% (95% CI 75.6–89.6%); all 17 errors in the 2–4× threshold grey zone, clear cases 100%.](receipt.svg)
*The results, visualized (the SHOW receipt) — diagram source `receipt.svg`, sourced from `eval/results.json`.*

| # | Artifact | This eval |
|---|---|---|
| 1 | **Claim + criterion** | "the detector flags a silently-stopped stream and passes a healthy one." Binary: `status=='silent'` must equal ground-truth `label=='stopped'`. |
| 2 | **Dataset** | 105 synthetic, honestly-labeled cases (50 alive / 55 stopped). Ground truth = generator intent (alive vs stopped), set independently of the 3× rule. Includes a deliberate 2–4× **grey zone** so the eval surfaces real limits, not a contrived 100%. Synthetic data, fixed seed `20260625` — generated 2026-06-25. `eval/make_goldset.py` → `eval/gold.jsonl`. |
| 3 | **Failure taxonomy** | All 17 errors fall in the grey zone; **0 errors on clear cases.** 7 false positives (alive streams that crossed 3× by chance) · 10 false negatives (streams that *just* died, <3× — detection latency). |
| 4 | **Harness** | `eval/run_eval.py` — deterministic detector + deterministic exact-match scoring. |
| 5 | **Judge validation** | N/A by design — no LLM judge. The grader is exact string-match against ground-truth labels, so judgment can't drift. (This is the strongest reproducibility posture for a first receipt.) |
| 6 | **Run config** | `multiplier=3.0`, `seed=20260625`, Python `3.10.12`, run 2026-06-25. |
| 7 | **Transcripts** | `eval/transcripts.jsonl` — per-case input summary, label, prediction, correct/incorrect, reason. |
| 8 | **Results + uncertainty** | below, with 95% Wilson CIs (small-n appropriate). |
| 9 | **Re-run command** | `python3 eval/make_goldset.py && python3 eval/run_eval.py` |

## Results (measured 2026-06-25)

| Metric | Value | 95% CI (Wilson) |
|---|--:|---|
| **Accuracy** | **83.8%** (88/105) | 75.6% – 89.6% |
| **TPR / recall** (catches real silent failures) | **81.8%** (45/55) | 69.7% – 89.8% |
| **TNR / specificity** (doesn't false-alarm) | **86.0%** (43/50) | 73.8% – 93.1% |

Confusion matrix: **TP 45 · FP 7 · TN 43 · FN 10.**

## Honest reading
- **On clearly-alive and clearly-dead streams (and empty streams), the detector is 100% correct.**
- **Every error is at the threshold boundary** — this is the inherent latency-vs-false-alarm tradeoff of staleness detection, not a bug. Lower the `multiplier` to catch deaths faster (more false alarms); raise it to tolerate bursty cadence (slower to catch a real death).
- It is **not** 100% accurate, and claiming it would be the exact slop this brand exists to refute. 83.8% with all errors explained and bounded is the honest, useful number.

*Re-run it. If your machine doesn't reproduce these numbers, that's a bug worth reporting (hello@alidoes.ai).*
