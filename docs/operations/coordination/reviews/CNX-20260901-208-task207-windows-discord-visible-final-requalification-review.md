# CNX-20260901-208 — Task 207 Windows Discord Visible-Final Requalification Review

Date: 2026-09-01 ICT  
Task: `CNX-20260901-208`  
Parent: `CNX-20260901-207`  
Reviewer: ChatGPT

## Review disposition

`ACCEPTED_SAFETY_STOP__RECOVERY_EXECUTABILITY_UNRESOLVED`

Task 208 correctly stopped before install-over and before any Discord Send after finding the historical Task-205 recovery row still stored as `pending`. The stop preserved the one-send acceptance funnel and made no product/runtime mutation.

The report's stronger statement that the row "remains capable of delayed output" is not yet independently proven. The narrower evidence-backed statement is: Task 208 did not prove the row incapable of delayed output, so stopping was correct under the safety contract.

## Independently confirmed Task-208 facts

Report commit:

`db7257afad6dc057efdf523ad10dc96f3795ccf6`

Historical identity:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
nonce: CNX205-20260831T190442Z-8cdbed
owner session: agent:main:discord:channel:1531199905673252946
```

Fresh Task-208 observation:

```text
recovery.mode: redeliver
recovery.state: pending
recovery.attempt_count: 0
recovery.active_run_id: null
recovery.next_attempt_at: 2026-08-31T19:08:52.400Z
recovery.owner_generation: 0
matching deliveries: 0
matching outbox rows: 0
SQLite integrity: ok
human Discord Send: 0
install-over: 0
```

Task-207 candidate `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b` was not installed by Task 208.

## Source-level executability contract

The current accepted direct-recovery scheduler does not select every row whose state is merely `pending`.

`plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts::dueDirectRecovery()` selects a recovery only when all relevant predicates hold, including:

- `r.state='pending'`;
- Ticket `status='accepted'`;
- `workflow_eligible=0`;
- `workflow_id IS NULL`;
- owner session `state='active'`;
- owner session `generation=r.owner_generation`;
- recovery is due by `next_attempt_at`;
- no model-call recovery fence blocks the Ticket.

`plugins/cogentnexus-openclaw/src/v094-direct-recovery.ts::claim()` independently rechecks the same Ticket/session generation authority before changing the recovery to `running`.

Therefore a stale `pending` row with a superseded owner-session generation is inert even though its stored recovery state remains `pending`.

## Evidence gap in Task 208

Task 208 recorded Host generation `32`, but Host lifecycle generation is not the same datum as `cnx_sessions.generation` for the Discord owner session.

The report did not retain the exact current row:

```text
SELECT state,generation
FROM cnx_sessions
WHERE session_key='agent:main:discord:channel:1531199905673252946';
```

It also did not evaluate the complete `dueDirectRecovery()` eligibility predicate for the historical Task-205 Ticket.

Consequently the row is correctly treated as unsafe for Task 208, but its actual runtime executability remains unresolved.

## Required successor

Open a read-only Task 209 to adjudicate exact recovery executability without altering the database or triggering recovery.

Task 209 must distinguish:

- `INERT_SUPERSEDED`: the historical row cannot satisfy the production scheduler/claim authority predicates;
- `EXECUTABLE_RECOVERY`: the row currently satisfies them and may launch/redeliver;
- `INDETERMINATE`: evidence is insufficient.

If inert, no SQLite cleanup is required merely to make the row cosmetically terminal; the successor may authorize a fresh Task-208-style acceptance after proving no other residue can emit output.

If executable, stop without install or Discord Send. A later explicitly authorized identity-fenced cancellation task may use supported session-boundary semantics only after proving it will not cancel unrelated live work. Do not manually update SQLite.

## Preserved authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-208 human Discord budget remains unconsumed:

`0 / 1 consumed`
