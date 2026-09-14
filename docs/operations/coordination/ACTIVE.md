# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_LIVE_TIMEOUT_REQUALIFICATION`
Execution mode: `ONE_BOUNDED_LIVE_SEMANTIC_REQUEST`
Task ID: `CNX-340F`
Parent: `CNX-340E`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Fresh session: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`
Active branch: `agent/v0.9.6-live-timeout-requalification-2`

## Objective

Execute exactly one bounded live semantic request in the CNX-340E fresh Dashboard session and prove from real durable runtime evidence that the repaired direct-model-call lease carries `timeoutMs=2700000` (2700 seconds) into the actual Ollama model-call path.

## Required provider/model

- Provider: `ollama`
- Model: `ollama/qwen3.8:27b`
- Timeout authority: `2700s / 2700000ms`
- OpenAI: excluded

## Hard fences

- Use only the exact fresh session above.
- Exactly one semantic request.
- No new session and no `New session` click.
- No second request, retry, resend, recovery, fallback, or manual dispatch.
- No provider/model/config/timeout/controller/database/install/release/tag mutation.
- No production code or test changes.
- Do not wait 2700 seconds; inspect the durable lease evidence directly.
- If evidence is ambiguous or unavailable, stop `BLOCKED`; do not repeat the request.
- Never modify `v0.9.5` history or force-push.

## Preflight

Capture read-only evidence for browser PID/window, current URL/session identity, exact fresh-session match, relevant provider/model/runtime configuration, and durable baseline counts needed for correlation.

If the session identity is not exactly `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`, stop `BLOCKED` without creating another session.

## Semantic request

Send exactly:

`CNX-340F-LIVE-TIMEOUT-TEST: Reply exactly with DONE.`

## Required evidence

Correlate one coherent real lifecycle:

- Dashboard session
- Ticket/admission identity (if applicable)
- Run identity
- `model_call_started` durable lease/event
- `timeoutMs=2700000`
- provider `ollama`
- model `ollama/qwen3.8:27b`
- no `timeoutMs=900000` on this call
- completion/result
- delivery confirmation
- final outbox `0`
- no duplicate owner

## PASS

PASS only if the real call uses the fresh session, produces durable lease evidence showing `timeoutMs=2700000`, uses the required provider/model, completes normally, and yields one correlated Ticket/Run/Result/Delivery lifecycle with outbox `0`.

## Disposition

Publish `docs/operations/coordination/reports/CNX-20260914-340F-live-timeout-requalification-report.md` and stop for independent ChatGPT review. Do not self-accept CNX-340F.
