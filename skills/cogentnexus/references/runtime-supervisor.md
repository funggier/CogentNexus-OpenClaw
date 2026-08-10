# Runtime Supervisor

Use for deterministic host health, bounded recovery, context monitoring, and always-on workflow resumption. The periodic supervisor never calls an LLM.

Commands:

    python skills/cogentnexus/scripts/phase3.py supervisor doctor
    python skills/cogentnexus/scripts/phase3.py supervisor tick
    python skills/cogentnexus/scripts/phase3.py supervisor tick --execute-safe
    python skills/cogentnexus/scripts/phase3.py supervisor status
    python skills/cogentnexus/scripts/phase3.py supervisor history

A tick probes Gateway, provider, memory, and disk; confirms failures; enforces cooldown, budgets, and circuit breaking; observes bound session pressure; and discovers non-terminal workflows.

Without `--execute-safe`, workflow discovery is observation-only. With it, the supervisor launches a bounded number of detached workflow controllers. It does not execute workflow steps or inference inside the scheduler process. Controllers claim durable ownership and continue independently.

Maintenance mode pauses health recovery, context actions, and workflow launches. Runtime evidence is stored under `.cogent/runtime`; workflow evidence remains under `.cogent/workflows`.