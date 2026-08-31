# Architecture

The current v0.9.3 architecture has two independent axes: **continuity** and **execution depth**.

## Continuity plane

```text
eligible user intent -> durable Ticket -> Host authority -> runtime -> durable result -> delivery receipt
```

The Ticket/Host plane survives process-level interruption and is authoritative over transient model/runtime observations.

## Execution plane

DIRECT, LOOKUP, ACTION and STAGED lanes choose the minimum machinery appropriate to risk/complexity. Ticket-first admission does not automatically create a workflow.

## Recovery authority

MANAGED Direct Recovery is fenced by Ticket, owner session, generation, Host-authorized model-call state and recovery run identity. Native OpenClaw restart continuation is consumed only when it exactly matches the already-owned durable recovery envelope.

Transient SQLite BUSY during authority reads is not durable revocation.

## Delivery

Model completion and user-visible completion are separate. `response_ready`/durable result precede delivery confirmation. Transport retries must not regenerate inference merely because delivery is uncertain.

Canonical operational scope: `docs/BASELINE.md` and `docs/CURRENT_STATE.md`.
