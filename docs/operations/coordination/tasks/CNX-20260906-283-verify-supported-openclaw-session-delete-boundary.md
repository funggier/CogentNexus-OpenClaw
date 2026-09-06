# CNX-20260906-283 — Verify Supported OpenClaw Session Delete Boundary

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-281`  
Resumes acceptance context: `CNX-20260906-272`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

Define and prove the exact supported OpenClaw session deletion invocation for installed OpenClaw `2026.7.1-2` before any further live Delete experiment.

This task is repository/source/read-only only. It does not authorize a live Delete, semantic send, or any mutation of CNX durable state.

## Required work

Verify the installed-runtime/client authorization, exact `sessions.delete` request shape, fencing, result/error behavior, and transcript semantics. Publish an immutable source-first report with a bounded proposal for any future live Delete task, then stop.

## Prohibited

- No live `sessions.delete` or reset invocation.
- No retry of `cnxclaw.cmd session cancel`.
- No Hermes semantic send.
- No manual SQLite, Ticket, session, transcript, or config mutation.
- No protected old Ticket/session mutation.
- No replay/redelivery/disposition.
- No installer, uninstall, reset, release promotion, or force push.
