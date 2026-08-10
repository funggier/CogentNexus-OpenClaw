# Recovery Controller

Use after a FAILURE or failed verification.

    cogent recover classify --task-id CNX-001
    cogent recover plan --task-id CNX-001
    cogent recover apply --task-id CNX-001
    cogent recover apply --task-id CNX-001 --execute-safe
    cogent recover inspect --task-id CNX-001

Recovery is dry-run by default. Safe apply changes only durable internal settings and task strategy. It never installs dependencies, bypasses permissions, deletes data, runs arbitrary recovery commands, or performs external actions. Retry budget exhaustion or two recent uses of one strategy opens the circuit breaker. Applied policies create RECOVERY ledger events and atomic state revisions.
