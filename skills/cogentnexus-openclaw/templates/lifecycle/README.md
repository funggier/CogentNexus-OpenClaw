# Lifecycle launchers

The current v0.9.3 operator surface is the `cnxclaw` launcher installed in the OpenClaw workspace:

```text
cnxclaw status
cnxclaw start
cnxclaw stop
cnxclaw restart
cnxclaw disable
cnxclaw enable
```

The `cnxclaw.cmd` compatibility template routes through `cnxclaw_v093.py`, the v0.9.3 Ollama-only facade. The accepted v0.9.2 `cnxclaw.py` implementation remains the compatibility backend used by that facade; it is not the current direct operator entry point. The other wrappers in this directory remain portable **low-level** runtime lifecycle helpers:

- Windows: `start-cogentnexus-openclaw.cmd`, `stop-cogentnexus-openclaw.cmd`
- Linux/macOS: `start-cogentnexus-openclaw.sh`, `stop-cogentnexus-openclaw.sh`

Use `cnxclaw` for normal operation because Host operating mode, desired state, Ticket recovery, watchdog compatibility, startup ownership, provider policy, and runtime lifecycle must remain aligned.

In v0.9.3 the managed inference-provider surface is Ollama only. The facade accepts an explicit `--provider ollama` for compatibility and rejects other managed provider selections before invoking the legacy backend.

`cnxclaw stop` means intentional MAINTENANCE. `cnxclaw disable` means PASSTHROUGH and must leave native OpenClaw usable; the low-level stop wrapper is **not** a substitute for PASSTHROUGH.

Run portable wrappers from the workspace whose runtime data lives under `.cogentnexus-openclaw`, or set `COGENTNEXUS_OPENCLAW_ROOT` explicitly.

On Linux/macOS, make shell wrappers executable when used directly:

```sh
chmod +x start-cogentnexus-openclaw.sh stop-cogentnexus-openclaw.sh
```

Do not use a low-level stop while a response still needs durable delivery unless interruption/maintenance behavior is intentional and understood.
