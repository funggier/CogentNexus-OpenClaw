# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK205_CORRECT_ROOM_DISCORD_REQUALIFICATION`
Current disposition: `TASK204_ROOM_MISMATCH_ACCEPTED__MANAGED_HEALTHY__CORRECT_ROOM_RETEST_AUTHORIZED`
Task ID: `CNX-20260901-205`
Parent task: `CNX-20260901-204`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Frozen repaired product candidate

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 204 accepted result

Task-204 report disposition:

`FAIL_DISCORD_SEMANTIC_DELIVERY`

Review:

[`reviews/CNX-20260901-204-task203-stale-reset-lifecycle-adjudication-cleanup-and-discord-closure-review.md`](reviews/CNX-20260901-204-task203-stale-reset-lifecycle-adjudication-cleanup-and-discord-closure-review.md)

Accepted facts:

- stale historical reset residue was identity-fenced and removed;
- exact installed repaired fingerprint and ownership remained valid;
- one `cnxclaw.cmd enable` exited `0`;
- Host is managed;
- startup adapter is enabled/Ready;
- plugin is enabled/loaded;
- Gateway and Ollama are healthy;
- delivery/recovery are READY with outbox 0;
- SQLite integrity is ok;
- no lifecycle residue remains;
- the Task-204 human Send was made in the wrong Discord room;
- its nonce had no Ticket/model/delivery/recovery/outbox durable match;
- Task-204 correctly did not send a second message.

The Task-204 Discord result is an acceptance-surface mismatch, not proof of failure in the intended room.

## Active Task 205

Hermes must execute:

[`tasks/CNX-20260901-205-task204-correct-room-discord-requalification.md`](tasks/CNX-20260901-205-task204-correct-room-discord-requalification.md)

Correct owner session:

`agent:main:discord:channel:1531199905673252946`

Correct numeric channel ID:

`1531199905673252946`

Execution order:

1. fresh read-only managed-health gate;
2. prove the operator's active Discord acceptance surface has exact numeric channel ID `1531199905673252946`;
3. do not rely only on room name/window title;
4. only after exact room identity is proven, generate one fresh `CNX205-*` nonce;
5. instruct the user to send the exact message manually once;
6. correlate one Ticket -> one direct model call -> response_ready -> one native visible Discord reply -> delivery_confirmed -> completed;
7. verify final managed health.

## New Discord budget

The user explicitly requested another attempt after correcting the wrong-room mistake.

Task-205 human Send budget:

`0 / 1 consumed; 1 / 1 available`

This is a new task budget, not a retry inside Task 204.

If exact numeric room identity cannot be proven, stop without sending.

## Hard fence

No installer/install-over/reset/uninstall/reinstall, no enable/disable/start/stop/restart, no process kill, no provider/model/config/SQLite manual mutation, no Discord probe Send, no bot/API/injected Send, no second human Send, no product/source/test/workflow edit, no Release/tag mutation, and no force push.
