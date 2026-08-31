# Active Coordination Task

Status: `IN_PROGRESS`
Execution mode: `TASK198_DISCORD_SESSION_CORRELATION_AND_DURABLE_DELIVERY_INVESTIGATION`
Current disposition: `TASK197_PASS_ACCEPTED__V093_PUBLISHED__TASK198_ACTIVE`
Task ID: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-08-31 ICT
Executor: ChatGPT for repository diagnosis/repair; Hermes only for bounded Windows/Discord reality evidence when required
Coordinator / final reviewer: ChatGPT

## Published v0.9.3 authority

Public tag and Release now exist.

Release target:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Release:

`https://github.com/funggier/CogentNexus-OpenClaw/releases/tag/v0.9.3`

Exactly three public assets were independently verified under Task 197. Publication is complete; do not republish or retarget v0.9.3.

## Active task

[`tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`](tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md)

Task 196 supplied live Discord RED evidence:

- one Discord session was blocked before agent execution with `missing-run-correlation` / `before_agent_run hook failed` / `missing-append-before-deliver`;
- a different Discord room produced one Ticket, one completed model call, terminal delivery/completion events, and a user-visible response;
- the successful room still emitted a `missing-run-correlation` observer skip and had no `cnx_assistant_delivery` row for that Ticket.

Root cause is not yet claimed. The first phase is source/test/data-flow tracing. No production fix is allowed before a focused failing regression test proves the violated invariant.

## Investigation discipline

1. Trace inbound Discord admission and Ticket/run/session attribution.
2. Trace `before_agent_run`, `reply_dispatch`, transcript/message-write and message-sent contracts.
3. Trace all writers of `delivery_confirmed_at`, `delivery_confirmed`, `completed`, and `cnx_assistant_delivery`.
4. Compare Dashboard vs Discord/non-Dashboard direct paths and current tests.
5. State one evidence-backed root-cause hypothesis.
6. Add a focused RED regression test and observe the intended failure.
7. Apply only the minimal production repair after RED.
8. Run focused + full plugin/repository validation.
9. If live proof is required, hand Hermes one bounded human Discord-send protocol only after repository GREEN.

## Lifecycle boundary

The user-directed release-first requirement is now satisfied. Clean uninstall/reset/fresh reinstall testing remains deferred while Task 198 diagnoses the live Discord/session defect so the test host is not destructively changed during evidence tracing.

## Hard fence

No v0.9.3 republish/retarget, no force push, no production mutation before root cause + RED proof, no test weakening, no provider change, no state deletion/reset/uninstall/reinstall merely to obtain a passing Discord run, and no repeated/synthetic Discord sends presented as human evidence.
