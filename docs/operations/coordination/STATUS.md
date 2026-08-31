# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK206_DISCORD_NATIVE_DELIVERY_HOOK_FORENSICS`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + read-only Windows/OpenClaw retained-evidence forensics  
**Active task:** `CNX-20260901-206`  
**Parent:** `CNX-20260901-205`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK205_FAIL_DURABLE_CORRELATION__TASK206_FORENSICS_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Frozen repaired candidate remains:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 205 terminal review

Task 205 is accepted as:

`FAIL_DURABLE_CORRELATION`

The correct numeric Discord channel was proven. One human Send created one Ticket and one completed direct Ollama model call. `response_ready` was persisted, but no durable native delivery confirmation or Ticket completion was observed. Runtime health remained green and no recovery/outbox residue occurred.

Exact live correlation:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
call_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5:model:1
owner session: agent:main:discord:channel:1531199905673252946
response_ready: 2026-08-31T19:06:52.333Z
```

## Active Task 206

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-206-task205-discord-native-delivery-hook-forensics.md`

The task is read-only and uses the existing Task-205 evidence window. It must determine whether native Discord delivery failed, succeeded without usable receipt correlation, reply-dispatch settlement failed, message-sent emission/correlation failed, another precise mechanism occurred, or retained evidence is insufficient.

No new Discord traffic is authorized.

## Contract clue under investigation

Accepted OpenClaw `2026.7.1-2 (0790d9f)` states outbound `message_sent.runId` is not yet plumbed through the outbound path and outbound `sessionKey` is optional. `reply_dispatch.runId` is also optional.

CogentNexus currently settles its `message_sent` fallback only after resolving a run from `event.runId` or an exact `event.sessionKey` match. This is a plausible correlation gap, but Task 206 must establish the actual live hook/outbound shape before repository TDD begins.

## Hard fence

No Discord Send/probe/retry, no lifecycle mutation, no process termination, no provider/model/config/SQLite mutation, no source/test/workflow edit, no Release/tag mutation, and no force push.
