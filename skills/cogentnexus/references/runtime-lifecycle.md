# Graceful Runtime Lifecycle

Use lifecycle mode to distinguish an intentional shutdown from a crash. While maintenance is active, the periodic supervisor returns success without probing or restarting Gateway/Ollama.

Commands:

    python skills/cogentnexus/scripts/runtime.py lifecycle status
    python skills/cogentnexus/scripts/runtime.py lifecycle prepare --reason "planned shutdown"
    python skills/cogentnexus/scripts/runtime.py lifecycle stop --provider
    python skills/cogentnexus/scripts/runtime.py lifecycle restart --reason "configuration reload"
    python skills/cogentnexus/scripts/runtime.py lifecycle start --provider
    python skills/cogentnexus/scripts/runtime.py lifecycle cancel

For planned shutdown, finish or checkpoint the current conversational step, then run lifecycle stop. The durable maintenance marker prevents restart storms. On the next login, native OpenClaw startup plus the supervisor normally restores runtime. Use lifecycle start for an immediate verified start and removal of the marker.

For a restart or reload that should recover automatically if the caller is killed, use `lifecycle restart`. It writes a recoverable marker before invoking OpenClaw. If Gateway stays down or the restart caller is killed, the independent native supervisor uses idempotent `gateway start` recovery with its existing cooldown and circuit breaker. It clears the marker only after both Gateway and provider health are verified. The lower-level `lifecycle prepare --recovery-policy healthy-runtime` remains available for integrations. The default `manual` policy remains fenced until `lifecycle start` or `lifecycle cancel`, so deliberate maintenance cannot end accidentally.

Gateway lifecycle is cross-platform through OpenClaw CLI. Managed Ollama start/stop uses the Windows application adapter or systemd user service. Cloud providers are never stopped. Do not power off until stop reports `safeToPowerOff=true`.

`lifecycle start` polls bounded Gateway and provider readiness after requesting startup, so normal Gateway warm-up does not require a second command. A manual maintenance marker remains until both probes pass.
