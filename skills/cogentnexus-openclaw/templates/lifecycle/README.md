# Lifecycle launchers

The v0.9.1 preferred operator surface is the transactional Host Controller launcher installed in the OpenClaw workspace:

```text
cnxclaw status
cnxclaw start
cnxclaw stop
cnxclaw restart
cnxclaw disable
cnxclaw enable
```

The `cnxclaw.cmd` compatibility template routes through `host_control_v091.py`, matching the installed launcher. The other wrappers in this directory remain portable **low-level** runtime lifecycle helpers:

- Windows: `start-cogentnexus-openclaw.cmd`, `stop-cogentnexus-openclaw.cmd`
- Linux/macOS: `start-cogentnexus-openclaw.sh`, `stop-cogentnexus-openclaw.sh`

Use `cnxclaw` for normal operation because Host operating mode, desired state, Ticket recovery, watchdog compatibility, startup ownership, and runtime lifecycle must remain aligned.

`cnxclaw stop` means intentional MAINTENANCE. `cnxclaw disable` means PASSTHROUGH and must leave native OpenClaw usable; the low-level stop wrapper is **not** a substitute for PASSTHROUGH.

Run portable wrappers from the workspace whose runtime data lives under `.cogentnexus-openclaw`, or set `COGENTNEXUS_OPENCLAW_ROOT` explicitly.

On Linux/macOS, make shell wrappers executable when used directly:

```sh
chmod +x start-cogentnexus-openclaw.sh stop-cogentnexus-openclaw.sh
```

Do not use a low-level stop while a response still needs durable delivery unless interruption/maintenance behavior is intentional and understood.
