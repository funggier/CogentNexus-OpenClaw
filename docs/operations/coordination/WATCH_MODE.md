# Hermes Continuous Coordination Watch Mode

Updated: 2026-09-05 ICT

## Purpose

Allow the single Hermes executor to consume durable assigned tasks and asynchronous wait states without requiring the human operator to relay every CI completion.

This mode never bypasses task-specific safety gates and does not perform ChatGPT review work.

Read `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md` and `DELAYED_RECHECK_QUEUE.md` first.

## Poll cycle

On every run:

1. fetch `origin/agent/v0.9.3-full-stabilization`;
2. read `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`, `DELAYED_RECHECK_QUEUE.md`, `CODEX_BOOTSTRAP.md`, `ACTIVE.md`, `STATUS.md`, and referenced task/report/review;
3. confirm current state assigns execution or wait ownership to `Hermes`;
4. if state is `WAITING_FOR_CHATGPT_REVIEW`, `WAITING_FOR_USER_AUTHORITY`, final-acceptance waiting, or explicit pause/stop, exit without task mutation;
5. if state is `READY_FOR_HERMES`, execute the exact assigned task;
6. if state is `WAITING_FOR_CI_RECHECK` / `CI_STALLED_DIAGNOSIS` and Hermes owns the wait, query only the exact dependency after fresh authority synchronization;
7. when task work actually completes, publish the matching report and set a ChatGPT-review handoff state;
8. stop mutation of the completed task.

## Five-minute CI self-wake

When required GitHub Actions remain `queued`, `pending`, or `in_progress`:

1. Hermes retains task ownership;
2. create/dedupe one persistent delayed wake for approximately +5 minutes;
3. end the current compute turn instead of busy-waiting;
4. on wake, fetch remote state first;
5. if the wait is stale because Task/HEAD/ownership changed, discard it;
6. otherwise inspect exact required runs/checks;
7. if still non-terminal, create one new +5 minute wake;
8. if success, resume the same task;
9. if failure/cancel/time-out/action-required, stop passive waiting and inspect the failure.

A five-minute wake must not rerun the operation that created the workflow, repeat external side effects, or manufacture heartbeat commits.

If the Hermes delayed queue is unavailable, an already-enabled watcher may poll at approximately five-minute cadence. If neither persistent mechanism exists, record `WAIT_RECHECK_WAKE_UNAVAILABLE`; do not falsely claim autonomous continuation.

## Stalled CI

After about 12 unchanged five-minute observations, perform one bounded `CI_STALLED_DIAGNOSIS` pass while continuing the recheck loop if the workflow remains legitimately active. Slow CI alone is not a reason to ask the human to wake Hermes.

## No-op / review states

Hermes performs no project task mutation when state is:

- `WAITING_FOR_CHATGPT_REVIEW`;
- `WAITING_FOR_CHATGPT`;
- `WAITING_FOR_USER_AUTHORITY`;
- `GOAL_COMPLETE_PENDING_CHATGPT_FINAL`;
- an explicit operator pause/stop state;
- assigned to another authority for review/decision.

`WAITING_FOR_CI_RECHECK` is not a no-op state for Hermes when Hermes owns the active task wait.

No-op polls create no commits.

## Automatic authority

Automatic pickup/self-wake only consumes an already-authorized Hermes task or re-checks an already-authorized asynchronous condition. It does not grant successor, review, live/destructive, or semantic authority.

Successor framing after a completed report belongs to ChatGPT under the standing single-agent protocol.

## Race handling

Fetch before every coordination write and every delayed-wake continuation. If remote advanced, stop using stale assumptions, re-read current ownership, discard stale wake entries, and never force-push.
