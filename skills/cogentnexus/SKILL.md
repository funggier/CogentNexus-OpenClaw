---
name: "cogentnexus"
description: "Enforce trusted owner-bound starts and audited operator exceptions."
---

# CogentNexus

Use this single entry point. Keep private reasoning private; expose useful status, evidence, decisions, and results.

## Kernel

1. **Purpose** - infer the requested outcome and observable success criteria.
2. **Understanding** - identify facts, constraints, authorization, unknowns, and risks.
3. **Capability and resources** - query observed capabilities and runtime facts.
4. **Intent compilation** - transform the request into the smallest capability-fit execution contract.
5. **Decision** - choose the smallest robust, authorized plan.
6. **Action and check** - execute, verify, checkpoint, and preserve completed work.
7. **Recovery and reflection** - classify failure, change strategy within policy, and finish only with evidence.

Never expose chain-of-thought, invent material requirements, store unrequested secrets, bypass authorization, or claim intended work as completed.

## Intent compiler

Compile simple requests internally: define observable acceptance criteria, inspect current state and existing solutions, choose executor size from observed capability, split dependency-heavy work into verifiable components, define validator/retry/dependencies, and keep orchestration and completion authority outside bounded generators.

Select the smallest lane:

- **Direct** - one small reversible action with immediately observable results.
- **Verified** - multi-step, generated, structured, or integration-sensitive work.
- **Durable** - long, resource-heavy, detached, costly-to-duplicate, or interruption-prone work.

Do not require the user to perform decomposition or prompt engineering. Ask only for missing authority, irreversible external action, a consequential product choice, or undiscoverable required input.

## Durable workflow controller

For Durable work, compile a JSON workflow manifest. When the work belongs to the current OpenClaw conversation, start it through the `cogent_workflow_start` plugin tool; that tool atomically initializes the workflow, binds the trusted current owner session, and launches the detached controller. This is the default conversational path because terminal completion must wake the owner automatically. Use the CLI sequence below only for operator-managed or explicitly unbound workflows:

    python skills/cogentnexus/scripts/workflow.py validate <manifest.json>
    python skills/cogentnexus/scripts/workflow.py --root <workspace> init <manifest.json> --operator-unbound --operator-reason "<audited reason>"
    python skills/cogentnexus/scripts/workflow.py --root <workspace> run <task-id>
    python skills/cogentnexus/scripts/workflow.py --root <workspace> status <task-id>

`run` owns continuation: it selects the next dependency-ready step, executes one bounded command or Ollama generation, runs an external validator, hashes declared artifacts, checkpoints state and ledger evidence, retries only within the declared ceiling, and advances without waiting for conversational supervision.

For a background workflow started on behalf of a conversation, use `cogent_workflow_start`; do not call `init` or `bind-owner` through shell tools. Terminal completion, blocking, or failure writes a durable outbox. The CogentNexus plugin claims that outbox idempotently, records a managed TaskFlow result, and schedules one owner continuation turn so the agent verifies the result and proceeds without waiting for a user prompt.

A live worker PID fences duplicate execution. After interruption, a valid produced artifact is recovered through its validator; an idempotent incomplete step is requeued; a non-idempotent interrupted step is blocked for review. The user must not need to say that a worker appears finished before the next verified step starts.

Use command executors without a shell. Treat Ollama output as a candidate until its validator passes. Keep external side effects outside automatic retry unless idempotency is proven.

## Enforced mode

For conversational Durable work, owner binding is a runtime invariant, not model guidance. The `cogent_workflow_start` tool initializes the manifest and trusted owner binding atomically. Direct conversational attempts to call `workflow.py init`, use `--operator-unbound`, or bind an owner manually are blocked by the plugin hook. Operator-unbound workflows remain available only as an explicit audited CLI path with a recorded reason.

Controllers reject workflows without a valid ownership mode. Completion delivery remains pending across gateway or scheduling failures, records attempt/error evidence, and retries idempotently until the tagged owner continuation is durably scheduled.

## Always-on resumption

The native five-minute supervisor deterministically discovers non-terminal workflows. With `supervisor tick --execute-safe`, it launches bounded detached workflow controllers up to the configured ceiling. Controllers run outside the scheduler process, survive conversation/tool interruption, claim workflow ownership, and continue from verified state.

