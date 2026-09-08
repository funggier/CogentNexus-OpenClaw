# CNX-20260901-207 — Direct Discord NO_REPLY Visible-Final Repair

Status: `DESIGN_READY__AWAITING_IMPLEMENTATION_APPROVAL`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-206`
Repair parent: `CNX-20260831-198`
Executor: ChatGPT / repository TDD
Coordinator / final reviewer: ChatGPT

## Purpose

Repair the proven semantic scope gap where a genuine direct Discord owner request can finish with OpenClaw's bare `NO_REPLY` sentinel because the existing Task-191 visible-final revision guard is Dashboard-only.

This task is deliberately bounded. It does **not** change native delivery confirmation, reply-dispatch correlation, message-sent correlation, provider/model selection, lifecycle, installer, Release/tag/assets, or durable schema.

## Immutable authorities

Published `v0.9.3` target remains immutable:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Current repaired candidate before Task 207:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Accepted OpenClaw baseline:

`2026.7.1-2 (0790d9f)`

Task-205 failing run:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
owner session: agent:main:discord:channel:1531199905673252946
model final: NO_REPLY
native queued payloads: 0
```

## Proven root cause

Task 191 added a `before_agent_finalize` guard that requests one same-run model revision when a genuine direct Dashboard Ticket finishes with exact bare `NO_REPLY` / `no_reply`.

The guard currently requires `dashboardTicket(path, runId)`. The Task-205 Ticket is a direct Discord owner Ticket, so the guard returns without a revision. OpenClaw then interprets bare `NO_REPLY` as silence and the channel turn has no queued reply payload.

## Required invariant

For a genuine direct human Discord owner Ticket:

```text
accepted direct Ticket
+ exact run correlation
+ exact owner-session correlation
+ natural final exactly bare NO_REPLY
=> one bounded same-run finalization revision
```

CogentNexus must not synthesize the answer. The model remains responsible for producing the visible corrected final.

## Bounded design

### Production behavior

Extend only the Task-191 finalization guard so that it recognizes a direct Discord owner Ticket in addition to a Dashboard direct Ticket.

The Discord eligibility proof must require all of:

1. exact `runId` exists;
2. exact `sessionKey` exists;
3. one accepted Ticket matches that exact run;
4. Ticket `owner_session_key` equals the exact hook session key;
5. Ticket is direct: `workflow_eligible=0` and `workflow_id IS NULL`;
6. session key is the canonical Discord channel shape (`agent:<agent>:discord:channel:<id>`);
7. natural final text after trim is exactly bare `NO_REPLY` case-insensitively.

When all conditions hold, return one `before_agent_finalize` revision decision:

```text
action: revise
maxAttempts: 1
idempotencyKey: deterministic per run
instruction: genuine direct Discord user request must produce a visible answer and must not return NO_REPLY/no_reply
```

### Preserve existing Dashboard behavior

Do not alter:

- `stageDashboardDirectResult`;
- Dashboard durable marker/staging;
- Dashboard native settlement;
- Task-191 Dashboard revision semantics except any internal helper refactor needed to share exact direct-Ticket lookup safely.

### Negative fences

The guard must return no decision for:

- non-ticketed runs;
- run/session mismatch;
- subagent sessions;
- non-Discord arbitrary session shapes;
- workflow/durable Tickets;
- empty final text;
- mixed substantive text containing the token, e.g. `Actual answer: NO_REPLY is a sentinel`;
- ordinary visible Discord final text.

## TDD sequence

### RED

Add a focused Task-207 regression test using a real temporary SQLite TicketStore and the real installed finalization hook.

Minimum RED assertions:

1. accepted direct Discord Ticket + exact bare `NO_REPLY` => expect one bounded `revise` decision;
2. current pre-fix source returns `undefined` for this case — this is the required RED;
3. visible/mixed text => no revision;
4. non-ticketed Discord run => no revision;
5. exact run with mismatched session => no revision;
6. existing Task-191 Dashboard tests remain unchanged and green.

Commit the test-only RED separately and verify CI fails only on the new positive Discord regression.

### Minimal repair

Modify only the smallest production surface necessary, expected to be:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

A small helper extraction for exact direct-Ticket lookup is allowed if it reduces duplicated SQL and keeps Dashboard staging semantics unchanged.

Do not touch `index.ts` delivery settlement, `message_sent`, `reply_dispatch`, direct recovery, lifecycle, installer, provider, schema, or release workflow in this task.

### GREEN

Run:

- focused Task-207 regression;
- full plugin tests;
- repository Validate matrix;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke;
- package proof for the exact repaired candidate.

If any unrelated test fails, classify rather than weakening it.

## Live requalification after repository GREEN

Because production plugin bytes change, open a separate bounded Windows task after CI GREEN.

That task may install-over the exact Task-207 candidate and perform exactly one human Discord Send in channel `1531199905673252946` after health and room-ID gates.

Expected live chain:

```text
1 human Send
-> 1 Ticket
-> 1 model call (plus at most one same-run finalization revision if first final is NO_REPLY)
-> visible native Discord reply
-> delivery_confirmed
-> completed
```

If a visible native payload is produced but durable settlement still fails, stop and reopen the separate `reply_dispatch/message_sent` correlation issue with run-bound evidence. Do not combine that second defect into Task 207.

## Hard fence

No Discord Send during repository TDD, no live SQLite lock, no lifecycle mutation, no installer/uninstall/reset/reinstall, no provider/model replacement, no schema change, no Release/tag/asset mutation, no force push.

## Expected disposition

Repository phase:

`READY_FOR_WINDOWS_REQUALIFICATION` or a precise TDD/CI failure.

Final Task-198 closure remains blocked until the successor Windows/Discord requalification passes.
