# CNX-20260901-209 — Task-205 Recovery Executability Adjudication Review

Date: 2026-09-01 ICT  
Reviewed task: `CNX-20260901-209`  
Parent: `CNX-20260901-208`  
Coordinator / reviewer: ChatGPT

## Review disposition

`ACCEPT_BLOCKED_EXECUTABLE_RECOVERY__SUPPORTED_CANCELLATION_REQUIRED`

Task 209 correctly proves that the historical Task-205 direct-redelivery recovery is executable under current production authority and correctly stops without mutation.

## Evidence accepted

Exact historical identity:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
owner session: agent:main:discord:channel:1531199905673252946
```

Fresh read-only state at `2026-09-01T08:57:10.821Z` proves:

```text
Ticket status: accepted
workflow_eligible: 0
workflow_id: null
session state/generation: active / 0
recovery mode/state: redeliver / pending
recovery owner_generation: 0
attempt_count: 0
active_run_id: null
next_attempt_at: 2026-08-31T19:08:52.400Z
active/recovering model calls: 0
SQLite integrity: ok
```

Every `dueDirectRecovery()` predicate is true and the exact Ticket-constrained production-equivalent scheduler query returns the historical Ticket. The old recovery is therefore not merely cosmetic residue.

## Same-session scope safety

Task 209 also proves the owner session has exactly:

```text
nonterminal Tickets: 1
pending/running/awaiting-delivery recoveries: 1
pending assistant deliveries: 0
pending outbox rows: 0
active/recovering model calls: 0
```

The only nonterminal Ticket/recovery pair is the Task-205 pair. There is no unrelated same-session emittable work in the captured durable tables.

This is sufficient to authorize a separately scoped supported session-boundary cancellation, provided the successor revalidates the same inventory immediately before mutation.

## Supported cancellation authority

The currently installed pre-Task-207 product lineage already exports `cancelSessionTickets(path,{runId,...})` from `v090`.

That function first resolves the owner session from the exact supplied `runId`, then delegates to the normal session-boundary cancellation path. The session-boundary path:

- increments the session generation;
- keeps a user-cancelled session active;
- cancels nonterminal Tickets in that exact owner session;
- suppresses pending outbox/assistant delivery owned by that session;
- marks non-cancelled direct-recovery rows for that session `cancelled`;
- preserves unrelated sessions.

The successor must invoke this supported function once using the exact historical run ID. It must not issue raw SQLite updates.

## Required successor invariants

Before cancellation, revalidate that the exact session still contains only the historical Task-205 nonterminal Ticket/recovery pair and no pending assistant delivery/outbox or active/recovering model call.

After cancellation, require:

```text
owner session remains active
session generation increments exactly once (expected 0 -> 1 if unchanged at pre-gate)
historical Ticket status = cancelled
historical recovery state = cancelled
historical Ticket is no longer selected by dueDirectRecovery-equivalent query
no same-session emittable residue
SQLite integrity = ok
```

If the pre-mutation inventory has changed, stop without cancellation.

## Task-207 authority

Repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

After successful supported cancellation and residue verification, the successor may continue directly into the previously deferred exact-candidate Windows install-over and one-send Discord requalification. No need to create an intermediate cosmetic cleanup task if all gates remain satisfied.

## Review result

Task 209 is accepted as an evidence-complete blocker. The next task should perform one exact-run supported cancellation, verify the generation/recovery boundary, then requalify Task-207 on Windows/Discord under a fresh one-send budget.
