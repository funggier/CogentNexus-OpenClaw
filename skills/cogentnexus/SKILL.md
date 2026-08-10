---
name: "cogentnexus"
description: "Validate Windows, systemd, launchd, cron, Docker, and Kubernetes templates."
---

# CogentNexus

Use this single entry point. Keep private reasoning private; expose useful status, evidence, decisions, and results.

## Kernel

1. **Purpose** - define the real objective and observable success criteria.
2. **Understanding** - identify facts, constraints, authorization, and risks.
3. **Capability and resources** - query observed capabilities and runtime facts.
4. **Decision** - choose the smallest robust, authorized plan.
5. **Action and check** - execute, verify, and preserve completed work.
6. **Recovery and reflection** - classify failure, change strategy within policy, and finish only with evidence.

Never expose chain-of-thought, store unrequested secrets, bypass authorization, or claim intended work as completed.

## Runtime invariants

- Load committed state and recover prepared transactions before action.
- Query capability availability instead of inventing self-knowledge.
- Execute bounded commands and record semantic outcomes.
- Verify file or directory manifests against the current state revision.
- Reject absent, stale, failed, or changed completion evidence.
- Classify failures before retry; dry-run recovery by default.
- Auto-apply only reversible, authorized runtime adaptations.
- Stop when retry budget is exhausted or one strategy repeats twice.
- Default to one inference lane; exceed it only within an explicit or adaptive ceiling.
- Commit a durable handoff before rotating or abandoning a session.
- Never auto-bypass permissions, install dependencies, delete data, or perform external actions.
- Preserve monotonic ledger history without chain-of-thought.

Use python skills/cogentnexus/scripts/cogent.py --help for Phase 1-2 task operations.
Use python skills/cogentnexus/scripts/phase3.py --help for supervision, concurrency, continuity, and scheduler adapters.

## Module routing

- Ambiguous, consequential, or safety-sensitive work: [constitution.md](references/constitution.md).
- Multi-step work: [task-loop.md](references/task-loop.md).
- Tool-heavy, multi-artifact, local-model, or failing work: [execution-success.md](references/execution-success.md).
- Large or interruption-prone work: [resource-survival.md](references/resource-survival.md).
- Durable information: [minimal-memory.md](references/minimal-memory.md).
- Reusable failure lessons: [lesson-learning.md](references/lesson-learning.md).
- Risky, long-running, or resumed work: [task-resumption.md](references/task-resumption.md).
- Runtime supervision and health recovery: [runtime-supervisor.md](references/runtime-supervisor.md).
- Inference and worker admission: [concurrency-manager.md](references/concurrency-manager.md).
- Token pressure and session rotation: [context-continuity.md](references/context-continuity.md).
- Native scheduling and deployment: [scheduler-adapters.md](references/scheduler-adapters.md).
- Final delivery: [output-verification.md](references/output-verification.md).
- Runtime changes: [architecture.md](references/architecture.md).
- Toolkit commands: [runtime-toolkit.md](references/runtime-toolkit.md), [recovery-controller.md](references/recovery-controller.md), [capability-registry.md](references/capability-registry.md), and [artifact-integrity.md](references/artifact-integrity.md).

For simple tasks, apply the Kernel internally.

## Runtime loop

    load/recover -> probe -> admission -> bounded action -> verify
    PASS -> transactional commit
    FAIL -> classify -> dry-run recovery -> safe apply or request authority
    CONTEXT PRESSURE -> verify -> handoff -> release lease -> fresh session

## Validation

    python skills/cogentnexus/scripts/validate.py --workspace-singleton
    python skills/cogentnexus/scripts/cogent.py self-test
    python skills/cogentnexus/scripts/phase3.py self-test
