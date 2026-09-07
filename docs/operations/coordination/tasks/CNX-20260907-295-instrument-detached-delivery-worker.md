# CNX-20260907-295 — Instrument Detached Delivery Worker Boundary

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-294`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

Capture evidence explaining why detached delivery-worker `chat.history` calls return exit 0 with empty stdout/stderr while identical direct and concurrent foreground calls return valid JSON.

## Allowed work

Read current state and perform bounded diagnostics only. Capture sanitized:

- resolved Python/Node/OpenClaw executable paths and versions inside the detached worker;
- sanitized argv shape, with session keys/payloads/credentials redacted or hashed;
- child PID/process-tree ownership and start/exit timestamps;
- raw stdout/stderr availability and byte lengths at the worker boundary;
- Gateway/CLI correlation timestamps;
- supervisor/worker environment differences relevant to process lifetime and stream capture.

Repository-only diagnostic instrumentation is allowed when needed, but use TDD for any production code change and do not alter delivery semantics.

## Required constraints

- Do not retry, replay, redeliver, cancel, disposition, or settle the pending Ticket.
- Do not send messages or create/delete/reset sessions.
- Do not read, print, copy, or change credentials or sensitive payloads.
- Do not mutate SQLite, Ticket, session, transcript, outbox, recovery, installer, release, or protected state.
- Preserve evidence with exact remote HEAD and hashes.

## Completion

Publish an evidence-rich report. If a deterministic source defect is proven, propose a separate minimal TDD repair task; otherwise publish the strongest detached-worker root-cause classification and exact missing decision. Stop at the report boundary.
