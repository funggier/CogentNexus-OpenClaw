# Canonical Session Deletion Ownership Contract

**Date:** 2026-09-10  
**Repository:** `funggier/CogentNexus-OpenClaw`  
**Branch:** `agent/v0.9.5-architecture-repair`  
**Scope:** Session lifecycle deletion/recreation semantics for CogentNexus-OpenClaw  

## 1. Problem

A Discord conversation can retain the same canonical `sessionKey` after the user deletes its Session and later sends a new message. The canonical Session identity is therefore not the session key alone. A deleted lifecycle must not be revived implicitly, and operational state owned by that lifecycle must not remain actionable after deletion.

The current source already records `session_id` and supports lifecycle-aware reactivation. The architecture now needs one explicit contract that defines the ownership boundary across all CNX state so future repairs do not implement Session deletion independently in Discord, Ticket, inference, delivery, or recovery code.

## 2. Canonical semantic model

A Session lifecycle is identified by:

- `sessionKey`: stable routing identity, such as a Discord channel;
- `sessionId`: OpenClaw lifecycle identity;
- `generation`: CNX monotonic ownership fence.

The tuple `(sessionKey, sessionId, generation)` represents one actionable lifecycle context.

A new lifecycle may reuse the same `sessionKey`, but it must receive a new `sessionId` and a new generation whenever the previous lifecycle was deleted.

The system must never infer lifecycle identity from recency, latest run, latest Ticket, or latest database row.

## 3. Delete semantics

Deleting a Session means **invalidate and clean its operational ownership**, not physically erase all historical evidence.

When lifecycle `S1` is deleted:

1. CNX advances the generation exactly once.
2. The Session row becomes a durable tombstone (`state=deleted`) and records the deleted lifecycle identity when known.
3. Actionable Tickets owned by the deleted lifecycle are cancelled/terminalized.
4. Pending Ticket outbox delivery owned by the lifecycle is suppressed and removed from the actionable queue.
5. Pending CNX assistant delivery owned by the lifecycle is cancelled/suppressed.
6. Direct recovery owned by the lifecycle is cancelled and cannot wake again.
7. Active or pending work must fail closed against the old lifecycle generation.
8. Existing event/audit history is retained.
9. No ownership is transferred to another Session or generation.

Physical deletion of audit/event history is out of scope for Session deletion.

## 4. Recreation semantics

After `S1` is deleted, a later Discord message on the same `sessionKey` is a **new lifecycle**, not a resurrection of `S1`.

For new lifecycle `S2`:

- `sessionKey` may equal `S1.sessionKey`;
- `sessionId` must differ from `S1.sessionId`;
- generation must advance by exactly one from the tombstone generation;
- the Session becomes `active`;
- new Tickets may be admitted under `S2`.

The first owner turn must not be rejected solely because OpenClaw's asynchronous `session_start` callback has not yet persisted `S2`, provided the owner lifecycle evidence is sufficient to establish that `S2` is genuinely new and is not the deleted `S1`.

Repeated `session_start` for `S2` is idempotent. A stale `session_start` for `S1` must remain rejected.

## 5. Cross-subsystem ownership contract

### Session

Session is the lifecycle authority. `state + sessionId + generation` determine whether an owner context is current.

### Ticket

Every actionable Ticket has one owner session key and is valid only while its owner lifecycle remains current. Session deletion cancels actionable Tickets owned by that lifecycle. A new lifecycle creates new Tickets; it never reuses old Ticket ownership.

### Inference

Every inference attempt is bound to the exact run/call identity and the owner lifecycle generation. A deleted/superseded generation cannot remain an actionable inference owner. Terminal evidence from an old lifecycle must not be attached to a new lifecycle.

### Delivery

Delivery records are bound to exact Ticket/inference/run/session/generation identity. Session deletion prevents old delivery from being prepared, staged, accepted, or confirmed as new work. Historical delivery evidence remains queryable.

### Recovery

Recovery records are lifecycle-owned. Session deletion cancels recovery and clears its wakeable run state. A future lifecycle may create a new recovery record; the deleted lifecycle must never be woken again.

## 6. Allowed state transition

```text
active(S1,gN)
      |
      | delete
      v
 deleted(S1,gN+1)
      |
      | Discord message with new lifecycle S2
      | S2.sessionId != S1.sessionId
      v
 active(S2,gN+1)
```

The generation increment belongs to the lifecycle boundary. Recreation consumes the tombstone generation; it must not increment a second time merely because the new lifecycle is registered.

## 7. Fail-closed rules

The following are invalid recovery/ownership shortcuts:

- selecting the latest Session row;
- selecting the latest Ticket/run as proof of current ownership;
- matching only `sessionKey` without lifecycle identity when a deleted lifecycle exists;
- allowing `state=active` alone to prove lifecycle freshness;
- confirming delivery after Session generation has rotated;
- waking recovery work without exact owner generation;
- transferring old Tickets or delivery records into the new lifecycle.

When exact lifecycle identity cannot be established, the operation must reject or suppress the action rather than guess.

## 8. Database/history boundary

`cnx_sessions` remains the durable lifecycle registry. Tombstones are intentionally retained because they provide the fence needed to reject stale callbacks and old work.

Operational cleanup may remove pending/actionable rows from queues such as `ticket_outbox` and pending `cnx_assistant_delivery`, but event history in `ticket_events` is retained.

Where a subsystem uses a terminal state instead of physical queue removal, that terminal state must remain non-actionable and must preserve the original owner identity.

## 9. Required tests

The implementation must add or strengthen tests covering at least:

1. Delete cancels actionable Tickets for exactly one lifecycle.
2. Delete suppresses pending outbox/assistant delivery and cancels recovery.
3. Delete leaves audit history intact.
4. Stale `S1` callbacks cannot reopen a deleted lifecycle.
5. A new Discord lifecycle `S2` on the same `sessionKey` becomes active.
6. `S2` generation advances exactly once.
7. Repeated `S2` start is idempotent.
8. Old `S1` Tickets cannot be attached to `S2`.
9. Old `S1` inference evidence cannot settle `S2` work.
10. Old `S1` delivery cannot be confirmed under `S2` generation.
11. Old `S1` recovery cannot wake after deletion.
12. First `S2` owner turn remains admissible when the asynchronous `session_start` registration races behind `before_agent_run`, using exact lifecycle evidence.
13. Cross-session isolation remains intact.

## 10. Compatibility and migration

The nullable `cnx_sessions.session_id` migration remains migration-safe for existing databases. Legacy active rows with `session_id=NULL` may be bound once to an observed current lifecycle without generation churn. Once a lifecycle identity is known, subsequent ownership decisions must use the exact identity rather than the legacy null state.

No provider-selection behavior, Gateway ownership, or release metadata is changed by this contract.

## 11. Non-goals

- No physical deletion of audit history.
- No automatic recreation without an actual new OpenClaw lifecycle event/context.
- No provider/model authority changes.
- No release/tag/merge promotion as part of this contract.
- No heuristic repair based on latest-run or latest-session ordering.

## 12. Success criterion

The user-visible semantic is deterministic:

> Delete Session -> old lifecycle is fully non-actionable inside CNX while history remains auditable -> send a new Discord message in the same room -> CNX opens a new lifecycle with a new lifecycle identity and the correct generation -> new work is independent of deleted work.

The implementation is complete only when focused lifecycle tests, broader plugin tests, and exact-head CI demonstrate these invariants.
