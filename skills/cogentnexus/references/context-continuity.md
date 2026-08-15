# Context Continuity

Task lifetime and delivery lifetime must not depend on one model context or one OpenClaw session turn.

Use CONTINUE, CHECKPOINT, HANDOFF, and ROTATE for durable tasks. Defaults are 25%, 35%, and 45% of fresh reported context. Before handoff or rotation, verify the current bounded unit and atomically commit task state.

Only durable tasks explicitly bound with `context bind` are eligible for proactive TaskFlow rotation. The monitor deduplicates by action and task revision, creates an integrity-bound handoff, and exposes management state with:

```text
python skills/cogentnexus/scripts/runtime.py context monitor --execute-safe
python skills/cogentnexus/scripts/runtime.py context rotations
python skills/cogentnexus/scripts/runtime.py context inspect --task-id ID
```

At ROTATE, the trusted CogentNexus OpenClaw Bridge validates the prepared handoff, derives the owner from trusted session context, creates or reuses one generation-fenced managed TaskFlow, and launches a clean temporary worker session. The worker must claim the lease, resume only the recorded next action, verify artifacts, commit state, release the lease, and return a compact result to the owner.

TaskFlow owns parent/child lifecycle. CogentNexus owns evidence, thresholds, authorization boundaries, generation identity, lease fencing, and durable continuity. Unbound conversations, stale usage, tampered or non-ROTATE handoffs, and duplicate generations are never launched automatically.

## Successful compaction is not completion

OpenClaw history compaction may succeed while the logical task still has non-terminal durable work. A successful compaction event therefore triggers a **Post-Compaction Continuation Guard** only when the same owner session still has pending Ticket/workflow/delivery state.

The guard is delayed and idempotently tagged. It resumes from committed Ticket/workflow/handoff state; it never reconstructs discarded private reasoning. If the original turn continues normally to its end, the bridge cancels the guard. If the guard fires after work is already terminal, it must observe terminal state and avoid duplicate output or side effects.

## Reply delivery is a separate continuity boundary

A successful `agent_end` with visible output means the response is ready, not necessarily fully delivered. CogentNexus keeps that direct Ticket non-terminal until final delivery settles successfully. Partial output, failed/cancelled final dispatch, or a missing delivery receipt promotes the work back to durable recovery.

Terminal workflow/Ticket outbox scheduling follows the same rule: scheduling a continuation is not proof of delivery. The marked continuation must itself settle before the outbox becomes delivered.

The periodic Host supervisor never runs inference. Session rotation and delivery/compaction guards are coordinated through the trusted OpenClaw Bridge. Use deterministic fixtures for acceptance; never force-rotate or interrupt a live owner merely to test policy.
