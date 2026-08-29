# CNX-20260830-152 — Independent Review

## Disposition

`ACCEPT`

## Scope of acceptance

This disposition accepts the Task-152 report as controlled real-Windows evidence. It does **not** accept Phase P and does **not** authorize Phase Q, merge, tag, release, or another Dashboard semantic attempt.

## Findings

Task 152 removed the Task-151 UI-control ambiguity by using operator-owned real-mouse composer and Send gates. The one Send produced exactly one durable Ticket, Ticket-first ordering, exactly one direct model call on the frozen Ollama route, and exactly one visible ACK. The direct model call completed without recovery or duplicate inference.

The required durable result boundary nevertheless failed: `response_ready` was present, but no `cnx_assistant_delivery` `direct_result` row, delivery confirmation, or completed event existed. The Ticket ended `failed` with `failure_delivery_suppressed`. SQLite remained healthy, pending outbox returned to zero, and no resend/alternate semantic transport occurred.

The publication commit `58d0d222e5463d736bf4a05cac36b23900ebaff5` adds only the matching Task-152 report. No source/config/runtime repair was mixed into the evidence commit.

## Classification

The evidence is sufficient to reject UI/mouse harness failure and to classify the observed acceptance result as a real product/runtime durable-capture failure.

However, the report does not contain the existing redacted `delivery-observe` hook sequence needed to identify the first internal boundary among:

- `reply_dispatch` handler entry/skip;
- `appendBeforeDeliver` callback registration/invocation;
- final-payload filtering;
- `stageDashboardDirectResult` attempt/rejection/exception/success.

The durable `response_ready` row alone cannot prove that the callback/staging path ran, because the installed source can create `response_ready` from the fallback `markDashboardAwaiting` path when no durable result is owned.

## Required next step

Before any source patch, collect the already-existing Task-152 redacted delivery telemetry from the real Windows OpenClaw logs in a read-only task. No new Dashboard semantic Send is authorized. The evidence collection must identify the first missing/failing hook boundary without exposing prompt/response text, nonce, raw Ticket/run/session identifiers, credentials, or secrets.

After that evidence is independently reviewed, ChatGPT owns offline root-cause analysis and TDD repair. A new live semantic attempt requires a repaired/frozen candidate and separate authorization.
