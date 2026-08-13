---
name: "cogentnexus"
description: "Trusted workflows with optional hidden background startup."
---

# CogentNexus

Use this entry point for every request. Keep private reasoning private; expose useful status, evidence, decisions, and results.

## Kernel

1. Infer the outcome and observable success criteria.
2. Identify facts, constraints, authority, unknowns, and risks.
3. Query observed capabilities and runtime facts.
4. Compile the smallest capability-fit execution contract.
5. Choose Direct, Verified, or Durable.
6. Execute, verify, checkpoint, and preserve completed work.
7. Classify failures, recover within policy, and finish only with evidence.

## Startup policy

Startup is explicitly user-controlled and persisted across upgrades:

    python skills/cogentnexus/scripts/startup.py status
    python skills/cogentnexus/scripts/startup.py enable
    python skills/cogentnexus/scripts/startup.py disable
    python skills/cogentnexus/scripts/startup.py ensure

- enabled: reconcile a native background supervisor and verify it.
- disabled: remove only CogentNexus automatic triggers; preserve workflows, configuration, evidence, artifacts, and manual launch.
- unset: inspect only; never silently enable.

Windows background actions use `pythonw.exe` and hidden Task Scheduler settings so periodic checks do not flash a console window. Least-privilege installs use logon startup; true pre-login boot requires separately provisioned service credentials. Linux uses systemd, macOS uses launchd, and minimal Unix uses cron where available.

Manual startup remains available:

    python skills/cogentnexus/scripts/runtime.py lifecycle start --provider

## Durable workflow controller

For conversational Durable work use the trusted workflow plugin for atomic owner binding and detached execution. The native supervisor discovers resumable workflows, launches bounded controllers, and never performs inference inside the scheduler process.

## Runtime invariants

- Recover committed state before action.
- Verify manifests, artifacts, hashes, and terminal evidence.
- Fence duplicate workers and bound retries.
- Respect intentional maintenance.
- Keep external side effects outside automatic retry unless idempotent.
- Preserve the persisted startup choice during GitHub updates.
- Reconcile and verify enabled background startup after updates.

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

    python skills/cogentnexus/scripts/validate.py --workspace-singleton
    python skills/cogentnexus/scripts/workflow.py self-test
    python skills/cogentnexus/scripts/cogent.py self-test
    python skills/cogentnexus/scripts/runtime.py self-test

All must pass before claiming runtime changes complete.
