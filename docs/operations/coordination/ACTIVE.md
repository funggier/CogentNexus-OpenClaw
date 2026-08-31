# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK206_DISCORD_NATIVE_DELIVERY_HOOK_FORENSICS`
Current disposition: `TASK205_FAIL_DURABLE_CORRELATION_ACCEPTED__READ_ONLY_FORENSICS_REQUIRED`
Task ID: `CNX-20260901-206`
Parent task: `CNX-20260901-205`
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

## Task 205 accepted result

Task-205 report disposition:

`FAIL_DURABLE_CORRELATION`

Review:

[`reviews/CNX-20260901-205-task204-correct-room-discord-requalification-review.md`](reviews/CNX-20260901-205-task204-correct-room-discord-requalification-review.md)

Accepted facts:

- exact numeric Discord channel `1531199905673252946` was proven before Send;
- fresh managed runtime health passed;
- exactly one human Send was consumed;
- one Ticket was accepted for owner session `agent:main:discord:channel:1531199905673252946`;
- exactly one direct Ollama model call completed;
- `response_ready` was persisted;
- no recovery or outbox residue occurred;
- Ticket remained `accepted` with `delivery_confirmed_at = null`;
- no matching native delivery settlement was proven;
- no retry, second message, second room, lifecycle mutation, or manual state repair occurred.

Exact Task-205 run:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
call_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5:model:1
response_ready: 2026-08-31T19:06:52.333Z
channel: 1531199905673252946
```

## Active Task 206

Hermes must execute:

[`tasks/CNX-20260901-206-task205-discord-native-delivery-hook-forensics.md`](tasks/CNX-20260901-206-task205-discord-native-delivery-hook-forensics.md)

Task 206 is read-only. It must inspect retained evidence from the existing Task-205 window and distinguish:

1. native Discord send failed/absent;
2. native send succeeded but receipt correlation was missing;
3. reply-dispatch settlement failed;
4. message-sent hook emission/correlation failed;
5. another precise delivery-path mechanism; or
6. insufficient retained evidence.

OpenClaw baseline contract relevant to this investigation:

- outbound `message_sent.runId` is optional and not plumbed through the accepted baseline outbound path;
- outbound `message_sent.sessionKey` is optional;
- `reply_dispatch.runId` is optional;
- CogentNexus `message_sent` fallback currently needs a run ID or exact session-key match to settle a direct Ticket.

Do not implement a fix until Task 206 identifies the live event shape or reports evidence insufficiency.

## Discord budget

Task 206 authorizes no Discord traffic:

`0 sends authorized`

## Hard fence

No Discord Send/probe, no retry/regenerate, no lifecycle command, no process kill, no provider/model/config/SQLite mutation, no product/source/test/workflow edit, no Release/tag mutation, and no force push.
