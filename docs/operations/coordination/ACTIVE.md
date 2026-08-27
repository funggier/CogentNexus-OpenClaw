# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `READ_ONLY_AUTHENTICATED_DASHBOARD_FRESH_SESSION_READINESS`
Current authorization: `TASK096_POST_REPORT_OWNER_READINESS_PROOF_AUTHORIZED`
Task ID: `CNX-20260827-097`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 096 reviewed

Task 096 report:

`d397396fd5d688d84c16d90e8be622e1f59b1411`

Independent decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_OWNER_SURFACE_READINESS_SNAPSHOT_ONLY`

Review:

[`reviews/CNX-20260827-096-live-install-repaired-staging-and-restore-parity.md`](reviews/CNX-20260827-096-live-install-repaired-staging-and-restore-parity.md)

The live deployment portion is accepted: exact source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1` was installed by one supported invocation, final candidate fingerprint is exact, deployment returned to MANAGED generation 24, health/parity passed and `NO_FLASH_MULTI_TICK_REPROVEN` was recorded.

The Task-096 report blocker reflects only the browser state at the time the task ended.

## Post-report operator observation

After Task 096 had already completed and published its report, the operator manually entered the OpenClaw token and reported that the Dashboard is now accessible.

This is new evidence and must not be retroactively inserted into Task 096.

No executor is authorized to read, print, copy, persist, request or re-enter the token.

## Active Task 097

[`tasks/CNX-20260827-097-prove-post-task-dashboard-owner-fresh-session-readiness.md`](tasks/CNX-20260827-097-prove-post-task-dashboard-owner-fresh-session-readiness.md)

Task 097 is read-only/readiness-only.

It must prove:

- current authenticated Dashboard/WebChat connection is correlated to owner/operator control scope;
- a read-only control RPC succeeds;
- actual New Chat can enter a fresh staged empty state without stale/unknown-parent or fallback behavior;
- no semantic message is sent;
- no new Ticket/outbox/provider activity occurs;
- live MANAGED/source/SQLite/Gateway health remains unchanged.

Required token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

## Hard fence

No semantic send, semantic nonce, direct provider/Ollama call, install/reset/repair, plugin generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, Task-092 rewrite, restart/reboot, merge/tag/release or force push is authorized.

The already authenticated browser state may be inspected and the New Chat control may be entered once without sending content.

## Successor gate

Only independent acceptance of Task 097 PASS may authorize the final one-message authenticated fresh-session semantic acceptance.
