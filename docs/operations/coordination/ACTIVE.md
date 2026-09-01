# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK209_TASK205_RECOVERY_EXECUTABILITY_ADJUDICATION`
Current disposition: `TASK208_SAFETY_STOP_ACCEPTED__RECOVERY_EXECUTABILITY_UNRESOLVED`
Task ID: `CNX-20260901-209`
Parent task: `CNX-20260901-208`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Current repaired product candidate

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

It was NOT installed by Task 208 and must NOT be installed by Task 209.

## Task 208 reviewed result

Report:

`reports/CNX-20260901-208-task207-windows-discord-visible-final-requalification.md`

Review:

`reviews/CNX-20260901-208-task207-windows-discord-visible-final-requalification-review.md`

Accepted review disposition:

`ACCEPTED_SAFETY_STOP__RECOVERY_EXECUTABILITY_UNRESOLVED`

Task 208 correctly stopped before install-over and before any Discord Send after finding the historical Task-205 recovery row still stored as `pending`.

Fresh Task-208 facts:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
recovery mode/state: redeliver / pending
attempt_count: 0
active_run_id: null
next_attempt_at: 2026-08-31T19:08:52.400Z
owner_generation: 0
install-over: 0
human Discord Send: 0
SQLite integrity: ok
```

Independent source review found that `pending` alone does not establish executability. Production `dueDirectRecovery()` and `claim()` also require accepted direct Ticket authority, active owner session, exact owner-session generation match, due time, and a clear active/recovering model-call fence.

Task 208 did not retain the exact `cnx_sessions.state/generation` row for the Discord owner session, so actual executability remains unresolved.

## Active Task 209

Hermes must execute:

`tasks/CNX-20260901-209-task205-recovery-executability-adjudication.md`

Task 209 is READ-ONLY.

Required decision:

1. capture exact joined Task-205 Ticket/session/recovery authority;
2. capture exact `cnx_sessions.state/generation` for `agent:main:discord:channel:1531199905673252946`;
3. evaluate every production `dueDirectRecovery()` predicate at a fresh UTC timestamp;
4. execute a read-only, exact-Ticket-constrained query equivalent to production scheduler selection;
5. inventory same-session nonterminal Tickets, recoveries, assistant deliveries, outbox rows, and active/recovering model calls;
6. classify the old recovery as inert/superseded, executable, other-emittable-residue, or indeterminate;
7. publish the Task-209 report and stop.

No install, session cancel/reset, recovery trigger, SQLite mutation, Gateway restart, or Discord Send is authorized.

## Discord budget

Task 209 authorizes:

`0 Discord sends`

Task-208 one-send acceptance budget remains unconsumed but cannot be used until a later successor explicitly reopens live acceptance.

## Hard fence

No install-over, no installer, no reset/uninstall/reinstall, no Gateway restart, no provider/model/config/schema change, no session stop/reset/delete, no Ticket cancel, no recovery launch/update, no manual SQLite mutation, no Discord traffic, no source/test/workflow mutation, no Release/tag mutation, and no force push.
