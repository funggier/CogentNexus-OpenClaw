# Historical: Phase 0 Ticket-first intake

> **Historical implementation note.** This file records the prototype sequence that led to the current Ticket runtime. It is not the source of truth for v0.8 behavior. See [BASELINE.md](BASELINE.md), [INSTALL.md](INSTALL.md), and the current plugin/Host code for active semantics.

## What Phase 0 established

The prototype proved the core continuity boundary:

- an eligible owner message can be committed to SQLite before inference;
- the complete command, trusted owner/session identity, request hash, and accepted event can be stored atomically;
- retries can be idempotent by request identity;
- running work can use leases, heartbeats, and monotonically increasing fencing generations;
- stale workers can be prevented from completing after reassignment;
- terminal state and owner-bound outbox delivery can be committed durably;
- deterministic recovery scanning can run without LLM inference;
- bounded dispatch can connect Tickets to verified workflows;
- workflow identity/fingerprints can suppress duplicate relaunch after interruption.

The database path established by this work remains:

```text
.cogent/runtime/cogentnexus.sqlite3
```

## Evolution after the prototype

The original document described `ticketFirst` as opt-in and disabled by default. That statement is historical.

In the v0.8 clean baseline:

- normal Host-managed installation enables Ticket-first continuity;
- Ticket creation is lightweight and does not imply STAGED execution;
- DIRECT messages may proceed as ordinary conversation after durable acceptance;
- committed direct turns interrupted by confirmed Gateway failure can be promoted to durable recovery;
- MANAGED / PASSTHROUGH / MAINTENANCE govern Host ownership;
- cancellation is terminal and must fence later recovery;
- one inference lane is the conservative managed default;
- the external Host Controller, not this phase document, owns desired runtime state and lifecycle reconciliation.

## Continuing invariants

The prototype invariants that remain active are:

1. durable state is committed before it is relied upon;
2. duplicate execution is fenced by stable identity/leases/generations;
3. recovery does not run model inference inside the periodic supervisor;
4. stale workers cannot regain authority after reassignment;
5. terminal delivery state is durable;
6. external side effects are never repeated blindly after interruption.

For current architecture and terminology, use [BASELINE.md](BASELINE.md).
