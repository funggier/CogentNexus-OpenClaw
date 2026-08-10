# Concurrency Manager

Default to one inference lane. Treat this as a safe default, not a permanent limit.

    python skills/cogentnexus/scripts/phase3.py concurrency status
    python skills/cogentnexus/scripts/phase3.py concurrency acquire --kind inference --owner TASK
    python skills/cogentnexus/scripts/phase3.py concurrency release --owner TASK --lease-id ID

Modes are fixed and adaptive. Adaptive mode may scale only to the configured ceiling and falls back to one lane under memory pressure. Inference, execution, verification, and supervisor leases are independent. Every worker must acquire admission before work and release it after a checkpoint. Expired leases are reclaimed. Tasks sharing a mutable artifact still require an exclusive task-level lock.
