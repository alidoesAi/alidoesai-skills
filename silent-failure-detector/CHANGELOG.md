# Changelog — silent-failure-detector

## 0.1.0 — 2026-06-25
- First release. Deterministic, read-only, stdlib-only detector for silent (no-error) stream failures.
- Reproducible eval (105-case synthetic labeled set, seed 20260625): accuracy 83.8% (TPR 81.8% / TNR 86.0%), all errors in the 2–4× threshold grey zone, clear cases 100%.
- Verified-skill package: SKILL.md, skill-card.md (risk_tier L0), SECURITY.md, BENCHMARK.md (the receipt).
- Known limits documented; `multiplier` is the latency/false-alarm tuning knob.
