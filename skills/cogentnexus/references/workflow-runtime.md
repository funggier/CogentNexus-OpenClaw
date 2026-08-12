# Durable Workflow Runtime

Use for long, detached, multi-component, local-model, or interruption-prone execution.

A schemaVersion 1 manifest defines taskId and dependency-ordered steps. Every step declares a command or Ollama executor, outputs, optional deterministic validator, maximumAttempts, and whether interruption retry is idempotent.

Initialize once, then call `workflow.py run`. The controller selects ready steps, executes them, validates outputs, records SHA-256 evidence, checkpoints state, and continues until completed, blocked, or failed.

When a workflow belongs to an OpenClaw conversation, call `workflow.py bind-owner <task-id> --session-key <trusted-key>` after initialization. A terminal transition commits `completion.json` as a durable outbox. The CogentNexus plugin polls pending outboxes, mirrors the terminal result into a managed TaskFlow, schedules one idempotently tagged owner turn, and marks delivery only after scheduling succeeds.

For always-on operation, call `workflow.py supervise` to observe resumable workflows or `workflow.py supervise --execute` to launch bounded detached controllers. The runtime scheduled supervisor invokes this deterministic discovery path during safe ticks.

State and ledger evidence live under `.cogent/workflows/<task-id>`. Manifest integrity is checked before transitions. A controller PID fences duplicate controllers, while step runner PIDs fence duplicate execution.

Recovery rules:

- live controller or runner: observe only;
- dead runner plus passing validator and declared artifacts: recover completed;
- dead runner plus idempotent incomplete step: requeue within its attempt ceiling;
- dead runner plus non-idempotent step: block for review.

Command execution never uses a shell. Prompt and artifact paths remain inside the workflow root. Model output stays a candidate until external validation passes.
