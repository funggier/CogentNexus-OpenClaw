# CNX-343 — Live Timeout Requalification After Verified Runtime Installation

- Parent: `CNX-342`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Fresh Dashboard session: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`
- Required provider/model: `ollama` / `qwen3.8:27b`
- Required direct-model-call lease timeout: `2700000ms` / `2700s`

## Objective

Perform exactly one bounded live semantic request against the already-established CNX-340E fresh Dashboard session, after CNX-342's verified complete repaired-artifact installation and one Gateway restart. Prove from real durable runtime evidence that the running Gateway now persists the repaired `2700000ms` direct-model-call lease instead of the legacy `900000ms` lease.

This is a live runtime requalification only. Do not modify installation or source during this task.

## Hard fences

- Use only the exact fresh Dashboard session above.
- Exactly one semantic request.
- Do not create a new session or click `New session`.
- Do not reinstall, rebuild, restart Gateway, or alter the plugin.
- Do not change provider/model/timeout/config/controller/database.
- No retry, resend, recovery, fallback, or manual dispatch.
- No OpenAI.
- Do not wait 2700 seconds; inspect the durable lease directly.
- If any required evidence is ambiguous or unavailable, stop `BLOCKED` and do not repeat the request.
- Never modify `v0.9.5` history, release, tag, or force-push.

## Preflight

Read-only verification must establish:

- current Firefox PID/window
- current Dashboard URL and session identity
- exact match to `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`
- provider/model presentation
- installed entry SHA and lease SHA, matching CNX-342's repaired hashes where observable
- Gateway process identity after CNX-342 restart
- baseline durable counts for correlation

If the session identity does not match, stop `BLOCKED — FRESH_SESSION_IDENTITY_MISMATCH`.

## Single semantic request

Send exactly:

`CNX-343-LIVE-TIMEOUT-REQUALIFICATION: Reply exactly with DONE.`

No other request is permitted.

## Required evidence

Correlate exactly one real lifecycle and capture:

- session ID
- Ticket ID
- Run ID
- Call ID
- `direct_model_call_started` durable event
- `timeoutMs = 2700000`
- `deadlineAt - startedAt = 2700000ms`
- provider `ollama`
- model `qwen3.8:27b`
- absence of `timeoutMs = 900000` on this call
- inference attempt identity
- call ended
- result/delivery identity
- completion
- final outbox `0`
- no duplicate owner

Also record the post-run installed artifact hashes/load evidence if available without restarting or mutation.

## PASS criteria

PASS only if the real call uses the verified post-CNX-342 runtime and produces durable direct-model-call lease evidence with:

`timeoutMs = 2700000`

and:

`deadlineAt - startedAt = 2700000ms`

with correct provider/model and one coherent Ticket → Run → Call → Result → Delivery lifecycle, final outbox `0`, and no duplicate ownership.

## FAIL criteria

If the tested live call persists `timeoutMs = 900000`, report:

`FAIL — LEGACY_TIMEOUT_AUTHORITY_REMAINS`

Do not retry.

## BLOCKED criteria

Use `BLOCKED` if:

- session identity cannot be verified
- durable lease cannot be read/correlated
- provider/model cannot be correlated
- the call identity is ambiguous
- any evidence needed for PASS/FAIL is unavailable

Do not repeat the request to obtain missing evidence.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260914-343-live-timeout-requalification-report.md`

The report must distinguish observed facts from deductions and include exact identities, timeout/deadline arithmetic, provider/model, lifecycle, delivery, outbox, and post-CNX-342 artifact/load evidence.

Stop for independent ChatGPT review. Do not self-accept CNX-343.
