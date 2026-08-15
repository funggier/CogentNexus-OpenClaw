---
name: "cogentnexus"
description: "Durable Host-managed continuity, recovery, lifecycle control, and verified execution for OpenClaw."
---

# CogentNexus

CogentNexus separates **continuity** from **execution depth**. The Host Controller keeps accepted work durable outside inference, while this skill governs the managed execution behavior used after admission.

Do not make ordinary conversation heavy merely because CogentNexus is enabled. Keep private reasoning private and expose only useful status, evidence, decisions, and results.

## Authority and execution order

1. Preserve higher-priority safety, authorization, and platform constraints.
2. Preserve the user's intent, requested outcome, and session identity.
3. Rely on Host/Ticket state for continuity; do not recreate or duplicate accepted work blindly.
4. Choose the lightest reliable execution lane before loading heavy workflow machinery.
5. Use deterministic evidence and bounded recovery before claiming consequential work complete.

## Kernel

1. Infer the requested outcome and observable success criteria.
2. Identify only the facts, constraints, authority, unknowns, and risks that materially affect the request.
3. Choose the lightest reliable lane:
   - **DIRECT** for greetings, conversation, explanation, advice, brainstorming, and other low-risk work that can be answered from current context.
   - **LOOKUP** for focused read-only retrieval.
   - **ACTION** for bounded reversible execution with proportionate verification.
   - **STAGED / DURABLE** for multi-step, consequential, interruption-prone, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work.
4. For DIRECT work, answer naturally without runtime probes, contracts, checkpoints, reviewers, or staged references unless the request actually needs them.
5. For LOOKUP/ACTION, load only the capabilities and verification needed for the bounded task.
6. For STAGED/DURABLE work, query observed capabilities and runtime facts, compile the smallest capability-fit execution contract, execute from durable state, verify evidence, checkpoint progress, and recover within policy.
7. Finish only when the request reaches an appropriate terminal outcome; never silently lose accepted work.

## Host-managed continuity

In MANAGED mode, eligible owner messages may be committed to the durable Ticket store before model inference. Ticket creation does **not** imply a staged workflow. A lightweight DIRECT Ticket can remain a direct conversation turn unless interruption or observed complexity requires escalation.

If a committed direct turn is interrupted by confirmed Gateway failure, the Host Controller may promote it to durable recovery so the user does not need to repeat the message.

## Operating modes

- **MANAGED** — CogentNexus owns Ticket-first continuity, deterministic recovery supervision, and managed runtime lifecycle behavior.
- **PASSTHROUGH** — CogentNexus interception and background ownership are disabled; OpenClaw behaves normally.
- **MAINTENANCE** — deliberate stop state; durable state is preserved and automatic recovery must not fight operator intent.

`disable` means PASSTHROUGH. `stop` means MAINTENANCE. Keep those semantics distinct.

## Durable workflow controller

For durable conversational work, use the trusted workflow plugin for atomic owner binding and detached execution. The native supervisor discovers resumable workflows, launches bounded controllers, and never performs inference inside the scheduler process.

Executor output is not completion evidence. Deterministic validators, stored artifacts, required reviewer policy, and controller state decide whether durable work may advance to PASS.

## Runtime invariants

- Recover committed state before new action.
- Never repeat external side effects blindly after interruption.
- Verify manifests, artifacts, hashes, and terminal evidence.
- Fence duplicate workers and bound retries.
- Respect intentional maintenance and PASSTHROUGH ownership boundaries.
- Keep OpenClaw usable when CogentNexus is disabled.
- Keep CogentNexus durable control state independent of a live OpenClaw inference process.
- Preserve persisted startup/operating-mode choices across updates.
- A durably accepted user request must eventually become delivered/completed, cancelled, or explicitly failed with evidence.

## Module routing

- Simple intent and lane selection: [intent-compiler.md](references/intent-compiler.md).
- Durable workflows: [workflow-runtime.md](references/workflow-runtime.md).
- Ambiguous or safety-sensitive work: [constitution.md](references/constitution.md).
- Multi-step work: [task-loop.md](references/task-loop.md).
- Tool-heavy or failing work: [execution-success.md](references/execution-success.md).
- Large or interruption-prone work: [resource-survival.md](references/resource-survival.md).
- Durable information: [minimal-memory.md](references/minimal-memory.md).
- Reusable lessons: [lesson-learning.md](references/lesson-learning.md).
- Risky or resumed work: [task-resumption.md](references/task-resumption.md).
- Supervision: [runtime-supervisor.md](references/runtime-supervisor.md).
- Lifecycle: [runtime-lifecycle.md](references/runtime-lifecycle.md).
- Startup policy: [startup-policy.md](references/startup-policy.md).
- Admission: [concurrency-manager.md](references/concurrency-manager.md).
- Context rotation: [context-continuity.md](references/context-continuity.md).
- Scheduling: [scheduler-adapters.md](references/scheduler-adapters.md).
- Final delivery: [output-verification.md](references/output-verification.md).
- Architecture: [architecture.md](references/architecture.md).
- Toolkit: [runtime-toolkit.md](references/runtime-toolkit.md), [recovery-controller.md](references/recovery-controller.md), [capability-registry.md](references/capability-registry.md), and [artifact-integrity.md](references/artifact-integrity.md).

## Validation

```sh
python skills/cogentnexus/scripts/validate.py --workspace-singleton
python skills/cogentnexus/scripts/workflow.py self-test
python skills/cogentnexus/scripts/cogent.py self-test
python skills/cogentnexus/scripts/runtime.py self-test
python -m unittest discover -s tests -v
```

All required gates must pass before claiming runtime changes complete.
