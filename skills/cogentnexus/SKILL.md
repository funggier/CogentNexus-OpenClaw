---
name: "cogentnexus"
description: "Durable Host-managed recovery, lifecycle control, and verified execution for OpenClaw work that needs CogentNexus machinery."
---

# CogentNexus

CogentNexus separates **continuity** from **execution depth**.

The Host/Ticket layer protects accepted work outside model inference. This skill is loaded only when managed policy or observed task requirements need CogentNexus execution machinery. Do not load heavy CogentNexus modules merely to answer an obvious DIRECT conversational request.

Keep private reasoning private. Expose useful status, evidence, decisions, and results.

## Authority order

1. Preserve higher-priority safety, authorization, and platform constraints.
2. Preserve the user's intent and requested outcome.
3. Respect already-committed Host/Ticket state; do not duplicate accepted work blindly.
4. Choose the lightest reliable request lane before loading heavy references.
5. Use deterministic evidence before claiming consequential completion.

## Request lanes

- **DIRECT** — greetings, casual conversation, explanations, advice, brainstorming, short drafting, and simple questions answerable from current context. Answer naturally; do not create contracts, checkpoints, reviewers, runtime probes, or staged workflows unless the request actually needs them.
- **LOOKUP** — focused read-only retrieval. Load only the minimum source/tool surface needed.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — multi-step, consequential, interruption-prone, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work. Use the durable workflow controller.

Escalate only when observed complexity or risk justifies it.

## Durable kernel for STAGED work

1. Infer the outcome and observable acceptance criteria.
2. Identify only material facts, constraints, authority, unknowns, and risks.
3. Query observed capabilities/runtime facts needed for the current bounded unit.
4. Compile the smallest capability-fit execution contract.
5. Execute from committed state.
6. Validate deterministic evidence and required semantic review.
7. Checkpoint completed work and recover within bounded policy.
8. Finish only from terminal evidence.

## Host-managed continuity

In MANAGED mode, eligible owner messages may be committed to a lightweight durable Ticket before inference. Ticket creation does **not** imply STAGED execution.

If a committed direct turn is interrupted by confirmed Gateway failure, the external Host Controller may promote it to durable recovery so the user does not need to repeat the message.

## Operating modes

- **MANAGED** — CogentNexus owns Ticket-first continuity and managed lifecycle/recovery behavior.
- **PASSTHROUGH** — CogentNexus interception/background ownership are disabled; OpenClaw behaves normally.
- **MAINTENANCE** — intentional stop; durable state remains and recovery must not fight operator intent.

`disable` means PASSTHROUGH. `stop` means MAINTENANCE.

## Runtime invariants

- Recover committed state before new action.
- Never repeat external side effects blindly after interruption.
- Verify manifests, artifacts, hashes, terminal state, and required reviewer evidence.
- Fence duplicate workers with leases/generations and bound retries.
- Respect cancellation, PASSTHROUGH, and intentional maintenance.
- Keep OpenClaw usable when CogentNexus is disabled.
- Keep CogentNexus durable control state independent of a live OpenClaw inference process.
- A durably accepted request must eventually become delivered/completed, cancelled, or explicitly failed with evidence.
- Periodic supervision performs no model inference.

## Module routing

Load references lazily and only for the selected lane/unit:

- Lane/intent compilation: [intent-compiler.md](references/intent-compiler.md)
- Architecture baseline: [architecture.md](references/architecture.md)
- Durable workflows: [workflow-runtime.md](references/workflow-runtime.md)
- Ambiguous or safety-sensitive work: [constitution.md](references/constitution.md)
- Multi-step execution: [task-loop.md](references/task-loop.md)
- Tool-heavy/failing work: [execution-success.md](references/execution-success.md)
- Interruption/resource survival: [resource-survival.md](references/resource-survival.md)
- Minimal durable memory: [minimal-memory.md](references/minimal-memory.md)
- Resumption: [task-resumption.md](references/task-resumption.md)
- Supervision: [runtime-supervisor.md](references/runtime-supervisor.md)
- Lifecycle: [runtime-lifecycle.md](references/runtime-lifecycle.md)
- Startup policy: [startup-policy.md](references/startup-policy.md)
- Concurrency: [concurrency-manager.md](references/concurrency-manager.md)
- Context continuity: [context-continuity.md](references/context-continuity.md)
- Scheduling: [scheduler-adapters.md](references/scheduler-adapters.md)
- Final delivery: [output-verification.md](references/output-verification.md)
- Toolkit details: [runtime-toolkit.md](references/runtime-toolkit.md), [recovery-controller.md](references/recovery-controller.md), [capability-registry.md](references/capability-registry.md), [artifact-integrity.md](references/artifact-integrity.md)

## Validation

```sh
python skills/cogentnexus/scripts/validate.py --workspace-singleton
python skills/cogentnexus/scripts/workflow.py self-test
python skills/cogentnexus/scripts/cogent.py self-test
python skills/cogentnexus/scripts/runtime.py self-test
python -m unittest discover -s tests -v
```

All required gates must pass before runtime changes are reported complete.
