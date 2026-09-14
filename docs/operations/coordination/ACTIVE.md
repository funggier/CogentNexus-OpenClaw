# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_LIVE_TIMEOUT_REQUALIFICATION_POST_INSTALL`
Execution mode: `ONE_BOUNDED_LIVE_SEMANTIC_REQUEST`
Task ID: `CNX-343`
Parent: `CNX-342`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Fresh session: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`
Active branch: `agent/v0.9.6-installation-provenance-requalification`

## Objective

Execute exactly one bounded live semantic request against the already-established CNX-340E fresh Dashboard session after CNX-342 verified the complete repaired artifact installation and one Gateway restart. Prove from real durable runtime evidence that the live Gateway now persists `timeoutMs=2700000` for the direct-model-call lease.

## Hard fences

- Exact CNX-340E fresh session only.
- Exactly one semantic request.
- No new session / no `New session` click.
- No reinstall, rebuild, or Gateway restart.
- No provider/model/config/timeout/controller/database mutation.
- No retry, resend, recovery, fallback, or manual dispatch.
- No OpenAI.
- Do not wait 2700 seconds; inspect durable lease evidence directly.
- If evidence is ambiguous/unavailable, stop `BLOCKED` and do not repeat.
- Never modify `v0.9.5` history or force-push.

## Preflight

Verify browser PID/window, exact session identity, provider/model, installed entry/lease hashes, Gateway process identity, and durable baseline read-only. Session must equal `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`.

## Semantic request

Send exactly:

`CNX-343-LIVE-TIMEOUT-REQUALIFICATION: Reply exactly with DONE.`

## Required evidence

Correlate one real lifecycle and capture exact session, Ticket, Run, Call, `direct_model_call_started`, `timeoutMs=2700000`, `deadlineAt-startedAt=2700000ms`, provider/model, inference attempt, completion, delivery, outbox `0`, and no duplicate owner. Record post-run installed artifact/load evidence where possible without mutation.

## PASS

PASS only if the live call produces durable `timeoutMs=2700000` and `deadlineAt-startedAt=2700000ms` with correct provider/model and coherent Ticket → Run → Call → Result → Delivery lifecycle, outbox `0`, and no duplicate ownership.

## FAIL

If live lease is `timeoutMs=900000`, report `FAIL — LEGACY_TIMEOUT_AUTHORITY_REMAINS` and do not retry.

## BLOCKED

Block on session mismatch, unreadable/ambiguous durable evidence, or inability to correlate the single call safely. Do not repeat the request.

## Report

Publish `docs/operations/coordination/reports/CNX-20260914-343-live-timeout-requalification-report.md` and stop for independent ChatGPT review. Do not self-accept CNX-343.
