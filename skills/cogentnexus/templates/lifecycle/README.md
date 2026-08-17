# Lifecycle launchers

The v0.9.1 preferred operator surface is the transactional Host Controller launcher installed in the OpenClaw workspace:

```text
cnx status
cnx start
cnx stop
cnx restart
cnx disable
cnx enable
```

The `cnx.cmd` compatibility template routes through `host_control_v091.py`, matching the installed launcher. The other wrappers in this directory remain portable **low-level** runtime lifecycle helpers:

- Windows: `start-cogentnexus.cmd`, `stop-cogentnexus.cmd`
- Linux/macOS: `start-cogentnexus.sh`, `stop-cogentnexus.sh`

Use `cnx` for normal operation because Host operating mode, desired state, Ticket recovery, watchdog compatibility, startup ownership, and runtime lifecycle must remain aligned.

`cnx stop` means intentional MAINTENANCE. `cnx disable` means PASSTHROUGH and must leave native OpenClaw usable; the low-level stop wrapper is **not** a substitute for PASSTHROUGH.

Run portable wrappers from the workspace whose runtime data lives under `.cogent`, or set `COGENTNEXUS_ROOT` explicitly.

On Linux/macOS, make shell wrappers executable when used directly:

```sh
chmod +x start-cogentnexus.sh stop-cogentnexus.sh
```

Do not use a low-level stop while a response still needs durable delivery unless interruption/maintenance behavior is intentional and understood.
