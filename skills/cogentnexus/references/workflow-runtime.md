# Durable Workflow Runtime

Use for long, detached, multi-component, local-model, or interruption-prone execution.

A schemaVersion 1 manifest defines taskId and dependency-ordered steps. Every step declares a command or Ollama executor, outputs, optional deterministic validator, maximumAttempts, and whether interruption retry is idempotent.

Initialize once, then call `workflow.py run`. The controller—not a conversational model—selects ready steps, executes them, validates outputs, records SHA-256 artifact evidence, checkpoints revisioned state, and continues until completed, blocked, or failed.

State and append-only ledger evidence live under `.cogent/workflows/<task-id>`. Manifest integrity is checked before each transition.

Recovery rules:

- live runner PID: report busy and never duplicate the step;
- dead runner plus passing validator and declared artifacts: recover completed;
- dead runner plus idempotent incomplete step: requeue within its attempt ceiling;
- dead runner plus non-idempotent step: block for human review.

Command execution never uses a shell. Paths for prompts and artifacts must remain inside the workflow root. Model output remains a candidate until external validation passes.
