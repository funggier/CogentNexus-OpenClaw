# Startup Policy

Startup policy and Host operating mode are related but **not the same state**.

- **Operating mode** answers who owns OpenClaw continuity/lifecycle now: MANAGED, PASSTHROUGH, or MAINTENANCE.
- **Startup policy** answers whether the operating system should launch the CogentNexus deterministic supervisor automatically.

## Startup states

- `enabled` — reconcile the native hidden background supervisor.
- `disabled` — remove only CogentNexus-owned automatic triggers.
- `unset` — inspect/report only; never silently enable from this low-level interface.

Low-level commands:

```text
python skills/cogentnexus/scripts/startup.py status
python skills/cogentnexus/scripts/startup.py enable
python skills/cogentnexus/scripts/startup.py disable
python skills/cogentnexus/scripts/startup.py ensure
```

Normal managed installation and `cnx enable` may explicitly reconcile startup ownership as part of entering MANAGED mode. `cnx disable` explicitly disables CogentNexus startup ownership as part of entering PASSTHROUGH.

Calling the low-level `startup.py` interface by itself must not rewrite Host operating mode.

## Platform behavior

- Windows: hidden Task Scheduler process using `pythonw.exe`; least-privilege default starts at user logon.
- Linux: systemd user timer where available.
- macOS: launchd adapter.
- minimal Unix: cron fallback where supported.

True pre-login Windows boot requires an appropriately provisioned service/task identity; user-logon startup cannot run before login.

## Persistence rules

Disabling automatic startup preserves durable Tickets, workflows, checkpoints, ledgers, artifacts, configuration, and manual launch capability.

Updates must preserve the persisted choice and reconcile it rather than silently replacing operator intent.

The periodic supervisor itself performs no model inference.
