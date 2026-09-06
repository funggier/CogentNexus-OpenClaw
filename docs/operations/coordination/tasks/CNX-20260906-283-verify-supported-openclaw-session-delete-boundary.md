# CNX-20260906-283 — Verify Supported OpenClaw Session Delete Boundary

## Status

`READY_FOR_CHATGPT_REVIEW`

Parent: `CNX-20260906-281`  
Resumes acceptance context: `CNX-20260906-272`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

Define and prove the exact supported OpenClaw session deletion invocation for installed OpenClaw `2026.7.1-2` before any further live Delete experiment.

This task is repository/source/read-only only. It does not authorize a live Delete, semantic send, or any mutation of CNX durable state.

## Evidence already established

Upstream source commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` contains:

- Gateway method `sessions.delete`;
- params schema: required non-empty `key`, optional `agentId`, `deleteTranscript`, `expectedSessionId`, `expectedLifecycleRevision`, `expectedSessionUpdatedAt`, `emitLifecycleHooks`, and `archivedOnly`;
- Gateway handler rejection for WebChat clients and the main session;
- active-work admission drain before mutation;
- pre-lock and under-lock identity/fencing checks;
- lifecycle storage deletion and transcript archival/deletion behavior;
- session-end hook and sessions-changed event after successful deletion;
- operator archive-then-delete restriction through `archivedOnly`.

The prior `cnxclaw.cmd session cancel` attempt returned `cancelled=[]` and must not be retried as a Delete substitute.

## Required read-only work

1. Verify that the exact installed runtime exposes `sessions.delete` through its Gateway protocol and identify the authenticated client/scope required.
2. Verify the exact installed Control UI or supported client request shape, including whether `deleteTranscript` and `archivedOnly` are required.
3. Verify how the runtime reports success, no-op, identity mismatch, active-work refusal, permission rejection, and WebChat rejection.
4. Verify transcript semantics: whether deletion removes the canonical session record and whether the transcript is archived/removed under this exact release.
5. Define the minimum safe fencing tuple for a future live test:
   - exact canonical session key;
   - exact pre-delete OpenClaw session ID;
   - exact CNX lifecycle generation/revision and updatedAt where available;
   - disposable target only;
   - protected Ticket/session exclusion.
6. Publish a source-first evidence report and stop for human/ChatGPT authorization.

## Prohibited

- No live `sessions.delete` or reset invocation.
- No retry of `cnxclaw.cmd session cancel`.
- No Hermes semantic send.
- No manual SQLite, Ticket, session, transcript, or config mutation.
- No protected old Ticket/session mutation.
- No replay/redelivery/disposition.
- No installer, uninstall, reset, release promotion, or force push.

## Completion

Publish a report under `docs/operations/coordination/reports/` with exact source paths/lines or equivalent immutable evidence, the supported invocation contract, and a bounded proposed successor live task. Then set coordination to `WAITING_FOR_CHATGPT_REVIEW`.
