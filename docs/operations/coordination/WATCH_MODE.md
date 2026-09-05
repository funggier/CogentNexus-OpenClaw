# Luna / Musethree Continuous Coordination Watch Mode

Updated: 2026-09-05 ICT

## Purpose

Allow the two Hermes agents to consume durable baton handoffs without requiring the human operator to relay every task.

This mode never bypasses task-specific safety gates.

## Poll cycle

Each agent polls/synchronizes independently but executes only when the current remote coordination state names that agent as `Assigned executor` or `Next actor`.

On every run:

1. fetch `origin/agent/v0.9.3-full-stabilization`;
2. read `HERMES_DUAL_AGENT_BATON_PROTOCOL.md`, `CODEX_BOOTSTRAP.md`, `ACTIVE.md`, `STATUS.md`, and the referenced task/report/review;
3. identify local actor as `Luna` or `Musethree`;
4. if baton is assigned to the peer, exit without mutation;
5. if state is `HANDOFF_TO_<this actor>`, review predecessor evidence first;
6. if review supports a clear authorized successor, publish review, open the bounded successor assigned to this actor, and execute it;
7. if state is `READY_FOR_<this actor>`, execute the exact active task;
8. publish the matching report;
9. hand off to the peer and invoke/call the peer through Hermes when available;
10. stop the completed task.

## Escalation/no-op states

Do not execute project work when state is:

- `WAITING_FOR_CHATGPT`;
- `GOAL_COMPLETE_PENDING_CHATGPT_FINAL`;
- an explicit operator pause/stop state;
- assigned to the peer.

No-op polls create no commits.

## Automatic authority

Automatic pickup means the actor may consume an already-authorized baton/task. It does not grant new live/destructive/semantic authority. Successor creation is permitted only under the deterministic peer-successor rules in the baton protocol.

## Race handling

Fetch before every coordination write. If the peer advanced the branch, stop using stale assumptions, re-read current baton ownership, and never force-push.
