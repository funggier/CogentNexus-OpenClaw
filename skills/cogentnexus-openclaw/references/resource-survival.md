# Resource Survival

Use before major actions in large, risky, or interruption-prone work.

Estimate context remaining, runtime, output size, file count, tool-call count, concurrency limits, current progress, and prior failures. Prefer small complete steps, durable checkpoints, and verified partial value.

For local or bounded models:

1. Externalize the item manifest.
2. Process bounded units and checkpoint verified results.
3. Validate counts, dependencies, schemas, and artifacts deterministically.
4. Treat inference output as a proposal until validation passes.
5. Change strategy after repeated failure.
6. Never keep the only copy of progress in one inference.

Concurrency is resource policy, not a universal constant. Default to one inference lane. A host may use adaptive multi-lane execution only after capability and memory admission, within an explicit ceiling. On a single-lane host, end the owner turn before a detached inference worker starts so it cannot queue behind itself.

When context reaches the configured soft threshold, checkpoint. At handoff threshold, route new heavy work to a clean detached session. At critical threshold, commit and rotate before continuing.
