# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK200_TASK198_REPAIRED_DISCORD_WINDOWS_REQUALIFICATION`
Current disposition: `TASK198_REPOSITORY_REPAIR_ACCEPTED__WAITING_ONE_LIVE_DISCORD_REQUALIFICATION`
Task ID: `CNX-20260831-200`
Parent task: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-08-31 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published v0.9.3 authority

Publication is already complete and must remain untouched.

Public tag `v0.9.3` target:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Do not republish, retarget, recreate, or modify the v0.9.3 Release/assets.

## Task 198 repository repair

Task 198 repository diagnosis/repair is accepted RED -> GREEN.

Report:

[`reports/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`](reports/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md)

Review:

[`reviews/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation-review.md`](reviews/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation-review.md)

Frozen repaired product candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Do not substitute later coordination HEADs for this product identity.

Exact candidate gates:

- Validate `33413832703`: `completed/success`
- Windows Installer Pack Smoke `33413832709`: `completed/success`
- PS5.1 Acceptance Smoke `33413832777`: `completed/success`
- package payload-v2: `db5fbd96630ac3685c0588e3d5009dce68e0052bc03f8dab5fdb29577410b27d`
- package file count: `190`

## Active Hermes task

[`tasks/CNX-20260831-200-task198-repaired-discord-windows-requalification.md`](tasks/CNX-20260831-200-task198-repaired-discord-windows-requalification.md)

Task 200 must:

1. capture read-only pre-state;
2. perform exactly one supported install-over from exact product candidate `9f4eaa...`;
3. prove installed repair identity and post-install health;
4. use known healthy Discord session `agent:main:discord:channel:1531199905673252946`;
5. generate a fresh nonce and tell the user the exact Discord prompt;
6. wait for user `ส่งแล้ว`;
7. after that single human Send, prove one Ticket -> one model call -> response_ready -> one native visible Discord reply -> delivery_confirmed -> completed;
8. prove no retry/recovery/duplicate/outbox residue and no `before_agent_run hook failed` for the tested send;
9. publish the Task 200 report and stop for ChatGPT review.

## Discord acceptance semantics

- Human Discord Send budget: exactly `1 / 1`.
- No Hermes/bot/API/injected human message.
- No retry, regenerate, or second room/message.
- `cnx_assistant_delivery` is **not required** for a native Discord Direct reply; Ticket-level native delivery confirmation is accepted.
- `missing-run-correlation` or `missing-append-before-deliver` from the Dashboard observer is not a failure by itself if the actual Discord lifecycle is correct.
- `before_agent_run hook failed` for the tested send is a failure.

## Hard fence

No force push, no release/tag mutation, no reset/uninstall/fresh reinstall, no state deletion, no artificial production SQLite lock, no provider/model substitution, no product/source/test/workflow edit, and no second human Discord Send under Task 200.
