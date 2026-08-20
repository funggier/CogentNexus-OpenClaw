---
name: "cogentnexus"
description: "Durable Host-managed recovery, lifecycle control, and verified execution for OpenClaw work that needs CogentNexus machinery."
---

# CogentNexus

CogentNexus separates **continuity** from **execution depth**. In MANAGED mode, eligible owner messages may be durably admitted before inference, while ordinary DIRECT work remains lightweight.

Keep private reasoning private. Expose useful status, evidence, decisions, and results.

## Authority order

1. Preserve higher-priority safety/authorization/platform constraints.
2. Preserve the user's intended outcome.
3. Respect durable Ticket/session/recovery state; do not duplicate accepted work blindly.
4. Choose the lightest reliable lane.
5. Claim consequential completion only from evidence.

## Request lanes

- **DIRECT** — ordinary conversation, explanation, brainstorming and simple drafting/questions.
- **LOOKUP** — focused read-only retrieval.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — multi-step, consequential, interruption-prone or independently verified work using the durable workflow controller.

Ticket creation does not imply STAGED execution.

## Host-managed continuity

For a committed Direct turn interrupted before durable response, the external Host may authorize Direct Recovery. Recovery must preserve the Ticket owner session/generation and original provider/model.

A transient SQLite BUSY read during authority polling is not durable revocation and must not create a competing retry while embedded inference is still running.

When durable CNX ownership exists, consume only the exact OpenClaw native restart continuation that belongs to the same session/generation/original prompt. Ordinary user messages and unreadable durable state fail open to native behavior.

## Operating modes

- **MANAGED** — Ticket-first continuity and CNX recovery/lifecycle ownership.
- **PASSTHROUGH** — CNX interception/background ownership disabled; OpenClaw behaves natively.
- **MAINTENANCE** — deliberate stop; state preserved and recovery must not fight operator intent.

`disable` means PASSTHROUGH. `stop` means MAINTENANCE.

## Runtime invariants

- recover committed state before starting replacement action;
- never repeat external side effects blindly after interruption;
- response-ready is a durable boundary, not merely model text in memory;
- delivery retry may retransport a durable result but must not regenerate inference without new recovery authority;
- fence duplicate workers with leases/generations;
- respect terminal/cancelled state and mode authority;
- periodic supervision performs no model inference;
- a durably accepted request must become delivered/completed, cancelled, or explicitly failed with evidence.

## Module routing

Load references lazily:

- architecture: `references/architecture.md`
- intent/lane: `references/intent-compiler.md`
- workflows: `references/workflow-runtime.md`
- recovery: `references/recovery-controller.md`
- lifecycle: `references/runtime-lifecycle.md`
- supervision: `references/runtime-supervisor.md`
- resumption: `references/task-resumption.md`
- startup: `references/startup-policy.md`
- context: `references/context-continuity.md`
- delivery: `references/output-verification.md`
- remaining specialized references only when required by the selected lane/unit.

## Current accepted checkpoint

Recovery Core: `eadb89099637d24f96e265a500d66c577aa939a3`, validated on OpenClaw `2026.7.1-2`. See root `docs/CURRENT_STATE.md` for accepted/deferred boundaries.
