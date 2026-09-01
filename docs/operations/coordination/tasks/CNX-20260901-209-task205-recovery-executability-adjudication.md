# CNX-20260901-209 — Task-205 Recovery Executability Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-208`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Resolve the single blocker discovered by Task 208 without changing runtime state.

The historical Task-205 row is stored as `pending`, but production recovery authority is additionally fenced by Ticket state, owner-session state/generation, due time, and active/recovering model-call state. Task 209 must determine whether that exact historical row is actually executable now.

This task is read-only. It does not install Task-207, send Discord traffic, cancel anything, or clean SQLite.

## Immutable authority

Public `v0.9.3` remains immutable:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Do not install it in Task 209.

Historical Task-205 identity:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
nonce: CNX205-20260831T190442Z-8cdbed
owner session: agent:main:discord:channel:1531199905673252946
recovery owner_generation observed by Task 208: 0
```

## Source authority to mirror exactly

Production scheduler predicate:

`plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts::dueDirectRecovery()`

A pending row is schedulable only when all relevant conditions hold:

```text
r.state = pending
t.status = accepted
t.workflow_eligible = 0
t.workflow_id IS NULL
s.state = active
s.generation = r.owner_generation
r.next_attempt_at IS NULL OR r.next_attempt_at <= now
no cnx_direct_model_call for the same ticket in state active/recovering
```

Production launch claim additionally rechecks Ticket/session generation authority in:

`plugins/cogentnexus-openclaw/src/v094-direct-recovery.ts::claim()`

Do not invoke the mutating `claim()` function. Reproduce its predicates read-only.

## Phase A — fresh read-only baseline

Create a fresh evidence directory under:

`%LOCALAPPDATA%\Temp\cnx209-*`

Capture:

- exact UTC timestamp;
- database path and file metadata;
- SQLite `PRAGMA integrity_check`;
- OpenClaw version;
- current managed host status;
- current delivery/recovery read-only checks;
- no lifecycle process residue relevant to install/recovery execution.

No mutation may occur.

## Phase B — exact joined historical authority row

Using SQLite read-only mode, capture the exact joined state for the Task-205 Ticket:

```sql
SELECT
  t.ticket_id,
  t.status AS ticket_status,
  t.workflow_eligible,
  t.workflow_id,
  t.owner_session_key,
  t.run_id AS ticket_run_id,
  s.state AS session_state,
  s.generation AS session_generation,
  r.mode AS recovery_mode,
  r.state AS recovery_state,
  r.attempt_count,
  r.active_run_id,
  r.next_attempt_at,
  r.owner_generation,
  r.last_error,
  r.created_at,
  r.updated_at
FROM tickets t
LEFT JOIN cnx_sessions s ON s.session_key=t.owner_session_key
LEFT JOIN cnx_direct_recovery r ON r.ticket_id=t.ticket_id
WHERE t.ticket_id='CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6';
```

Also capture all `cnx_direct_model_call` rows for this Ticket, including their `state`, provider/model, run/model-call identity, and timestamps.

## Phase C — exact production scheduler eligibility

Evaluate the production `dueDirectRecovery()` predicate for the exact historical Ticket without changing state.

At the fresh captured UTC timestamp, record booleans for each condition:

```text
recovery_pending
ticket_accepted
direct_ticket
no_workflow
session_active
session_generation_matches_owner_generation
due_by_time
model_call_recovery_fence_clear
```

Then run a read-only query equivalent to production selection, additionally constrained to the exact Ticket ID, for example:

```sql
SELECT r.ticket_id
FROM cnx_direct_recovery r
JOIN tickets t ON t.ticket_id=r.ticket_id
JOIN cnx_sessions s ON s.session_key=t.owner_session_key
WHERE r.ticket_id='CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6'
  AND r.state='pending'
  AND t.status='accepted'
  AND t.workflow_eligible=0
  AND t.workflow_id IS NULL
  AND s.state='active'
  AND s.generation=r.owner_generation
  AND (r.next_attempt_at IS NULL OR r.next_attempt_at<=?)
  AND NOT EXISTS (
    SELECT 1 FROM cnx_direct_model_call m
    WHERE m.ticket_id=r.ticket_id
      AND m.state IN ('active','recovering')
  );
```

Bind `?` to the exact captured current UTC ISO timestamp.

Do not infer from `recovery.state` alone.

## Phase D — same-session residue inventory

Read-only inventory the exact owner session:

`agent:main:discord:channel:1531199905673252946`

Capture:

- all nonterminal Tickets (`accepted`, `planned`, `running`, `waiting`);
- pending/running/awaiting-delivery direct-recovery rows;
- pending assistant-delivery rows;
- pending ticket outbox rows;
- active/recovering model calls;
- session state/generation.

This inventory is required to determine whether a later supported session-boundary cancellation could be safely scoped if cancellation becomes necessary. Task 209 itself must not cancel anything.

## Decision rules

### `PASS_INERT_SUPERSEDED_RECOVERY`

Use only if the exact Task-205 row cannot satisfy production scheduler/claim authority, for example because:

- session generation differs from `owner_generation`; or
- session is not active; or
- Ticket is no longer accepted/direct/non-workflow; or
- another permanent authority fence makes selection impossible.

The exact constrained production-equivalent scheduler query must return no row.

If this disposition is reached, explicitly state whether any other same-session residue can emit output. Do not clean the stale row merely for cosmetic consistency.

### `BLOCKED_EXECUTABLE_TASK205_RECOVERY`

Use if all scheduler predicates are true and the constrained production-equivalent query selects the historical Ticket.

Stop immediately. Do not install, send, cancel, advance session generation, trigger recovery, or restart Gateway.

The report should recommend a separate identity-fenced cancellation task. That later task may use supported session-boundary semantics only after proving no unrelated same-session work would be cancelled.

### `BLOCKED_OTHER_EMITTABLE_RESIDUE`

Use if the historical Task-205 recovery itself is inert but another pending/running recovery, pending assistant delivery, pending outbox row, or equivalent same-session residue can still emit output.

### `BLOCKED_INDETERMINATE_RECOVERY_AUTHORITY`

Use if any required table/row/field cannot be read or eligibility cannot be decided exactly.

## Explicit non-actions

Task 209 authorizes none of the following:

- install-over;
- installer execution;
- reset/uninstall/fresh reinstall;
- Gateway restart;
- provider/model/config change;
- session stop/reset/delete;
- Ticket cancel;
- direct-recovery launch;
- direct-recovery state update;
- manual SQLite mutation;
- Discord Send/probe/API/bot/injection;
- source/test/workflow mutation;
- Release/tag/asset mutation;
- force push.

## Discord budget

Task 209:

`0 Discord sends authorized`

The unconsumed Task-208 acceptance budget is not transferable into this read-only task.

## Evidence/report

Publish:

`docs/operations/coordination/reports/CNX-20260901-209-task205-recovery-executability-adjudication.md`

The report must include:

- exact joined Task-205 authority row;
- exact `cnx_sessions.state/generation`;
- exact recovery `owner_generation`;
- per-predicate scheduler truth table;
- result of the constrained production-equivalent scheduler query;
- same-session residue inventory;
- SQLite integrity;
- mutation ledger proving zero writes/actions;
- one allowed disposition above.

Stop after publishing the report for ChatGPT review.
