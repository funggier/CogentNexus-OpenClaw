# CNX-20260907-293 — Verify Human-Initiated Clean Recreation

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-292`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

Verify the user's newly sent Discord message and determine whether it created the expected fresh OpenClaw session and CNX lifecycle.

## Allowed work

Read-only inspect supported OpenClaw session inventory and CNX durable state. Correlate the new Discord session key/session ID, generation, Ticket, delivery, outbox, recovery, and health. Confirm the old deleted session/tombstone and protected session remain fenced.

## Prohibited

No message sending, session creation, `sessions.delete`, reset, cancel substitute, replay/redelivery, manual SQLite/Ticket/session/transcript mutation, credential action, installer, release, or force push.

## Completion

Publish an evidence report. If the new lifecycle is found, propose the next bounded read-only/delivery acceptance step. If absent or ambiguous, stop with `NEEDS_CHATGPT`.
