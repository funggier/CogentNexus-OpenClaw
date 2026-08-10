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
