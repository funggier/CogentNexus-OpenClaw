# CogentNexus v0.9.1 Operational Baseline

This document is the canonical architecture and invariant baseline for the current v0.9.1 release. Historical release notes describe earlier states and must not override this file or `docs/CURRENT_STATE.md`.

## Purpose

CogentNexus preserves user intent across process/runtime boundaries while keeping execution proportional to the task. A message may be durably admitted before inference without being forced into a heavyweight workflow.

## Core continuity invariant

Once eligible work is durably accepted, it must not silently disappear. It must reach one of these durable outcomes:

- delivered/completed;
- cancelled by valid authority;
- explicitly failed with evidence.

## Authority model

In MANAGED mode, durable CNX state determines recovery authority. Process timing, a late OpenClaw observation, or a transient SQLite read failure must not silently revoke durable Host ownership.

Authority is fenced by:

- Ticket identity and owner session;
- session generation;
- model-call state and Host timeout authorization;
- Direct Recovery state/run identity;
- cancellation/terminal state;
- operating mode.

OpenClaw native restart continuation is suppressed only when the exact continuation shape belongs to the same CNX-owned session/generation and the durable original prompt matches. Ordinary messages continue normally.

## Request lanes

- **DIRECT** — ordinary conversation and simple tasks. Ticket durability does not imply workflow creation.
- **LOOKUP** — focused read-only retrieval.
- **ACTION** — bounded reversible execution with proportionate checks.
- **STAGED** — durable multi-step work requiring checkpoints, validators, bounded repair, or interruption-safe orchestration.

Escalation is based on observed risk/complexity rather than ceremony.

## Recovery boundary

A recoverable Direct interruption follows this conceptual sequence:

```text
Ticket accepted
  -> original model call
  -> Host confirms eligible pre-response interruption
  -> Host records timeout/recovery authority
  -> runtime/provider quiesce/restart as required
  -> Direct Recovery claims same session/generation
  -> embedded inference on original provider/model
  -> response_ready committed once
  -> direct_result durable once
  -> delivery confirmed
  -> Ticket completed
```

### Single-owner rule

When CNX owns Direct Recovery, OpenClaw native restart recovery must not create a competing inference attempt. The v0.9.9 compatibility fence consumes only the exact native restart dispatch proved to belong to the durable CNX-owned recovery.

### SQLite BUSY rule

Transient `SQLITE_BUSY` / WAL recovery contention while polling authority is not durable revocation. Read-only authority connections use a busy timeout and the revocation watcher tolerates transient BUSY conditions. A BUSY read must not reject the watcher and race a still-running inference against `retry()`.

### Response/delivery rule

`response_ready` is immutable once committed. Delivery transport may retry delivery of a durable result; it must not regenerate inference merely because delivery is uncertain.

CogentNexus therefore provides an **exactly-once-ish durable delivery boundary**, not a universal guarantee that arbitrary external side effects happen exactly once.

## Operating modes

### MANAGED

CNX owns Ticket-first continuity, managed lifecycle, and recovery behavior.

### PASSTHROUGH

CNX interception/background ownership are disabled. OpenClaw remains natively usable. Durable CNX state is preserved unless explicitly purged by clean reinstall.

### MAINTENANCE

An operator deliberately stops managed runtime. Recovery must not fight that intent. Later start/restart may resume eligible durable work.

## Host and supervisor

The external supervisor is deterministic and CPU-only in its periodic healthy path. It may inspect endpoint health and durable state, but does not perform model inference itself. Heavy recovery work is entered only when durable state/health warrants it.

## Durable workflow baseline

STAGED work retains:

- revisioned task state;
- checkpoint/resume/rollback;
- worker leases and generation fences;
- durable outboxes;
- deterministic validators;
- artifact hashes/manifests;
- bounded retry/repair;
- terminal evidence gates.

These features are orthogonal to lightweight Direct Ticket continuity.

## Accepted checkpoint

Recovery Core commit: `eadb89099637d24f96e265a500d66c577aa939a3`.

Accepted live Test A v16: one Host-authorized recovery attempt, no competing native recovery inference, no recursive Ticket, no same-session duplicate Ticket, no escaped SQLite lock retry, original model provenance retained, one durable result, and confirmed delivery.

See `docs/CURRENT_STATE.md` for supported/deferred boundaries and `docs/CONTINUITY_TESTS.th.md` for acceptance interpretation.
