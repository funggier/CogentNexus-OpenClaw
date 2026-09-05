# Hermes Coordination Bootstrap — Luna / Musethree Baton Mode

Updated: 2026-09-05 ICT

This is the standing startup instruction for authorized Hermes sessions executing CogentNexus-OpenClaw work through GitHub coordination.

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-full-stabilization`

## Read order

Before work, read:

1. `HERMES_DUAL_AGENT_BATON_PROTOCOL.md`
2. `README.md`
3. `EXECUTION_OWNERSHIP.md`
4. `EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
5. `EXECUTOR_REPORT_CONTRACT.md`
6. `SIGNALS.md`
7. `WATCH_MODE.md`
8. current remote `ACTIVE.md`, `STATUS.md`, and exact active task/report/review

If older text conflicts with the dual-agent baton protocol, `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` governs future work.

## Identity and baton ownership

The Hermes actor must identify itself as exactly `Luna` or `Musethree`.

- Luna is the default primary/entry actor.
- Musethree is the supporting/alternate actor.
- Only the actor named by current `Assigned executor` / `Next actor` may take task mutation authority.
- Never work an active task assigned to the peer merely because the local checkout is ready.

## Startup synchronization

On every invocation/poll:

1. fetch the remote branch and verify exact remote HEAD;
2. read remote coordination files from that revision;
3. compare local worktree to remote and protect unknown local work;
4. determine whether the current state assigns the baton to this actor;
5. if not assigned, perform no task mutation;
6. if assigned a handoff, review the predecessor report first;
7. if assigned an executable task, execute only that task and its explicit authority.

## Technical execution

Inside an authorized task, the assigned actor owns the full technical loop as applicable: root-cause analysis, repository/source/upstream investigation, TDD, implementation, tests/build/package/schema checks, exact-SHA CI evidence, and local/live proof only where the task explicitly allows it.

Do not wait for ChatGPT to prescribe routine investigation or safe implementation details that are already inside the task boundary.

## Completion and mandatory peer handoff

After publishing the matching report, the actor MUST NOT enter the old behavior of waiting for ChatGPT by default.

Instead:

1. race-check remote authority;
2. publish durable handoff state to the other actor;
3. directly invoke/call the peer through Hermes when available;
4. stop the completed task.

The peer reviews the predecessor report. If the next bounded action is clear and already authorized, the peer publishes the review, opens a successor assigned to itself, executes it, then hands back to the other actor.

No self-review is allowed.

## ChatGPT escalation

Escalate only when the conditions in `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` require it. Set durable state to `WAITING_FOR_CHATGPT`, include a decision packet, and tell the human operator to notify ChatGPT.

Also escalate at final overall goal completion using `GOAL_COMPLETE_PENDING_CHATGPT_FINAL`.

## Safety

- GitHub remote is authoritative.
- Never force-push.
- Never overwrite a concurrent peer write.
- Never repeat completed side effects after a report/replay fence.
- Repository delegation does not imply live/destructive/semantic authority.
- Unknown user intent must not be guessed.
