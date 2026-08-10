# Context Continuity

Task lifetime must not depend on session lifetime.

Threshold actions are CONTINUE, CHECKPOINT, HANDOFF, and ROTATE. Before handoff or rotation, verify the current unit and atomically commit task state. Create a minimal handoff outside session context:

    python skills/cogentnexus/scripts/phase3.py context status --used-tokens N --maximum-tokens N
    python skills/cogentnexus/scripts/phase3.py context checkpoint --task-id ID --owner-session SESSION --next-action ACTION --used-tokens N --maximum-tokens N
    python skills/cogentnexus/scripts/phase3.py context claim --task-id ID --worker-session SESSION
    python skills/cogentnexus/scripts/phase3.py context release --task-id ID --worker-session SESSION --lease-id ID --result completed --summary SUMMARY

Bind a durable task to its real OpenClaw session once, then let the five-minute supervisor observe machine-readable usage automatically:

    python skills/cogentnexus/scripts/phase3.py context bind --task-id ID --session-key KEY --owner-session SESSION --next-action ACTION
    python skills/cogentnexus/scripts/phase3.py context monitor --task-id ID --execute-safe
    python skills/cogentnexus/scripts/phase3.py context unbind --task-id ID

The monitor reads `openclaw sessions --json`, requires `totalTokensFresh=true`, and compares `totalTokens` with `contextTokens`. At CHECKPOINT, HANDOFF, or ROTATE it prepares an external handoff only when the threshold action or task-state revision changed, preventing a five-minute generation storm. Missing, stale, or invalid session usage cannot trigger a checkpoint. ROTATE is a signal to the trusted calling layer; the deterministic supervisor never creates or redirects a user session itself.

The handoff contains goal, state revision, verified artifacts, failures, next action, authorization boundary, generation, and lease. It excludes full conversation history, secrets, and chain-of-thought. A fresh worker receives only the handoff and required artifacts. With one inference lane, the owner must finish its turn before the detached worker starts. With multiple lanes, only independent artifact scopes may run concurrently.

TaskFlow owns the durable parent/child lifecycle. CogentNexus owns task evidence and handoff fencing. The calling integration should create a managed TaskFlow, link the detached worker, persist only handoff identifiers in stateJson, and return a compact verified result to the owner.

The optional `plugins/cogentnexus-rotation` OpenClaw plugin implements that calling integration. Its `cogent_rotation` tool defaults to dry-run, accepts only a validated prepared `ROTATE` handoff, derives the owner from trusted tool context, and uses the task generation to fence duplicate worker starts. The clean worker must claim the handoff before acting and release its lease after committing verified results. A rotation changes the worker session, not the user's source conversation; compact results return through the managed TaskFlow.
