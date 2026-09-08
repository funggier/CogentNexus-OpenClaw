# CNX-20260901-206 — Task 205 Discord Native Delivery / Hook Forensics Review

Status: `REVIEWED__ROOT_CAUSE_REFINED`
Date: 2026-09-01 ICT
Reviewed report: `reports/CNX-20260901-206-task205-discord-native-delivery-hook-forensics.md`
Parent: `CNX-20260901-205`
Repair parent: `CNX-20260831-198`

## Accepted evidence

Task 206 was read-only and preserved the Task-205 live state. The following facts are accepted:

- the correct Discord owner session was `agent:main:discord:channel:1531199905673252946`;
- Task 205 created one direct Ticket and one completed Ollama model call;
- the exact model/trajectory result for the Task-205 run was bare `NO_REPLY`;
- `didSendViaMessagingTool=false` and no messaging-tool target existed;
- OpenClaw recorded `visible channel turn dispatched with no queued reply payloads` for the same owner session after model completion;
- no native Discord message ID, outbound success receipt, or failure receipt was retained for the Task-205 result;
- the Ticket reached `response_ready` and later timed out into pending direct redelivery;
- Task 206 sent no additional Discord traffic and performed no mutation.

## Classification refinement

The report's `EVIDENCE_REPLY_DISPATCH_SETTLEMENT_FAILED` label is accepted as a boundary observation but **not** as the proven Task-205 root cause.

The retained `reply_dispatch` diagnostic entry had:

```text
hasEventRunId=false
hasContextRunId=false
hasDispatcher=true
hasAppendBeforeDeliver=false
handler-skip: missing-run-correlation
```

However that observer entry occurred approximately 0.85 seconds before the Task-205 session start and its correlation digest cannot bind it to run `b79dbb65-15eb-4b3e-8ffb-4084125e6cb5`. It therefore must not be used to justify a production correlation change for Task 205.

The run-bound failure chain that **is** proven is:

```text
genuine direct Discord owner request
  -> accepted direct Ticket
  -> one completed Ollama model call
  -> final assistant text exactly NO_REPLY
  -> no queued native reply payload
  -> no native Discord message ID/receipt
  -> Ticket response_ready remained unconfirmed
  -> direct-redelivery timeout
```

## Root cause

Task 191 already established that bare `NO_REPLY` is OpenClaw's silent/suppression sentinel and added a bounded `before_agent_finalize` revision guard for genuine direct **Dashboard** Tickets.

The installed Task-205 candidate still scopes that guard through `dashboardTicket(path, runId)`. A genuine direct Discord owner Ticket therefore does not enter the guard. The small local model may return bare `NO_REPLY`; OpenClaw suppresses that final and produces no queued channel payload.

The violated semantic invariant is:

> A genuine direct human owner request that has been admitted into a direct Ticket must not silently terminate as bare `NO_REPLY` merely because its accepted transport is Discord rather than Dashboard.

## Separate latent correlation question

OpenClaw `2026.7.1-2 (0790d9f)` documents outbound `message_sent.runId` as not yet plumbed and `message_sent.sessionKey` as optional. CogentNexus currently depends on run/session correlation for fallback settlement.

That remains a legitimate integration risk, but Task 205 did not reach a native visible payload, so this task does **not** authorize changing `reply_dispatch` or `message_sent` correlation yet. First restore a visible Discord final. If a subsequent one-send requalification produces a native payload but still fails durable settlement, reopen correlation diagnosis with exact run-bound evidence.

## Accepted next action

Open Task 207 as a bounded TDD repair of the direct Discord `NO_REPLY` visible-final scope gap.

Task 207 must preserve:

- Dashboard Task-191 behavior unchanged;
- Dashboard durable marker/staging remains Dashboard-only;
- no synthetic user answer from CogentNexus;
- exactly one same-run revision maximum;
- exact run + exact owner-session + accepted direct/non-workflow Ticket binding;
- no revision for non-ticketed, subagent, background/internal, mismatched-session, or mixed substantive text;
- no delivery-correlation production change in the same repair.

Final review disposition:

`TASK206_ACCEPTED__DISCORD_NO_REPLY_SCOPE_GAP_PROVEN__OPEN_TASK207_BOUNDED_TDD`
