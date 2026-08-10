# Context Continuity

Task lifetime must not depend on session lifetime.

Use CONTINUE, CHECKPOINT, HANDOFF, and ROTATE. Defaults are 25%, 35%, and 45% of fresh reported context. Before handoff or rotation, verify the current unit and atomically commit task state.

Only durable tasks explicitly bound with `context bind` are eligible. The monitor deduplicates by action and task revision, creates an integrity-bound handoff, and exposes management state with:

    python skills/cogentnexus/scripts/phase3.py context monitor --execute-safe
    python skills/cogentnexus/scripts/phase3.py context rotations
    python skills/cogentnexus/scripts/phase3.py context inspect --task-id ID

At ROTATE, the trusted CogentNexus rotation plugin validates the prepared handoff, derives the owner from trusted session context, creates or reuses one generation-fenced managed TaskFlow, and launches a clean temporary worker session. The worker must claim the lease, resume only the recorded next action, verify artifacts, commit state, release the lease, and return a compact result to the owner.

TaskFlow owns parent/child lifecycle. CogentNexus owns evidence, thresholds, authorization boundaries, generation identity, and lease fencing. Unbound conversations, stale usage, tampered or non-ROTATE handoffs, and duplicate generations are never launched automatically.

The periodic host supervisor never runs inference. Session rotation occurs from the trusted post-turn plugin bridge. Use fixtures for acceptance; never force-rotate a live owner merely to test policy.