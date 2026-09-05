# Luna / Musethree Continuous Coordination Watch Mode

Updated: 2026-09-05 ICT

## Purpose

Allow the two Hermes agents to consume durable baton handoffs and asynchronous wait states without requiring the human operator to relay every task or wake an agent after CI finishes.

This mode never bypasses task-specific safety gates.

Read `DELAYED_RECHECK_QUEUE.md` for the canonical five-minute asynchronous wait contract.

## Poll cycle

Each agent polls/synchronizes independently but executes only when the current remote coordination state names that agent as `Assigned executor`, `Next actor`, or wait owner.

On every run:

1. fetch `origin/agent/v0.9.3-full-stabilization`;
2. read `HERMES_DUAL_AGENT_BATON_PROTOCOL.md`, `DELAYED_RECHECK_QUEUE.md`, `CODEX_BOOTSTRAP.md`, `ACTIVE.md`, `STATUS.md`, and the referenced task/report/review;
3. identify local actor as `Luna` or `Musethree`;
4. if baton/wait ownership belongs to the peer, exit without mutation;
5. if state is `HANDOFF_TO_<this actor>` or the actor is named `Next actor`, review predecessor evidence first;
6. if review supports a clear authorized successor, publish review, open the bounded successor assigned to this actor, and execute it;
7. if state is `READY_FOR_<this actor>`, execute the exact active task;
8. if state is `WAITING_FOR_CI_RECHECK` / `CI_STALLED_DIAGNOSIS` and this actor owns the wait, query only the exact asynchronous dependency after fresh authority synchronization;
9. when task/review work actually completes, publish the matching report/review;
10. hand off to the peer and invoke/call the peer through Hermes when available;
11. stop the completed task.

## Five-minute CI self-wake

When the assigned actor reaches required GitHub Actions that are still `queued`, `pending`, or `in_progress`:

1. retain the baton;
2. create/dedupe one persistent delayed wake for approximately +5 minutes;
3. end the current compute turn instead of busy-waiting;
4. on wake, fetch remote state first;
5. if the queued wait is stale because task/HEAD/baton changed, discard it;
6. otherwise inspect exact required runs/checks;
7. if still non-terminal, create one new +5 minute wake;
8. if success, resume the same task/review;
9. if failure/cancel/time-out/action-required, stop passive waiting and inspect the failure.

A five-minute wake must not rerun the operation that created the workflow, repeat external side effects, or manufacture a new commit merely to prove the watcher is alive.

If the Hermes delayed queue is unavailable, an already-enabled watcher should poll the wait owner at approximately five-minute cadence. If neither persistent mechanism exists, record `WAIT_RECHECK_WAKE_UNAVAILABLE`; do not falsely claim autonomous continuation.

## Stalled CI

After about 12 unchanged five-minute observations, perform one bounded `CI_STALLED_DIAGNOSIS` pass while continuing the recheck loop if the workflow remains legitimately active. A slow workflow alone is not a reason to ask the human to wake the bot.

See `DELAYED_RECHECK_QUEUE.md` for retry and escalation rules.

## Escalation/no-op states

Do not execute project work when state is:

- `WAITING_FOR_CHATGPT`;
- `GOAL_COMPLETE_PENDING_CHATGPT_FINAL`;
- an explicit operator pause/stop state;
- assigned to the peer.

`WAITING_FOR_CI_RECHECK` is not a no-op state for its wait owner; it is a scheduled recheck state.

No-op polls create no commits.

## Automatic authority

Automatic pickup/self-wake means the actor may consume an already-authorized baton/task or re-check an already-authorized asynchronous condition. It does not grant new live/destructive/semantic authority. Successor creation is permitted only under the deterministic peer-successor rules in the baton protocol.

## Race handling

Fetch before every coordination write and every delayed-wake continuation. If the peer advanced the branch, stop using stale assumptions, re-read current baton ownership, discard stale wake entries, and never force-push.
