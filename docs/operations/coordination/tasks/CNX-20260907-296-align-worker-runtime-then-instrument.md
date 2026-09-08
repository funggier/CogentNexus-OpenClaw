# CNX-20260907-296 — Align Worker Runtime Then Instrument Actual Invocation

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-295`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

First apply a minimal TDD repair candidate that binds the detached delivery worker to the same Node runtime used by the Gateway server, then instrument the actual detached invocation to determine whether the no-JSON boundary is resolved and capture sanitized evidence if it is not.

## Phase A — TDD repair

1. Re-anchor current remote state and inspect the worker runtime-resolution code.
2. Add RED tests proving the worker selects the configured Gateway/server Node runtime when available and fails closed with a diagnostic when not.
3. Implement the smallest source repair; do not alter delivery semantics, retry policy, Ticket state, or payload handling.
4. Run focused tests and required validation to GREEN.
5. Record exact diff, test commands, and hashes.

The repair must not print credentials or message payloads.

## Phase B — actual detached-worker instrumentation

Using the repaired code and only bounded diagnostics, capture sanitized:

- resolved Python/Node/OpenClaw paths and versions;
- argv shape with keys/payloads/credentials redacted or hashed;
- PID ancestry and process start/exit times;
- stdout/stderr presence, lengths, and hashes;
- Gateway correlation timestamps;
- pending delivery observation without settling it.

Do not use the Chat UI input.

## Strict prohibitions

- Do not retry, replay, redeliver, cancel, dispose, or settle the pending Ticket.
- Do not send any semantic message.
- Do not create/delete/reset sessions.
- Do not mutate SQLite, Ticket, session, transcript, outbox, recovery, or credentials.
- Do not install, restart, or mutate live services.
- Do not release, force push, or modify protected state.

## Completion

Publish one evidence-rich report containing TDD RED/GREEN results, exact repair files, actual detached-worker instrumentation, and whether the repair resolves the no-JSON failure. If the repair is not safe or causality remains unresolved, stop with `NEEDS_CHATGPT`; otherwise propose the next bounded acceptance task.
