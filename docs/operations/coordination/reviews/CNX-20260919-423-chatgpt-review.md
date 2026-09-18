# CNX-20260919-423 — ChatGPT Review

## Decision

`REJECT_READY__DUAL_SESSION_ADAPTER_IDEMPOTENCY_REPAIR_REQUIRED`

Rejected executor classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

CNX-423 correctly repaired the two CNX-422 blockers:

- OpenClaw internal/inter-session/control provenance is now excluded before external-owner trust evaluation;
- source owner session and effective ACP dispatch session are now separated, so legitimate ACP retargeting is no longer treated as a same-role identity conflict.

Those repairs are accepted.

However, independent review found a residual cross-adapter idempotency defect specific to that new dual-session model. The defect can create two Tickets for one OpenClaw run when both `reply_dispatch` and `before_agent_run` fire with different source/effective session keys.

No controlled live upgrade is authorized from implementation HEAD:

`59830e4512b89d8924295c886f121d077b3d6c61`

Reviewed publication HEAD:

`27dabc44e9baa9889fdddc31a9017785d5613bae`

## Accepted CNX-423 evidence

Accepted:

- provenance exclusion direction and implementation;
- ACP source-owner/effective-dispatch distinction;
- same-role non-ACP conflict remains fail closed;
- provider/model/harness values remain untouched;
- CNX-423 RED provenance/ACP matrix and final GREEN result;
- focused baseline regressions;
- package validation;
- OpenClaw v2026.9.4 target build/tests;
- isolated v2026.9.4 startup, plugin load, health and clean shutdown;
- inherited CNX-422 migration/rollback evidence.

The historical CNX-383 RED remains unrelated and is not the reason for this rejection.

## Blocking finding — run-level idempotency still depends on owner session key

The Ticket store computes:

`requestKey = hash(ownerSessionKey + "\0" + runId)`

This was sufficient while both adapters used the same session key.

CNX-423 correctly changed `reply_dispatch` ownership for bound ACP dispatch to the source owner session:

`ctx.SessionKey`

while `before_agent_run` can observe the effective ACP target session:

`ctx.sessionKey`

The two adapters therefore may submit the same host run with:

- same `runId`;
- same prompt;
- different owner/session key.

Because the persistence idempotency key includes session key, that can create two Tickets.

The in-memory `ticketedRuns` set is populated by `reply_dispatch`, but `before_agent_run` does not consult it before calling the shared admission kernel.

## Reviewer RED reproduction

A disposable reviewer-only regression reproduced the exact dual-session sequence:

1. `reply_dispatch`
   - dispatch kind: `acp`
   - source owner session: `agent:main:discord:C123`
   - effective ACP session: `agent:opencode:acp:bound-session`
   - runId: `dual-session-run`

2. `before_agent_run`
   - session key: effective ACP session
   - same runId
   - same prompt

Required invariant:

- one Ticket;
- owner session remains the source owner session;
- one routed event.

Observed:

`tickets = 2`

Vitest result:

- test files: `1 failed`
- tests: `1 failed / 1 total`
- assertion: `expected { n: 2 } to deeply equal { n: 1 }`

The reviewer-only test was deleted after reproduction and the repository worktree returned clean.

## Why this blocks upgrade readiness

CNX-423's own task explicitly required:

`reply_dispatch + before_agent_run remains one Ticket / one route event`

The existing CNX-422 regression proves that only when both adapters use the same session key. It does not cover bound ACP dual-session identity.

The new source/effective identity semantics are correct, but cross-adapter idempotency must now be made run-aware independently of session retargeting.

## Required repair

Authorize CNX-424 as a narrow source-only TDD repair.

Required RED before production change:

- bound ACP `reply_dispatch(source-owner)` followed by `before_agent_run(effective-target)` with the same real runId creates exactly one Ticket;
- owner session on that Ticket remains source owner;
- route event cardinality remains exactly one.

Required preserved behavior:

- same-session CNX-422 idempotency remains GREEN;
- `before_agent_run` still performs admission when no earlier `reply_dispatch` Ticket exists;
- direct and durable semantics remain unchanged;
- internal/inter-session provenance exclusions remain unchanged;
- external trust failure remains fail closed;
- provider/model/harness remain untouched.

Preferred minimal repair:

- treat the already-admitted real `runId` as the cross-adapter in-process idempotency fence;
- if `before_agent_run` receives a runId already admitted by `reply_dispatch`, pass without invoking a second Ticket acceptance;
- do not weaken persistent TicketStore idempotency or globally change its request-key schema unless evidence requires it.

## Requalification

After repair:

- CNX-424 RED -> GREEN;
- CNX-423 and CNX-422 suites GREEN;
- focused regressions GREEN;
- package validation GREEN;
- broad suite characterized;
- exact OpenClaw v2026.9.4 target build/tests GREEN;
- isolated v2026.9.4 startup/register/shutdown GREEN.

Copied-state migration does not need rerun unless storage/schema/startup migration changes.

## Safety decision

Until CNX-424 passes review:

- live OpenClaw upgrade: prohibited;
- live state/session migration: prohibited;
- semantic provider acceptance send: prohibited;
- live provider/model mutation: prohibited;
- live plugin lifecycle mutation for upgrade: prohibited;
- release/tag/main: prohibited;
- force push/history rewrite: prohibited.

## Reviewer

ChatGPT

Human final authority: Operator
