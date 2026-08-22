# ChatGPT Session Handoff

Updated: 2026-08-22 20:44 ICT

This file exists so a new ChatGPT conversation can recover the active CogentNexus development context from GitHub instead of depending on the previous chat context window.

## Bootstrap instruction for a new ChatGPT conversation

The operator can say:

```text
ต่อ CogentNexus จาก GH coordination
```

The new ChatGPT conversation should then read, in this order:

1. `docs/operations/coordination/README.md`
2. `docs/operations/coordination/SIGNALS.md`
3. `docs/operations/coordination/ACTIVE.md`
4. the active task referenced by `ACTIVE.md`
5. the matching report under `docs/operations/coordination/reports/`, if present
6. the matching review under `docs/operations/coordination/reviews/`, if present
7. `docs/operations/STATUS.md`
8. `docs/operations/ROADMAP.md`
9. `docs/operations/WORKLOG.md`
10. `docs/operations/DECISIONS.md`

GitHub coordination state is the durable handoff authority for current work. Do not infer that a task was completed merely because an older chat said it was planned.

## Current coordination model

The human conversation remains in ChatGPT.

ChatGPT is the coordinator/reviewer and writes task authorization, review, and next-step state to GitHub.

Codex is the machine-side executor. The operator sends a short signal such as:

```text
ต่อ
```

Codex then synchronizes GitHub, reads the current coordination state itself, executes only the authorized active task, publishes the matching report/evidence references, and stops for review.

The operator should not need to carry task details or logs between ChatGPT and Codex.

## Current active task at this handoff

Task ID: `CNX-20260822-001`

Purpose: run the dedicated v0.9.3 Gateway durable-recovery convergence diagnostic on the real Windows machine and determine whether durable recovery state returns to `READY` by itself after automatic Gateway restoration, without an operator recovery command forcing convergence.

At this handoff, `ACTIVE.md` is `READY_FOR_CODEX`.

## Important current project boundaries

- v0.9.2 is the frozen Golden Baseline and must not be rewritten.
- v0.9.3 development is Ollama-only on the operator-facing managed path.
- process-tree kill is forbidden in disruptive recovery tests; only exact validated PIDs may be killed.
- recovery authority is event/durable-evidence driven; observation timeouts are safety/test fuses only.
- a recovered listener is not equivalent to durable recovery completion.
- real-machine evidence outranks roadmap assumptions.
- PR #24 remains Draft until the required real Windows recovery evidence is accepted.

## Most recent proven recovery facts before this handoff

- v0.9.3 real-machine baseline passed.
- a real OpenClaw Gateway exact-PID hard crash was injected safely.
- the Gateway listener recovered under CogentNexus supervision with a new PID.
- the previous full v3 test then observed `READY_WITH_WARNINGS` because the maintenance/recovery marker was still present shortly after listener recovery.
- cleanup via `cnx start` later restored a clean `READY` state, so the remaining question is whether the marker would converge by itself if observed without operator intervention.
- the dedicated Gateway Convergence diagnostic was created specifically to answer that question.

## Continuation rule

A new ChatGPT session should not ask the operator to restate the project history before checking GitHub coordination state.

If a Codex report for the active Task ID exists, review it first. If no report exists and `ACTIVE.md` is still `READY_FOR_CODEX`, tell the operator that Codex may be signaled with `ต่อ`.
