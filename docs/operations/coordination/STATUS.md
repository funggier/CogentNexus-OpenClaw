# Coordination Channel Status

**State:** `READY_FOR_LUNA`
**Execution mode:** `TASK263_DISCORD_MANUAL_SESSION_DELETE_RECREATION_SOURCE_REPAIR`
**Updated:** 2026-09-05 ICT — user-authorized post-acceptance lifecycle repair opened by ChatGPT
**Transport:** GitHub repository / Actions authoritative
**Active task:** `CNX-20260905-263`
**Parent:** `CNX-20260905-262`
**Parent umbrella:** `CNX-20260831-188`
**Disposition:** `USER_AUTHORIZED_POST_ACCEPTANCE_SESSION_LIFECYCLE_REPAIR`

**Assigned executor:** `Luna`
**Handoff from:** `ChatGPT`
**Next actor after report:** `Musethree`
**Protocol:** `docs/operations/coordination/HERMES_DUAL_AGENT_BATON_PROTOCOL.md`
**Delayed recheck:** `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## Fresh root cause

OpenClaw's session-delete lifecycle emits `session_end` with
`reason="deleted"`, the deleted `sessionId`, canonical `sessionKey`, and no
replacement. CogentNexus already handles that event by cancelling/suppressing
old-generation durable work and tombstoning `cnx_sessions`.

The remaining defect is recreation: a later Discord message may cause OpenClaw
to create a new lifecycle instance at the same canonical key. The current
CogentNexus `session_start` hook calls `sessionAuthority()` and only warns when
the row is `deleted`; it does not establish a fresh active generation. The new
session can therefore remain fenced by the old tombstone.

## Task263 acceptance target

TDD repair must prove all of the following:

1. delete keeps old-generation cancellation/suppression semantics;
2. a new OpenClaw `sessionId` on the same key reactivates exactly one fresh
   CogentNexus generation;
3. repeated start for the same new lifecycle is idempotent;
4. stale start for the deleted lifecycle cannot reactivate it;
5. old recovery/outbox/assistant delivery remains fenced and is not rebound;
6. new owner requests can be admitted under the fresh generation;
7. existing reset/new/session-succession contracts stay green.

Task file:

`docs/operations/coordination/tasks/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

## Hard fences

Task263 is source/test/docs only. No live session deletion/reset, semantic send,
SQLite mutation, installer, Gateway lifecycle, release/tag/default-branch
mutation, force push, or history rewrite is authorized.

Luna reports then hands off to Musethree. Musethree reviews and continues under
the dual-agent baton protocol. Any Actions-only wait must use the persistent
five-minute delayed recheck queue.
