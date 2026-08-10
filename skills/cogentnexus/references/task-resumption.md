# Task Resumption

Use for risky, long-running, detached, or interrupted work.

Active task truth lives under .cogent/tasks/<task-id>. State, ledger, verification, artifact evidence, and handoff must be sufficient to resume without conversation reconstruction.

Before resuming:

1. Recover prepared transactions.
2. Inspect state revision and latest ledger sequence.
3. Verify previously completed artifacts.
4. Inspect the handoff generation and lease.
5. Confirm the task is not abandoned and does not conflict with the current request.
6. Claim the handoff before action.
7. Execute the smallest next unit and checkpoint after verification.

Do not silently resume unrelated stale work. Do not rerun external operations until remote state is checked. A live lease fences duplicate workers; an expired lease may be reclaimed with a new lease identifier. TaskFlow may preserve owner and child lifecycle, while CogentNexus remains the source of task evidence.
