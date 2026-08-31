# CNX-20260831-198 — Discord Session Correlation and Durable Delivery Investigation

Status: `QUEUED_AFTER_TASK197_PUBLICATION`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Evidence source: `CNX-20260831-196`
Executor: ChatGPT for repository diagnosis/repair; Hermes for bounded Windows/Discord reality evidence when required

## Purpose

Diagnose and repair the Discord session/correlation durability inconsistency observed during Task 196 without conflating it with release-publication mechanics.

## Live RED evidence from Task 196

### Session A — blocked before agent execution

`agent:main:discord:channel:1531201432861282405`

Observed log pattern:

- `handler-skip: missing-run-correlation`
- `before_agent_run hook failed; blocking request`
- `handler-skip: missing-append-before-deliver`

No accepted durable Ticket/model-call/delivery chain was proven for the blocked requests.

### Session B — user-visible success with incomplete durable delivery evidence

`agent:main:discord:channel:1531199905673252946`

Observed durable identifiers:

- Ticket: `CNXT-50d93e89-a04b-421d-bad2-b2c747f646da`
- Run: `65f3abad-9817-4c7a-aeb7-1feeafda5213`
- Model call: `65f3abad-9817-4c7a-aeb7-1feeafda5213:model:1`
- Provider/model: `ollama / qwen3.5:9b`

Observed lifecycle:

`accepted -> routed -> direct_model_call_started -> direct_model_call_ended -> response_ready -> delivery_confirmed -> completed`

The user confirmed the response was visible in Discord. SQLite integrity was `ok`, with zero recovery attempts and zero Ticket outbox rows.

Anomaly:

- no `cnx_assistant_delivery` row existed for the completed Ticket;
- a `missing-run-correlation` observer skip still appeared around the request.

## Questions that must be answered before source mutation

1. Which OpenClaw hook/event supplies Discord run/session correlation at each phase (`before_agent_run`, `reply_dispatch`, transcript/message write, message_sent), and which fields are optional across room/session lifecycles?
2. Why can one Discord session fail closed before the agent while another reaches completed using an apparently incomplete observer correlation path?
3. Which component set `delivery_confirmed_at` / terminal delivery events for Session B when `cnx_assistant_delivery` had no row?
4. Is `cnx_assistant_delivery` intended only for Dashboard direct-result ownership, or is Discord expected to have a separate durable delivery record/table/contract? Do not assume table absence is itself a bug until the channel contract is read from source/tests/docs.
5. Does `reply_dispatch` lack runId for Discord by design, requiring correlation via session/ticket authority rather than treating missing runId as a blocking defect?
6. Could stale per-session state, session migration, plugin reload, or session generation explain Session A vs Session B?
7. Is the `before_agent_run` fail-closed decision coupled incorrectly to delivery-observer capabilities that are not guaranteed on Discord transport?

## Investigation sequence

1. Fresh-fetch current repository state and accepted OpenClaw baseline.
2. Trace Discord admission from inbound message to Ticket creation and `before_agent_run`.
3. Trace run/session correlation maps and their lifecycle/cleanup.
4. Trace reply dispatch and native Discord delivery confirmation path.
5. Trace all writers of `delivery_confirmed_at`, `delivery_confirmed`, `completed`, and `cnx_assistant_delivery`.
6. Compare existing tests for Dashboard vs Discord/non-Dashboard direct sessions.
7. Determine the minimum violated invariant from Task-196 evidence.
8. Add a focused regression test that reproduces the violated invariant (RED).
9. Apply the minimal production fix only after RED is proven.
10. Run focused tests, full plugin tests, Validate and proportional Windows/Discord requalification if production source changes.

## Safety / scope fence

Before root cause and RED proof:

- no production/runtime/plugin source mutation;
- no test weakening;
- no provider change;
- no state deletion/reset/uninstall/reinstall merely to obtain a passing Discord run;
- no synthetic user message presented as human Discord evidence;
- no repeated Discord sends without a bounded test protocol;
- no force push.

If a live repeat becomes necessary, Hermes must define exact pre-state, one human Send, expected durable deltas, and stop after the single attempt for evidence review.

## Acceptance target

The final repaired contract must make Discord session behavior deterministic enough that a genuine user message cannot be blocked merely because an observer-specific run correlation is absent when the transport contract does not guarantee that field, while preserving exactly-once Ticket/model/delivery semantics and fail-closed behavior where attribution truly cannot be proven.

Any delivery-confirmation mechanism must have a documented durable evidence path appropriate to Discord; do not blindly require the Dashboard-only `direct_result` mechanism if source architecture defines a different channel contract.

## Final dispositions

- `PASS`
- `FAIL_DISCORD_SESSION_CORRELATION`
- `FAIL_DISCORD_DURABLE_DELIVERY`
- `BLOCKED_OPENCLAW_HOOK_CONTRACT`
- `REQUALIFICATION_SCOPE_EXPANSION_REQUIRED`

## Report

When executed, publish:

`docs/operations/coordination/reports/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`
