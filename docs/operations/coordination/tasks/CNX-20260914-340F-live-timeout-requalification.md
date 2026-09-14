# CNX-340F — Live Model-Call Timeout Requalification

- Parent: `CNX-340E`
- Branch: `agent/v0.9.6-live-timeout-requalification-2`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: operator
- Fresh session established by CNX-340E: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`

## Objective

Perform exactly one bounded live semantic request in the freshly established Dashboard session and prove, from real runtime durable evidence, that the repaired direct-model-call lease carries the authoritative `2700s / 2700000ms` timeout into the actual model-call path.

This task is a runtime requalification of the CNX-340A timeout-authority repair. It is not a source-only or isolated synthetic test.

## Required provider/model

- Provider: `ollama`
- Model: `ollama/qwen3.8:27b`
- Required timeout authority: `2700 seconds`
- Required durable lease field: `timeoutMs = 2700000`

OpenAI is explicitly excluded from this task.

## Hard fences

- Use only the fresh Dashboard session established by CNX-340E: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`.
- Exactly one semantic request.
- Do not create another Dashboard session.
- Do not click `New session` again.
- Do not retry, resend, recover, fallback, manually dispatch, or submit a second request.
- Do not change provider, model, timeout, config, controller, installation, release, or tag state.
- Do not modify production code or tests.
- Do not change `v0.9.5` or rewrite published history.
- Do not wait for the full 2700-second timeout; inspect the durable `model_call_started` lease evidence directly.
- If any required evidence is ambiguous, stop and report `BLOCKED`; do not repeat the semantic request.

## Preflight evidence

Before submitting the single semantic request, capture read-only evidence of:

- exact Firefox PID/window
- current Dashboard URL/session identity
- current session equals the CNX-340E fresh session identity above
- provider/model presentation
- relevant runtime/config/controller state without mutation
- current durable database counts/relevant baseline needed for post-run correlation

If the fresh session identity does not match exactly, stop `BLOCKED` and do not create or activate another session.

## Semantic request

Submit exactly one bounded prompt whose purpose is only to exercise one real model call and allow durable timeout evidence to be captured. The prompt must not request configuration changes, file mutations, provider changes, or destructive actions.

Suggested prompt:

`CNX-340F-LIVE-TIMEOUT-TEST: Reply exactly with DONE.`

## Required live evidence

Correlate one unique lifecycle across the real runtime:

- fresh Dashboard session
- one Ticket/admission identity, if applicable
- one Run identity
- one `model_call_started` durable event/lease
- exact `timeoutMs = 2700000`
- provider `ollama`
- model `ollama/qwen3.8:27b`
- no legacy `timeoutMs = 900000` for this call
- completion/result
- delivery confirmation
- outbox final state `0`
- no duplicate owner

Also verify that the timeout value is sourced through the repaired runtime authority, not merely copied from a report or static configuration.

## PASS criteria

PASS only if one real live model-call execution from the CNX-340E fresh session produces durable direct-model-call lease evidence with `timeoutMs = 2700000`, uses `ollama/qwen3.8:27b`, completes normally, and yields one coherent Ticket/Run/Result/Delivery lifecycle with no duplicate ownership and outbox `0`.

The absence of a 900-second lease is part of PASS evidence.

## BLOCKED / FAIL conditions

- `timeoutMs = 900000` or any legacy 900-second lease on the tested call: `FAIL — LEGACY_TIMEOUT_AUTHORITY_REMAINS`.
- Fresh session identity mismatch: `BLOCKED — FRESH_SESSION_IDENTITY_MISMATCH`.
- Durable timeout evidence absent or unreadable: `BLOCKED — LIVE_TIMEOUT_EVIDENCE_UNAVAILABLE`.
- Any second semantic request or retry: task fence violation; stop immediately and report.
- Provider/model/config/controller/install mutation: task fence violation; stop immediately and report.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260914-340F-live-timeout-requalification-report.md`

The report must include exact session, Ticket/Run/Result/Delivery identifiers, exact `timeoutMs`, provider/model, event timestamps, completion/delivery evidence, and final outbox state.

Stop for independent ChatGPT review. Do not self-accept CNX-340F.
