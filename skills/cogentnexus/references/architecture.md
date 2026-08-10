# Architecture and Extension Contract

CogentNexus is a modular monolith: one discoverable OpenClaw skill and one SKILL.md.

- SKILL.md: stable kernel and routing.
- references/: cognitive and operational contracts.
- scripts/: deterministic portable runtime.
- assets/: configuration defaults.
- templates/: native scheduler and deployment adapters.

Portable logic must remain in Python standard-library code. Platform-specific behavior belongs behind an adapter or template. Windows Task Scheduler, systemd, launchd, cron, Docker, and Kubernetes must call the same supervisor contract. Do not run an inference inside the periodic supervisor.

Every new module needs one responsibility, one routing entry, validation coverage, interruption/resume tests, and evidence-based completion. Do not add nested SKILL.md files.
