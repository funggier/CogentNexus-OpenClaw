# CogentNexus-OpenClaw Recovery Architecture Baseline

This document records the accepted Recovery Core architecture/invariants. It is a **historical technical baseline**, not the current release identity.

Current release line: **v0.9.3**.  
Current managed provider: **Ollama only**.  
Validated OpenClaw baseline: `2026.7.1-2 (0790d9f)`.  
Accepted Recovery Core checkpoint: `eadb89099637d24f96e265a500d66c577aa939a3`.  
Frozen accepted v0.9.3 product candidate: `f6392da3e4112ce441526d5ef19925c90a872b0b`.

The v0.9.3 candidate later completed bounded real-Windows install-over, reset, uninstall/external-preservation, fresh-reinstall, and final Dashboard semantic/durable-delivery acceptance. Those later results do not rewrite this historical Recovery Core checkpoint; they extend the accepted evidence for the exact v0.9.3 candidate.

At Task 187, public v0.9.3 publication is blocked because stale current guidance exists inside documentation-bearing product/payload surfaces. Correcting those files changes the accepted artifact identity and therefore requires a new exact candidate and scoped requalification before release publication.

See `docs/CURRENT_STATE.md` for current release/acceptance/publication status. Historical release notes describe the state that existed at their respective versions and must remain historically accurate.

## Purpose

CogentNexus-OpenClaw preserves user intent across process/runtime boundaries while keeping execution proportional to the task. A message may be durably admitted before inference without being forced into a heavyweight workflow.

## Core continuity invariant

Once eligible work is durably accepted, it must not silently disappear. It must reach one of these durable outcomes: delivered/completed, cancelled by valid authority, or explicitly failed with evidence.

## Authority model

In MANAGED mode, durable CNXCLAW state determines recovery authority. Process timing, a late OpenClaw observation, or a transient SQLite read failure must not silently revoke durable Host ownership.

Authority is fenced by Ticket identity, owner session, session generation, model-call/Host timeout state, Direct Recovery run identity, cancellation/terminal state, and operating mode.

OpenClaw native restart continuation is suppressed only when the exact continuation shape belongs to the same CNX-owned session/generation and the durable original prompt matches. Ordinary messages continue normally.

## Request lanes

- **DIRECT** — ordinary conversation and simple tasks; Ticket durability does not imply workflow creation.
- **LOOKUP** — focused read-only retrieval.
- **ACTION** — bounded reversible execution with proportionate checks.
- **STAGED** — durable multi-step work requiring checkpoints, validators, bounded repair, or interruption-safe orchestration.

## Recovery boundary

```text
Ticket accepted
  -> original model call
  -> Host confirms eligible pre-response interruption
  -> Host records recovery authority
  -> runtime/provider quiesce/restart as required
  -> Direct Recovery claims same session/generation
  -> inference on original provider/model
  -> response_ready committed once
  -> direct_result durable once
  -> delivery confirmed
  -> Ticket completed
```

### Single-owner rule

When CNXCLAW owns Direct Recovery, OpenClaw native restart recovery must not create a competing inference attempt. Compatibility fencing consumes only the exact native restart dispatch proved to belong to durable CNX-owned recovery.

### SQLite BUSY rule

Transient `SQLITE_BUSY` / WAL recovery contention while polling authority is not durable revocation. Read-only authority connections use a busy timeout and the revocation watcher tolerates transient BUSY conditions. A BUSY read must not race a still-running inference against a replacement attempt.

### Response/delivery rule

`response_ready` is immutable once committed. Delivery transport may retry delivery of a durable result; it must not regenerate inference merely because delivery is uncertain.

CogentNexus-OpenClaw therefore provides an exactly-once-ish durable delivery boundary, not a universal guarantee that arbitrary external side effects happen exactly once.

## Operating modes

- **MANAGED** — CNXCLAW owns Ticket-first continuity, managed lifecycle, and recovery behavior.
- **PASSTHROUGH** — CNXCLAW interception/background ownership are disabled and OpenClaw remains natively usable.
- **MAINTENANCE** — deliberate stop; durable state remains and recovery must not fight operator intent.

OpenClaw must remain usable without CogentNexus-OpenClaw. PASSTHROUGH is therefore an operational boundary, not merely a configuration label.

The durable managed-policy registration is stored at `.cogentnexus-openclaw/host/managed-policy.md`. The `policy register` operation records that policy independently from whether MANAGED integration is currently applied, so PASSTHROUGH can remove active integration without destroying the registered policy source.

## Host and supervisor

The external supervisor is deterministic and CPU-only in its periodic healthy path. It may inspect endpoint health and durable state, but does not perform model inference itself.

## Durable workflow baseline

STAGED work retains revisioned task state, checkpoint/resume/rollback, worker leases and generation fences, durable outboxes, deterministic validators, artifact hashes/manifests, bounded retry/repair, and terminal evidence gates.

## Accepted checkpoint

Recovery Core commit: `eadb89099637d24f96e265a500d66c577aa939a3`.

Accepted live Test A v16: one Host-authorized recovery attempt, no competing native recovery inference, no recursive Ticket, no same-session duplicate Ticket, no escaped SQLite lock retry, original model provenance retained, one durable result, and confirmed delivery.

The later frozen v0.9.3 candidate `f6392da3...` completed the separate lifecycle and final Dashboard acceptance sequence. Any later product/payload change creates a different candidate identity and must be qualified according to the changed surface before inheriting that evidence.
