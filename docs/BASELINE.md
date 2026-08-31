# CogentNexus-OpenClaw Recovery Architecture Baseline

This document records accepted Recovery Core architecture/invariants. It is a **historical technical baseline**, not the current public-release identity.

Current release line: **v0.9.3**.  
Current managed provider: **Ollama only**.  
Validated OpenClaw baseline: `2026.7.1-2 (0790d9f)`.  
Accepted Recovery Core checkpoint: `eadb89099637d24f96e265a500d66c577aa939a3`.  
Historical broad-lifecycle implementation candidate: `f6392da3e4112ce441526d5ef19925c90a872b0b`.  
Frozen repaired publication candidate for Task-191/192 evidence: `050ab53f4b593ab538143084d6bbdbf7e1672e34`.

The v0.9.3 implementation completed bounded real-Windows install-over, reset, uninstall/external-preservation, fresh-reinstall, and Dashboard semantic/durable-delivery acceptance. Those results extend this historical Recovery Core checkpoint; they do not rewrite it.

Task 187 stopped initial publication when stale current guidance was found inside documentation-bearing product surfaces. Task 188 corrected those bytes. A subsequent proportional Dashboard requalification exposed a narrow executable integration defect where bare OpenClaw `NO_REPLY` could be promoted into a visible durable result after CogentNexus-OpenClaw marker decoration.

Task 191 repaired that boundary with TDD. Task 192 then requalified exact candidate `050ab53f4b593ab538143084d6bbdbf7e1672e34` on the accepted Windows host. Current package payload-v2 is `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / `186` files, installed skill-tree identity remains `a1e873ba404205507a1623961b49f1b1a0689f9f`, executable skill scripts tree remains `3d9d323ba19443d46e970b87cef52ce878da274f`, and repaired Dashboard source blob is `aa97d7a5411f799c612cd0aeece050085298a8bb`.

See `docs/CURRENT_STATE.md` for current release/acceptance/publication status. Historical release notes describe the state that existed at their respective versions and must remain historically accurate.

## Purpose

CogentNexus-OpenClaw preserves user intent across process/runtime boundaries while keeping execution proportional to the task. A message may be durably admitted before inference without being forced into a heavyweight workflow.

## Core continuity invariant

Once eligible work is durably accepted, it must not silently disappear. It must reach one of these durable outcomes: delivered/completed, cancelled by valid authority, or explicitly failed with evidence.

## Authority model

In MANAGED mode, durable CNXCLAW state determines recovery authority. Process timing, a late OpenClaw observation, or a transient SQLite read failure must not silently revoke durable Host ownership.

Authority is fenced by Ticket identity, owner session, session generation, model-call/Host timeout state, Direct Recovery run identity, cancellation/terminal state, and operating mode.

OpenClaw native restart continuation is suppressed only when the exact continuation shape belongs to the same CNX-owned session/generation and durable evidence matches the owned recovery. Ordinary messages continue normally.

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

Transient `SQLITE_BUSY` / WAL recovery contention while polling authority is not durable revocation. Read-only authority connections use bounded tolerance. A BUSY read must not race a still-running inference against a replacement attempt.

### Response/delivery rule

`response_ready` is immutable once committed. Delivery transport may retry delivery of a durable result; it must not regenerate inference merely because delivery is uncertain.

CogentNexus-OpenClaw therefore provides an exactly-once-ish durable delivery boundary, not a universal guarantee that arbitrary external side effects happen exactly once.

### Direct Dashboard silent-sentinel rule

A bare OpenClaw `NO_REPLY` / `no_reply` silent sentinel is not visible semantic content and must never be marker-staged into a durable visible Dashboard result.

For a genuine direct Dashboard Ticket whose natural final is exactly the bare sentinel, the repaired integration may request at most one same-run OpenClaw finalization revision. CogentNexus-OpenClaw does not fabricate the answer and does not authorize a separate external Direct Recovery run merely because the sentinel appeared.

Task 192's accepted real turn required zero revisions because the first natural final was already the requested visible nonce. The repair remains protected by repository regression tests even though the fallback branch was not needed in that successful live turn.

## Operating modes

- **MANAGED** — CNXCLAW owns Ticket-first continuity, managed lifecycle, and recovery behavior.
- **PASSTHROUGH** — CNXCLAW interception/background ownership are disabled and OpenClaw remains natively usable.
- **MAINTENANCE** — deliberate stop; durable state remains and recovery must not fight operator intent.

OpenClaw must remain usable without CogentNexus-OpenClaw. PASSTHROUGH is therefore an operational boundary, not merely a configuration label.

The durable policy register is stored at `.cogentnexus-openclaw/host/managed-policy.md`. Registration is independent from whether MANAGED integration is currently applied, so PASSTHROUGH can remove active integration without destroying the registered policy source.

## Host and supervisor

The external supervisor is deterministic and CPU-only in its periodic healthy path. It may inspect endpoint health and durable state, but does not perform model inference itself.

## Durable workflow baseline

STAGED work retains revisioned task state, checkpoint/resume/rollback, worker leases and generation fences, durable outboxes, deterministic validators, artifact hashes/manifests, bounded retry/repair, and terminal evidence gates.

## Accepted checkpoint and later evidence

Recovery Core commit: `eadb89099637d24f96e265a500d66c577aa939a3`.

Accepted live Test A v16 demonstrated one Host-authorized recovery attempt, no competing native recovery inference, no recursive Ticket, no same-session duplicate Ticket, no escaped SQLite lock retry, original model provenance retained, one durable result, and confirmed delivery.

The later broad-lifecycle candidate `f6392da3...` completed the lifecycle sequence. The documentation-corrected candidate `604569c...` was later superseded after the `NO_REPLY` defect was exposed. Task 191/192 provide the repair and proportional real-Windows evidence for `050ab53f...`.

Acceptance remains exact-artifact based. Later living-document/coordination commits may accompany publication without redefining the Task-191/192 product candidate, but any new product-bearing executable/package change requires classification and evidence appropriate to that changed surface.
