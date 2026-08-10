# Runtime Supervisor

Use for deterministic host health checks and bounded recovery. The supervisor never calls an LLM.

Commands:

    python skills/cogentnexus/scripts/phase3.py supervisor doctor
    python skills/cogentnexus/scripts/phase3.py supervisor tick
    python skills/cogentnexus/scripts/phase3.py supervisor tick --execute-safe
    python skills/cogentnexus/scripts/phase3.py supervisor status
    python skills/cogentnexus/scripts/phase3.py supervisor history

Tick probes Gateway, the configured local provider, memory, and disk. It confirms a failed probe before recovery. Recovery requires --execute-safe, respects cooldown and hourly budgets, verifies afterward, and opens a circuit instead of restarting forever. When `contextContinuity.autoMonitor` is enabled, the same tick observes registered OpenClaw session usage and prepares deduplicated durable handoffs at configured thresholds. It does not spawn or rotate sessions. Runtime state and append-only events live under .cogent/runtime. Scheduler ticks must be deterministic and must not consume an inference lane.
