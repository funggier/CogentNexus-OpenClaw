# Scheduler Adapters

Keep supervision logic portable and use the native scheduler only as a trigger.

- Windows: Task Scheduler every five minutes.
- Ubuntu and Linux: systemd user oneshot service and timer.
- macOS: launchd LaunchAgent.
- Minimal Unix: cron fallback.
- Docker Compose: healthcheck and restart policy.
- Kubernetes: exec liveness/readiness probes.
- OpenClaw cron: notifications or task resumption only; it cannot reliably resurrect a stopped Gateway.

Render templates with:

    python skills/cogentnexus/scripts/phase3.py scheduler detect
    python skills/cogentnexus/scripts/phase3.py scheduler render --backend systemd

Back up native scheduler configuration before installation or replacement. Installation and removal change system configuration and require explicit authority. Use absolute paths, non-interactive execution, overlap prevention, bounded runtime, and rollback evidence.

Background execution is invariant across adapters. Windows child commands use `CREATE_NO_WINDOW`; POSIX child commands start in a new session. systemd disconnects stdin and writes diagnostics to the journal, launchd declares a background process type, cron detaches standard streams, and container templates explicitly disable stdin and TTY allocation. Runtime evidence remains available in the CogentNexus ledger even where scheduler output is discarded.
