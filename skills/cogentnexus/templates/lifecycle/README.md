# Portable lifecycle launchers

These wrappers expose the verified CogentNexus lifecycle commands without embedding machine-specific paths.

- Windows: `start-cogentnexus.cmd` and `stop-cogentnexus.cmd`
- Linux/macOS: `start-cogentnexus.sh` and `stop-cogentnexus.sh`

Run them from the workspace whose runtime data should live in `.cogent`, or set `COGENTNEXUS_ROOT` to an absolute runtime-data directory.

On Linux/macOS, make the shell files executable after installation:

```sh
chmod +x start-cogentnexus.sh stop-cogentnexus.sh
```

The stop launcher establishes maintenance mode before stopping OpenClaw and the local provider. The start launcher is idempotent and verifies health before clearing maintenance mode. Do not use stop while an active response still needs to be delivered.
