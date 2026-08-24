# Context Continuity

Durable work identity must not depend on keeping unlimited model context alive.

Context compaction/rotation may discard transient reasoning while Tickets, recovery state, workflow checkpoints, artifacts and receipts remain authoritative.

For Direct Recovery, reconstruct only the minimum owner-session context required while preserving original Ticket prompt/model provenance. A native restart continuation that merely repeats the same durable prompt is not new user intent when CNXCLAW already owns that recovery.

For long STAGED work, checkpoint before context rotation and rehydrate from committed artifacts/state rather than replaying side effects.
