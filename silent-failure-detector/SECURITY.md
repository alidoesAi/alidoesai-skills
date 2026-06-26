# SECURITY — silent-failure-detector

A verification-brand skill has to hold itself to the bar it sells. This is the threat model.

## What it does
Reads one JSON file of emission timestamps you provide and prints a SILENT/HEALTHY verdict. Pure function of its inputs.

## What it does NOT do
- **No network.** It makes zero outbound connections; nothing is sent anywhere.
- **No shell.** It does not execute commands, spawn subprocesses, or `curl|bash`.
- **No credentials.** It never reads environment secrets, tokens, or keys.
- **No agent-memory access.** It does not read or write `MEMORY.md` / `SOUL.md` / `AGENTS.md` or any persistence file.
- **No writes** outside its own `eval/` directory (where the harness writes the gold set, results, and transcripts).
- **No runtime fetch.** All logic is in `detector.py`; nothing is downloaded or evaluated at run time.

## Data handling
The only data it sees is the list of timestamps you pass in. Use real timestamps freely — they never leave your machine. (The bundled gold set is **synthetic and honestly labeled**, not anyone's private logs.)

## Risk tier
**L0.** Read-only, no egress, no credentials, deterministic. The lethal-trifecta conditions (private data + untrusted content + external egress) are structurally absent — there is no egress and no untrusted-content channel.

## Disclosure
Found an issue or a way the declared behavior differs from the actual behavior? Report it: **hello@alidoes.ai**. Confirmed issues are fixed in the open and logged.