The periodic supervisor must not call an LLM or wait for inference. It only probes, discovers, fences, and launches. The detached workflow controller owns execution, validation, retry, checkpointing, and terminal state. Live controller or step PIDs prevent duplicate execution; dead ownership is reclaimable from durable evidence.

## Automatic session rotation

For a durable task explicitly bound to an OpenClaw session, context monitoring checkpoints at 25%, prepares handoff at 35%, and requests rotation at 45% by default. A verified ROTATE handoff is bridged through the CogentNexus rotation plugin into one generation-fenced managed TaskFlow and a clean temporary worker session.

The worker claims the handoff before action, resumes only the recorded next step, verifies and commits evidence, releases its lease, and returns a compact result to the owner. Duplicate generations resolve to the existing flow. Unbound conversations, stale telemetry, invalid handoffs, and irreversible side effects never rotate automatically.

Use `phase3.py context rotations` as the management view for bound session, generation, worker lease, status, decision, and result.

## Runtime invariants

- Load committed state and recover prepared transactions before action.
- Query capability availability instead of inventing self-knowledge.
- Execute bounded commands and record semantic outcomes.
- Verify manifests and artifacts against the current state revision.
- Reject absent, stale, failed, or changed completion evidence.
- Classify failures before retry; stop at the retry ceiling or after repeated strategy.
- Separate model-generated work from deterministic repair in evidence.
- Default to one inference lane unless admission permits more.
- Fence duplicate workers with locks and live-worker identity.
- Commit durable handoff state before rotation or abandonment.
- Never auto-bypass permissions, install dependencies, delete data, or perform external actions.
- Preserve monotonic ledger history without chain-of-thought.
- Planned shutdown must establish maintenance mode before stopping services.
- Lifecycle start must be idempotent and clear maintenance mode only after health verification.

Use `cogent.py` for Phase 1-2 task operations, `phase3.py` for health, continuity, and always-on workflow discovery, and `workflow.py` for verified autonomous component workflows.

## Module routing

- Simple intent, lane selection, or prompt compilation: [intent-compiler.md](references/intent-compiler.md).
- Durable workflow manifests and continuation: [workflow-runtime.md](references/workflow-runtime.md).
- Ambiguous or safety-sensitive work: [constitution.md](references/constitution.md).
- Multi-step work: [task-loop.md](references/task-loop.md).
- Tool-heavy, local-model, or failing work: [execution-success.md](references/execution-success.md).
- Large or interruption-prone work: [resource-survival.md](references/resource-survival.md).
- Durable information: [minimal-memory.md](references/minimal-memory.md).
- Reusable failure lessons: [lesson-learning.md](references/lesson-learning.md).
- Risky or resumed work: [task-resumption.md](references/task-resumption.md).
- Runtime supervision: [runtime-supervisor.md](references/runtime-supervisor.md).
- Lifecycle: [runtime-lifecycle.md](references/runtime-lifecycle.md).
- Admission: [concurrency-manager.md](references/concurrency-manager.md).
- Context rotation: [context-continuity.md](references/context-continuity.md).
- Scheduling: [scheduler-adapters.md](references/scheduler-adapters.md).
- Final delivery: [output-verification.md](references/output-verification.md).
- Runtime changes: [architecture.md](references/architecture.md).
- Toolkit: [runtime-toolkit.md](references/runtime-toolkit.md), [recovery-controller.md](references/recovery-controller.md), [capability-registry.md](references/capability-registry.md), and [artifact-integrity.md](references/artifact-integrity.md).

For simple tasks, apply the Kernel internally and answer concisely.

## Runtime loop

    intent -> compile -> select lane -> load/recover -> probe -> bounded action
    PASS -> validate -> hash -> checkpoint -> automatically start next ready step
    FAIL -> classify -> bounded retry or materially different strategy
    INTERRUPT -> fence -> inspect validator/artifacts -> recover, requeue, or block

## Validation

    python skills/cogentnexus/scripts/validate.py --workspace-singleton
    python skills/cogentnexus/scripts/workflow.py self-test
    python skills/cogentnexus/scripts/cogent.py self-test
    python skills/cogentnexus/scripts/phase3.py self-test
