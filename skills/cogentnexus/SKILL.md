---
name: "cogentnexus"
description: "Durable Host-managed recovery, lifecycle control, and verified execution for OpenClaw work that needs CogentNexus machinery."
---

# CogentNexus

CogentNexus separates **continuity** from **execution depth**. In MANAGED mode, eligible owner messages may be durably admitted before inference, while ordinary DIRECT work remains lightweight.

Keep private reasoning private. Expose useful status, evidence, decisions, and results.

## Authority order

1. Preserve higher-priority safety, authorization, and platform constraints.
2. Preserve the user's intended outcome.
3. Respect durable Ticket/session/recovery state; do not duplicate accepted work blindly.
4. Choose the lightest reliable lane.
5. Claim consequential completion only from evidence.

## Request lanes

- **DIRECT** — ordinary conversation, explanation, brainstorming, simple drafting, and simple questions.
- **LOOKUP** — focused read-only retrieval.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — multi-step, consequential, interruption-prone, dependency-heavy, repeatedly failing, or independently verified work using the durable workflow controller.

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

- Recover committed state before starting replacement action.
- Never repeat external side effects blindly after interruption.
- `response_ready` is a durable boundary, not merely model text in memory.
- Delivery retry may retransport a durable result but must not regenerate inference without new recovery authority.
- Fence duplicate workers with leases/generations.
- Respect terminal/cancelled state and mode authority.
- Periodic supervision performs no model inference.
- A durably accepted request must become delivered/completed, cancelled, or explicitly failed with evidence.

## Module routing

Do not load heavy CogentNexus modules merely to answer an obvious DIRECT request.

Load references lazily and only when the selected lane/unit needs them:

- Ambiguity, consequence, safety, low confidence: [constitution.md](references/constitution.md)
- Multi-step execution loop: [task-loop.md](references/task-loop.md)
- Tool-heavy or repeatedly failing execution: [execution-success.md](references/execution-success.md)
- Resource/interruption survival: [resource-survival.md](references/resource-survival.md)
- Minimal durable memory: [minimal-memory.md](references/minimal-memory.md)
- Evidence-backed reusable lessons: [lesson-learning.md](references/lesson-learning.md)
- Resume from committed state: [task-resumption.md](references/task-resumption.md)
- Final output/delivery verification: [output-verification.md](references/output-verification.md)
- Architecture baseline: [architecture.md](references/architecture.md)
- Runtime toolkit details: [runtime-toolkit.md](references/runtime-toolkit.md)
- Recovery controller: [recovery-controller.md](references/recovery-controller.md)
- Capability registry: [capability-registry.md](references/capability-registry.md)
- Artifact integrity: [artifact-integrity.md](references/artifact-integrity.md)
- Runtime supervision: [runtime-supervisor.md](references/runtime-supervisor.md)
- Concurrency admission: [concurrency-manager.md](references/concurrency-manager.md)
- Context continuity: [context-continuity.md](references/context-continuity.md)
- Scheduler adapters: [scheduler-adapters.md](references/scheduler-adapters.md)
- Startup policy: [startup-policy.md](references/startup-policy.md)

## Validation

```sh
python skills/cogentnexus/scripts/validate.py --workspace-singleton
python skills/cogentnexus/scripts/workflow.py self-test
python skills/cogentnexus/scripts/cogent.py self-test
python skills/cogentnexus/scripts/runtime.py self-test
python -m unittest discover -s tests -v
```

## Current accepted checkpoint

Recovery Core: `eadb89099637d24f96e265a500d66c577aa939a3`, validated on OpenClaw `2026.7.1-2`. See root `docs/CURRENT_STATE.md` for accepted/deferred boundaries.
