# Scheduler Adapters

Native schedulers are **triggers only**. They must not own recovery policy and must not bypass Host operating mode.

For v0.8 managed installations, automatic periodic execution should enter through the CogentNexus Host supervisor path. The Host first checks MANAGED / PASSTHROUGH / MAINTENANCE and desired runtime state; only then may it invoke lower-level runtime supervision.

Supported adapters:

- Windows: Task Scheduler using hidden `pythonw.exe` execution at user logon/periodic trigger.
- Linux: systemd user service/timer.
- macOS: launchd LaunchAgent.
- Minimal Unix: cron fallback.
- Docker Compose / Kubernetes: container-native health/restart/probe adapters where applicable.
- OpenClaw cron: useful for notifications/task scheduling but not authoritative for resurrecting a stopped Gateway because it lives inside the managed application boundary.

Low-level template rendering remains available:

```text
python skills/cogentnexus/scripts/runtime.py scheduler detect
python skills/cogentnexus/scripts/runtime.py scheduler render --backend systemd
```

## Adapter invariants

- use absolute paths and non-interactive execution;
- prevent overlapping supervisor instances;
- bound runtime/retry behavior;
- persist operator intent before lifecycle action;
- PASSTHROUGH performs no CogentNexus recovery;
- MAINTENANCE performs no managed restart;
- periodic scheduler processes perform no LLM inference;
- controller/workflow children use leases/generations for ownership;
- preserve rollback/configuration evidence for scheduler installation/removal.

Windows child commands use `CREATE_NO_WINDOW`; POSIX detached children use session/background semantics appropriate to the adapter. Diagnostics may go to platform logs, but durable runtime/workflow evidence remains under `.cogent`.
