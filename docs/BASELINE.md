# CogentNexus-OpenClaw Recovery Architecture Baseline

This document records the durable architectural invariants that survive across release lines. It is not a release-status page; use [CURRENT_STATE.md](CURRENT_STATE.md) for the current source/release state.

**Current source/release line:** `v0.9.9` (published accepted baseline; tag SHA `ea3b454815378dc1d45b2db621662744ddcd9936`)
**Latest physical runtime acceptance:** OpenClaw `2026.9.6`
**Regression/dev dependency pin:** OpenClaw `2026.7.1-2`
**Managed provider ownership:** Ollama
**Cloud/provider/model/auth routing:** OpenClaw-owned pass-through

Historical checkpoints such as the v0.9.1 Recovery Core and v0.9.4/v0.9.5 publication candidates remain evidence for the exact bytes and environments they described. They are not rewritten into later releases.

## Core continuity invariant

Once eligible work is durably accepted, it must not silently disappear. It must reach one of these durable outcomes:

- delivered/completed;
- cancelled by valid authority; or
- explicitly failed with durable evidence.

## Authority model

In MANAGED mode, durable CNX state determines continuity/recovery authority. Process timing, a late OpenClaw observation, or a transient SQLite read failure must not silently revoke durable ownership.

Authority is fenced by:

- Ticket identity;
- owner session key and physical session identity;
- owner generation;
- active/bound run identity;
- model/inference attempt state;
- cancellation/terminal state;
- operating mode;
- delivery/result evidence.

## Pre-dispatch serialization baseline

Eligible owner input is durably persisted before inference. If an older Ticket in the same owner generation remains non-terminal, later input is held at the claiming `before_dispatch` hook instead of entering OpenClaw's native follow-up queue.

This establishes a deterministic boundary:

```text
message accepted
  -> durable Ticket + ingress claim
  -> older same-generation Ticket exists?
       yes -> hold outside Host queue
       no  -> continue original request
```

A valid user Stop advances owner generation once, cancels active + held Tickets, and causes held cancelled ingress to return `handled:true` before Host queue admission. This prevents cancelled queued input from creating a successor Host run.

## Request lanes

- **DIRECT** — ordinary conversation and simple work.
- **LOOKUP** — focused read-only retrieval.
- **ACTION** — bounded reversible execution.
- **STAGED** — durable multi-step work requiring checkpoints, validators, retries, or interruption-safe orchestration.

Ticket creation does not imply STAGED execution.

## Recovery boundary

```text
Ticket accepted
  -> original model call
  -> eligible interruption evidence
  -> recovery authority
  -> bounded Direct Recovery
  -> response_ready committed once
  -> durable result
  -> delivery confirmation
  -> Ticket completed
```

### Restart recovery for held ingress

If the Gateway process disappears while later ingress is being held before Host admission, only accepted ingress with `bound_run_id IS NULL` is eligible for the dedicated restart-recovery path. It remains FIFO-fenced behind older non-terminal ingress.

Bound active runs remain owned by the normal Host/recovery reconciliation path; the held-ingress restart mechanism does not regenerate them.

### Exact Gateway-interruption recovery

A confirmed replacement of the Gateway process while a bound Direct model call is active is stronger evidence than an elapsed timer. v0.9.7 treats that process boundary as exact interruption evidence only after the Host has quiesced/stopped Gateway inference. Eligible active Direct calls may then be converted to pending Direct Recovery before the replacement Gateway starts.

An elapsed model-call deadline with an otherwise healthy Gateway/provider remains observation-only and never authorizes destructive recovery.

### SQLite BUSY rule

Transient `SQLITE_BUSY`/WAL contention while reading authority is not durable revocation. Bounded read tolerance must not race a still-running inference against a replacement attempt.

### Response/delivery rule

`response_ready` is immutable once committed. Delivery uncertainty permits bounded retransmission of a durable result; it does not by itself authorize inference regeneration.

### External side effects

CogentNexus-OpenClaw does not claim universal exactly-once execution of arbitrary external side effects. Repetition after interruption requires adapter-specific idempotency, receipts, or read-after-write proof.

## Operating modes

- **MANAGED** — CNX owns Ticket/session continuity and managed lifecycle boundaries.
- **PASSTHROUGH** — provider/model/auth routing remains OpenClaw-owned and managed provider ownership is inactive.
- **MAINTENANCE** — deliberate stop; durable state is preserved and recovery must not fight operator intent.

## Provider boundary

The durable managed-policy register is stored at `.cogentnexus-openclaw/host/managed-policy.md`; registration is separate from whether MANAGED integration is currently applied.

OpenClaw must remain usable without CogentNexus-OpenClaw. PASSTHROUGH/disable/uninstall boundaries must preserve native OpenClaw operation rather than making CNX a mandatory runtime dependency.

Managed local-provider ownership is Ollama-only. Cloud routes remain OpenClaw-owned pass-through. Historical LM Studio/provider work is retained as historical compatibility evidence and does not define the current managed-provider promise.

## OpenClaw compatibility

OpenClaw `2026.7.1-2` remains the regression/dev dependency pin used by the package test surface. The latest physical runtime acceptance is OpenClaw `2026.9.6`. These are distinct facts and must remain labeled separately.

## Accepted latest live proof

CNX-455 latest runtime compatibility acceptance on OpenClaw `2026.9.6` proved:

- supported-package upgrade convergence completed;
- CogentNexus-OpenClaw MANAGED authority is active at generation 54 with OpenClaw-owned provider/model/auth routing;
- default `ollama/qwen3.8:27b`, 24,576 context and six-hour Ollama keep-alive remained intact;
- GPT-6 Astra, GPT-6 Sol and GPT-6 Luna each completed physically with no reroute/fallback;
- the OpenClaw 2026.9.6 Gateway restart path required about 128.8 seconds, so CogentNexus-OpenClaw now uses a bounded 180-second restart command budget instead of the prior 60 seconds;
- focused regression, runtime self-test and the full `755 passed, 5 skipped, 38 subtests passed` suite are GREEN;
- final Gateway/CogentNexus-OpenClaw/Discord/supervisor health is GREEN.

CNX-442 remains the authoritative Stop/FIFO physical proof:

CNX-442 final physical acceptance proved:

- first Ticket bound to one Host run;
- second Ticket durably accepted and held at pre-dispatch;
- second Ticket had zero model/inference activity before Stop;
- Stop advanced owner generation exactly once;
- both Tickets became cancelled;
- held Ticket remained unbound;
- no successor Host run was created;
- no new CNX block error reached Dashboard/Discord;
- Gateway and Discord remained healthy after settlement.

See the CNX-442 final coordination report and [CURRENT_STATE.md](CURRENT_STATE.md) for exact IDs and current classification.
