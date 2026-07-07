# Governed auto-memory (dogfood receipt)

This skills repo practices what alidoes.ai publishes: agent auto-memory is **configured and
version-controlled** (`../settings.json` → `autoMemoryDirectory`), not left implicit. This directory
is where governed auto-memory lands.

**Privacy firewall.** Memory *bodies* are gitignored by default (see `.gitignore` here) — only this
README and the ignore rule are tracked. The committed **receipt** is the *configuration*, not the
contents: a brand built on verification can show its own tooling is set up the way it recommends,
without leaking anything from a public repo. Anything ever published from here is curated on purpose.

Pairs with the same receipt in the site repo (`alidoesAi/alidoes.ai` → `.claude/`).
