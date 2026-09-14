# CNX-344 — OpenAI GPT-5.6 Luna Dashboard Ticket Routing Acceptance

- Parent: `CNX-343`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Execution mode: `HUMAN_ASSISTED_ONE_BOUNDED_LIVE_REQUEST`

## Objective

Verify whether a Dashboard session that the human operator creates manually and configures manually to use OpenAI `gpt-5.6 Luna` actually traverses the CogentNexus durable Ticket lifecycle in the live runtime.

This is a routing/lifecycle acceptance test, not a timeout test. The test must use the provider/model selected by the human operator in the Dashboard and must correlate the visible request with the durable Ticket/Run/Result/Delivery lifecycle.

## Human operator setup

The operator must manually:

1. Open the authenticated OpenClaw Control Dashboard.
2. Click `New session` exactly once.
3. Select the OpenAI model shown as `gpt-5.6 Luna` (or the exact UI label corresponding to that configured OpenAI model).
4. Tell Hermes that the fresh session has been created and the model selected.

Hermes must not perform the New Session click or model-selection UI action.

## Hard fences

- Exactly one human `New session` click.
- Exactly one human model selection for the requested OpenAI GPT-5.6 Luna model.
- Exactly one semantic request.
- No second session.
- No second request.
- No retry, resend, recovery, fallback, or manual dispatch.
- No provider/model/config/timeout/controller/database mutation.
- No production code/test changes.
- No install/reinstall/rebuild/restart unless a separate successor task explicitly authorizes it.
- No `v0.9.5` mutation.
- No force-push/history rewrite.
- If session/model identity cannot be verified before the semantic request, stop `BLOCKED` and do not send the request.

## Preflight evidence

After the human reports setup complete, Hermes must read-only verify:

- exact Firefox PID/window
- current Dashboard URL
- fresh session identity
- the session is newly created rather than the prior CNX-343 session
- visible selected provider/model is OpenAI / GPT-5.6 Luna
- relevant runtime configuration without mutation
- durable baseline counts for tickets, ticket events, result/delivery state and inference attempts

If any required identity is ambiguous, stop `BLOCKED`.

## Semantic request

Send exactly:

`CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`

The request must be sent through the Dashboard UI in the fresh human-created session.

## Required durable evidence

Correlate the single request across the real runtime:

- fresh Dashboard session
- provider/model
- Ticket/admission identity
- Run identity
- Call/inference identity where available
- durable lifecycle events
- Result
- Delivery
- final Ticket status
- outbox final state
- duplicate-owner check

The evidence must establish that the request was admitted through the CogentNexus Ticket path rather than merely reaching an OpenAI/model transport outside the durable Ticket lifecycle.

## PASS criteria

PASS only if:

1. Human-created fresh session is independently verified.
2. Dashboard visibly has OpenAI GPT-5.6 Luna selected before sending.
3. Exactly one semantic request is sent.
4. A correlated durable Ticket is created and accepted.
5. The live OpenAI model call is linked to the same Ticket/Run lifecycle.
6. A durable Result and Delivery are linked to that same lifecycle.
7. Final Ticket status is `completed` (or the task's canonical successful terminal state).
8. Final outbox is `0`.
9. No duplicate owner/call is observed.
10. No retry/fallback/manual dispatch or protected-state mutation occurred.

## FAIL classification

`FAIL — OPENAI_REQUEST_BYPASSED_TICKET_LIFECYCLE`

Use this only when the request reaches the OpenAI model and produces a response but no corresponding CogentNexus durable Ticket lifecycle exists.

Other evidence-backed failures should use a more specific classification.

## BLOCKED classification

`BLOCKED — SESSION_OR_MODEL_IDENTITY_UNVERIFIED`

Use this when the fresh session or GPT-5.6 Luna selection cannot be verified safely before the request.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260914-344-openai-dashboard-ticket-routing-report.md`

Include exact session/provider/model/Ticket/Run/Call/inference/Result/Delivery identifiers, event sequence, outbox final count, duplicate-owner evidence, and any limitation distinguishing UI selection from internal provider/model identity.

Stop for independent ChatGPT review. Do not self-accept CNX-344.
