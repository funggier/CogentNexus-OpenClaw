# Graceful Runtime Lifecycle

Use lifecycle mode to distinguish an intentional shutdown from a crash. While maintenance is active, the periodic supervisor returns success without probing or restarting Gateway/Ollama.

Commands:

    python skills/cogentnexus/scripts/phase3.py lifecycle status
    python skills/cogentnexus/scripts/phase3.py lifecycle prepare --reason "planned shutdown"
    python skills/cogentnexus/scripts/phase3.py lifecycle stop --provider
    python skills/cogentnexus/scripts/phase3.py lifecycle start --provider
    python skills/cogentnexus/scripts/phase3.py lifecycle cancel

For planned shutdown, finish or checkpoint the current conversational step, then run lifecycle stop. The durable maintenance marker prevents restart storms. On the next login, native OpenClaw startup plus the supervisor normally restores runtime. Use lifecycle start for an immediate verified start and removal of the marker.

For a restart or reload that should recover automatically if the caller is killed, use `lifecycle prepare --recovery-policy healthy-runtime`. The supervisor clears only this explicitly recoverable marker, and only after both Gateway and provider health are verified. The default `manual` policy remains fenced until `lifecycle start` or `lifecycle cancel`, so deliberate maintenance cannot end accidentally.

Gateway lifecycle is cross-platform through OpenClaw CLI. Managed Ollama start/stop uses the Windows application adapter or systemd user service. Cloud providers are never stopped. Do not power off until stop reports `safeToPowerOff=true`.
