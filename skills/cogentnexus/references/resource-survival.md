# Resource Survival

Use before major actions in large, risky, or interruption-prone work.

Estimate context remaining, runtime, output size, file count, tool-call count, concurrency limits, current progress, and prior failures. Exact measurement is unnecessary.

- **Low risk:** proceed normally.
- **Medium risk:** split work, reduce complexity, checkpoint, or defer optional work.
- **High risk:** do not continue blindly; persist state, reduce scope, or request the smallest necessary decision.

Prefer small complete steps. Avoid unnecessary full-project reads and oversized outputs. Preserve verified work. If interrupted, resume from the last checkpoint. Prefer partial verified value over total failure.

## Local-model completion policy

For local models, especially tasks containing six or more explicit items, dependency graphs, or long multi-step output:

1. Externalize the complete item manifest before execution and count it deterministically.
2. Process bounded batches and checkpoint every material verified batch.
3. Validate counts, uniqueness, dependencies, schemas, and file state with code or tools rather than model self-assessment.
4. Treat an inference response as a proposal until the validator passes.
5. After validator failure, reconstruct from the source constraints and error list in a fresh attempt; do not merely echo-edit the rejected answer.
6. Reserve enough output budget for a final answer when reasoning mode is enabled.
7. Stop repeated identical retries and change strategy, model, decomposition, or validator.
8. Never let one long inference be the only copy of task progress.

On this host, respect the single inference lane: do not start a nested CLI agent from an active session when it would queue behind itself. Use a 32K effective context cap and staged checkpoints for larger work; longer timeout does not replace progress validation.