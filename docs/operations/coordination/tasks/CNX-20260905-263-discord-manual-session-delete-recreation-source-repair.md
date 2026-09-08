# CNX-20260905-263 — Discord Manual Session Delete/Recreation Source Repair

Status: `READY_FOR_LUNA`
Executor: `Luna`
Reviewer / next baton: `Musethree`
Parent: `CNX-20260905-262`
Umbrella: `CNX-20260831-188`
Authority source: explicit user request on 2026-09-05 to repair the manual web-session deletion edge case after final stabilization acceptance.

## Problem statement

OpenClaw's `sessions.delete` lifecycle now has explicit, test-covered semantics:

- it emits `session_end`;
- `event.reason === "deleted"`;
- `event.sessionId` is the deleted lifecycle identity;
- `event.sessionKey` is the canonical owner key (including Discord keys);
- no replacement `nextSessionId` is supplied;
- a later session creation emits `session_start` with `sessionId` and `sessionKey`.

CogentNexus already consumes `session_end(reason="deleted")` in `v090.ts` and
correctly performs the destructive half of the lifecycle boundary:

- increments owner generation;
- marks the owner deleting/deleted;
- cancels nonterminal Tickets;
- suppresses/removes pending Ticket outbox and assistant delivery;
- cancels direct recovery;
- suppresses workflow completion;
- cancels bound/synthetic CogentNexus work.

The defect is the recreation half. Current `session_start` only reads
`sessionAuthority()` and warns when the owner row is tombstoned. Because
`ensureSession()` uses `INSERT OR IGNORE`, a deleted row remains deleted and a
new Discord lifecycle at the same canonical session key can never become a
fresh active CogentNexus owner.

This is a real lifecycle gap, not a reason to weaken deletion semantics.

## Desired semantic contract

Manual web Delete is an explicit abandonment boundary for the old lifecycle.
Nothing from the deleted generation is implicitly carried into the recreated
session.

After OpenClaw later creates a genuinely new lifecycle instance at the same
canonical Discord session key, CogentNexus must establish a new active owner
generation so a new user message can be admitted normally.

Conceptually:

```text
OpenClaw session K / sessionId A
  CNX generation G active
        |
        | sessions.delete
        v
  old Ticket/outbox/recovery cancelled/suppressed
  CNX tombstone generation G+1
        |
        | later Discord message creates sessionId B on same key K
        v
  CNX reactivation generation G+2 active
        |
        +-- fresh Tickets only

stale A callbacks/recovery/delivery -> rejected forever
```

The exact generation arithmetic may be implemented differently if the same
invariants are proven, but a new lifecycle must never share authority with the
deleted lifecycle.

## Required design properties

### Lifecycle identity

Do not reactivate merely because a `session_start` event mentions the same
`sessionKey`. Bind reactivation to OpenClaw lifecycle identity (`sessionId`) or
an equivalent exact lifecycle token.

The durable owner record must retain enough identity to distinguish:

- duplicate start of the currently active lifecycle;
- stale start from the deleted lifecycle;
- genuinely new lifecycle on the same canonical key.

If schema extension is required, it must be migration-safe for existing
SQLite databases and bootstrap/validation paths.

### Deletion remains destructive for old work

Do not change the existing meaning of `session_end(reason="deleted")` into a
normal successor rebind. Specifically, automatic deletion handling must not:

- rebind old Tickets to the recreated session;
- restore old outbox rows;
- restore suppressed assistant delivery;
- reactivate cancelled direct recovery;
- revive workflow completion delivery;
- repeat external side effects.

### Reactivation

A genuine new OpenClaw lifecycle on the same key must transition the owner to
`active` under a fresh generation exactly once. Repeated `session_start` for
the same lifecycle must be idempotent and must not increment generation each
time.

A stale or duplicated `session_start` for the deleted `sessionId` must leave
the tombstone in force.

### Admission after recreation

After valid reactivation, a normal trusted owner turn from that Discord session
must be able to create a fresh direct/durable Ticket under the new generation.
No old durable work is inherited implicitly.

### Fences

All existing generation/state checks for direct recovery, assistant delivery,
workflow completion and synthetic workers must continue to reject the old
generation after reactivation.

## TDD requirements

Production changes require strict RED -> minimal repair -> GREEN.

At minimum, add focused executable tests covering:

1. `session_end(reason="deleted", sessionId=A, sessionKey=K)` tombstones K and
   preserves current cancellation/suppression behavior.
2. `session_start(sessionId=B, sessionKey=K)` with B != A reactivates K as a
   fresh generation.
3. repeating `session_start(B,K)` is idempotent: no additional generation
   change and no duplicate durable effects.
4. stale `session_start(A,K)` after deletion cannot reactivate K.
5. old-generation direct recovery and pending assistant delivery remain
   non-emittable after B is active.
6. a fresh owner request on B/K is admitted successfully after reactivation.
7. unrelated session key isolation.
8. existing same-key `new`, `reset`, delete, session-succession, direct-recovery,
   delivery and database-bootstrap tests remain green.

RED evidence must show failure because recreation is currently refused, not
because of fixture/setup errors.

## Likely implementation surface

Primary source candidates:

- `plugins/cogentnexus-openclaw/src/v090.ts`
- focused lifecycle/session-ownership tests (prefer existing test files where
  the behavior naturally belongs)
- bootstrap/migration validation only if a durable lifecycle-id column is
  introduced.

Avoid unrelated refactoring.

## Verification

Run the narrow RED/GREEN tests first, then the relevant plugin suite and repo
validation required by the current branch contract. Exact commands/results go
in the report.

CI for the resulting exact source/report SHA must be observed to terminal state.
If Actions are only queued/in-progress, the current baton holder must enqueue a
persistent +5 minute delayed recheck and continue polling until terminal or a
real stalled-CI diagnosis is required.

## Task263 hard fences

```text
live OpenClaw sessions.delete/reset = 0
live Discord/Dashboard semantic message = 0
live Ticket/session/SQLite mutation = 0
installer/install-over/uninstall/reset = 0
Gateway stop/start/restart = 0
release/tag/default-branch promotion = 0
force push/history rewrite = 0
```

Do not use the user's actual Discord session to prove source behavior in this
task.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-263-discord-manual-session-delete-recreation-source-repair.md`

Include:

- fresh opening/final HEAD and ancestry;
- exact OpenClaw lifecycle evidence used;
- root cause;
- RED test and expected failure;
- minimal production repair and schema migration if any;
- GREEN commands/results;
- exact files/commits;
- exact-SHA CI status;
- hard-fence ledger;
- PASS/FAIL/BLOCKED disposition;
- remaining live-acceptance requirements.

## Completion / baton

Luna publishes the Task263 report and hands the baton to Musethree.
Musethree independently reviews source semantics, migration/idempotency,
RED/GREEN evidence and exact-SHA CI.

If accepted, the next work should be a separate bounded live acceptance task
for the real web-Delete -> next Discord message lifecycle. Do not perform that
live destructive/semantic test inside Task263. If authority for the live test
is insufficient, transition to `WAITING_FOR_CHATGPT` rather than guessing user
intent.
