# skill-card — silent-failure-detector

Machine-readable identity + governance, aligned to the emerging verified-skill bar
(NVIDIA skill-card / OWASP Universal Skill Format), pared to a solo-feasible subset.

| Field | Value |
|---|---|
| **name** | silent-failure-detector |
| **version** | 0.1.0 |
| **owner** | Afsar Ali — alidoes.ai |
| **license** | Apache-2.0 |
| **risk_tier** | **L0** (read-only, no egress, no credentials) |
| **external APIs called** | none |
| **dependencies** | Python ≥3.8 standard library only (no third-party packages) |
| **declared permissions** | filesystem: **read-only** (one input JSON you pass) · network: **none** · shell: **false** · writes: **none** (the eval harness writes only inside its own `eval/` dir) |
| **memory access** | none — does not read or write `MEMORY.md` / `SOUL.md` / `AGENTS.md` |
| **determinism** | full — output depends only on the timestamps passed in |
| **benchmark** | `BENCHMARK.md` (reproducible eval; accuracy 83.8%, all errors in the threshold grey zone) |
| **scan posture** | no `curl\|bash`, no runtime fetch, no obfuscated/base64 commands, no secret access — passes a behavior scan by construction; declared behavior == actual behavior |
| **known limitations** | grey-zone (2–4× threshold) false alarms + one-window detection latency; only as good as the configured `expected_interval_sec` |

**Declared == actual:** this skill reads a JSON file of timestamps and prints a verdict. That is the whole of its behavior. There is no network call, no shell-out, no write outside its eval folder, and no access to credentials or agent memory.
