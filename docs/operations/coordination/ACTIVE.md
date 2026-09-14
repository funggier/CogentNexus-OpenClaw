# Active Coordination Task

Status: `READY_FOR_OPERATOR`
State: `V096_OPENAI_GPT56_LUNA_TICKET_ROUTING`
Execution mode: `HUMAN_ASSISTED_ONE_BOUNDED_LIVE_REQUEST`
Task ID: `CNX-344`
Parent: `CNX-343`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Active branch: `agent/v0.9.6-openai-gpt56-luna-ticket-routing`

## Objective

Verify whether a Dashboard session manually created and manually configured by the human operator to use OpenAI `gpt-5.6 Luna` traverses the real CogentNexus durable Ticket lifecycle.

This is a routing/lifecycle acceptance test, not a timeout test.

## Human operator setup

1. Open the authenticated OpenClaw Control Dashboard.
2. Click `New session` exactly once.
3. Select the OpenAI model shown as `gpt-5.6 Luna` (or the exact configured UI label corresponding to that OpenAI model).
4. Tell Hermes the fresh session is created and the requested model is selected.

Hermes must not perform the New Session click or model-selection UI action.

## Hard fences

- Exactly one human `New session` click.
- Exactly one human selection of the requested OpenAI GPT-5.6 Luna model.
- Exactly one semantic request.
- No second session.
- No second request.
- No retry, resend, recovery, fallback, or manual dispatch.
- No provider/model/config/timeout/controller/database mutation.
- No production code/test changes.
- No install/reinstall/rebuild/restart.
- No `v0.9.5` mutation.
- No force-push/history rewrite.
- If session/model identity cannot be verified before the request, stop `BLOCKED` and do not send it.

## Preflight

After the operator reports setup complete, Hermes must read-only verify:

- Firefox PID/window
- current Dashboard URL
- fresh session identity
- session is new rather than the prior CNX-343 session
- visible selected provider/model is OpenAI / GPT-5.6 Luna
- relevant runtime configuration without mutation
- durable baseline counts for tickets, events, inference, and delivery/outbox

## Semantic request

Send exactly:

`CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`

The request must be sent through the Dashboard UI in the human-created fresh session.

## Required evidence

Correlate the single request across the real runtime:

- Dashboard session
- provider/model
- Ticket/admission identity
- Run identity
- Call/inference identity where available
- durable event sequence
- Result
- Delivery
- final Ticket status
- outbox final state
- duplicate-owner check

The evidence must establish that the OpenAI request entered the CogentNexus Ticket path rather than reaching the provider outside the durable Ticket lifecycle.

## PASS

PASS only if the fresh human-created session and GPT-5.6 Luna selection are independently verified, exactly one request is sent, a correlated Ticket is accepted, the real OpenAI model call belongs to the same Ticket/Run lifecycle, Result and Delivery are durable and correlated, final Ticket state is successful, outbox is `0`, and no duplicate owner/call exists.

## FAIL

If the OpenAI request reaches the provider and produces a result but lacks a corresponding CogentNexus durable Ticket lifecycle:

`FAIL — OPENAI_REQUEST_BYPASSED_TICKET_LIFECYCLE`

Use another evidence-backed classification when a different concrete failure is established.

## BLOCKED

`BLOCKED — SESSION_OR_MODEL_IDENTITY_UNVERIFIED`

Use when the fresh session or GPT-5.6 Luna selection cannot be safely verified before sending.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260914-344-openai-dashboard-ticket-routing-report.md`

Include exact session/provider/model/Ticket/Run/Call/inference/Result/Delivery identifiers, event sequence, outbox final count, duplicate-owner evidence, and any limitation distinguishing UI model selection from internal provider/model identity.

Stop for independent ChatGPT review. Do not self-accept CNX-344.
