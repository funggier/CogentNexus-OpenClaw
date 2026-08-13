# Durable experience and lesson store

CogentNexus 0.4 extends the current Ticket-first SQLite runtime without replacing its workflow, resource-admission, outbox, startup-policy, or filesystem-artifact contracts.

## Contract

- Ticket attempts, failures, expired-lease corrections, and verified completions write evidence-backed experience rows in the same transaction as the corresponding Ticket transition.
- A lesson begins as a `hypothesis` and is excluded from normal retrieval.
- `verify`, `contradict`, and `retire` require an evidence reference not already attached to that lesson. Reusing the candidate evidence cannot verify it, and retirement is terminal.
- Normal retrieval uses local SQLite FTS5 and returns only `verified` lessons with all provenance references.
- Applying a lesson is permitted only while it is verified, and the outcome plus evidence is retained.
- Lesson text cannot change authorization, safety policy, validation requirements, or runtime state by itself.
- The knowledge capability is optional. Disabling it cannot disable durable intake, recovery, validation, assembly, or owner delivery.

## Why FTS5 first

This preserves the roadmap's resilience-first ordering. Semantic embeddings remain an optional evaluation-stage enhancement; an embedding provider outage must not become a durability outage. OpenClaw's separate user-memory search can still use embeddings independently.

## Tool operations

`cogent_knowledge` supports `experience`, `candidate`, `verify`, `contradict`, `retire`, `search`, `apply`, and `status`. Mutating calls require explicit evidence references and trusted OpenClaw session context.
