# alidoesai-skills

Verified [Agent Skills](https://agentskills.io) — each one shipped **with the reproducible eval that proves it works**. Built by [Ali](https://alidoes.ai), the verified version of personal AI ops.

> Anyone can show you what an AI tool does. These show you *how I know it's right* — every skill carries its benchmark receipt, a permissions/security disclosure, and documented failure modes.

## Skills

| Skill | What it does | Receipt |
|---|---|---|
| [silent-failure-detector](./silent-failure-detector/) | Flags when a heartbeat/log stream goes **silent** — the failure that doesn't error | [BENCHMARK.md](./silent-failure-detector/BENCHMARK.md) · 83.8% accuracy, every error at the threshold boundary, deterministic grader |

## What "verified" means here
Every skill ships: `SKILL.md` (the skill) · `skill-card.md` (identity + declared permissions + risk tier) · `SECURITY.md` (threat model + what it does *not* do) · `BENCHMARK.md` (a **reproducible** eval — re-run it yourself) · a visual receipt. Aligned to the emerging verified-skill bar (NVIDIA / OWASP). License: Apache-2.0.

More at **[alidoes.ai/proof](https://alidoes.ai/proof/)**.
