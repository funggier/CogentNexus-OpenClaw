# CNX-20260907-298 — Bounded Enable Deploy and Worker Requalification

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-297`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Explicit human authorization

The human authorized:

`cnxclaw enable` bounded to deploy the tested Task296 repair and requalify the detached delivery worker.

This authorization does not include uninstall, reset, install-over, release, unrelated service changes, or semantic messaging.

## Objective

Use the canonical `cnxclaw enable` lifecycle path to deploy/activate the tested worker runtime resolver, then verify whether the live detached worker adopts the Gateway Node runtime and resolves the `chat.history` no-JSON delivery boundary.

## Preconditions

Freshly verify:

- current remote HEAD and active coordination state;
- Task296 TDD evidence and exact repair identity;
- target generation-2 pending Ticket/session;
- protected Ticket/session exclusion;
- Gateway/Ollama/Host/Supervisor health;
- expected enable scope and current worker state.

If scope is broader than the authorized bounded repair deployment, stop.

## Allowed action

1. Run the canonical `cnxclaw enable` command exactly once.
2. Capture command output, exit code, file/config hashes, and before/after worker state.
3. Verify the worker adopts `C:\Program Files\nodejs\node.exe` through sanitized instrumentation.
4. Allow only natural existing-worker processing needed for requalification; do not manually retry, replay, redeliver, cancel, dispose, or settle the pending Ticket.
5. Read-only inspect delivery status, `chat.history` stream evidence, and service health.

## Strict fences

- `cnxclaw enable`: maximum 1
- uninstall: 0
- reset: 0
- install-over: 0
- semantic sends: 0
- manual replay/redelivery/disposition: 0
- manual Ticket/SQLite/session/transcript/outbox/recovery mutation: 0
- session create/delete: 0
- credential exposure/change: 0
- protected state mutation: 0
- release/tag/force push: 0

## Stop rules

Stop without retry if enable fails, scope is ambiguous, worker does not adopt the tested repair, health degrades, or the pending delivery remains ambiguous. Do not claim durable delivery from response-ready or visible Discord text alone.

## Completion

Publish an evidence-rich report with exact command result, deployment hashes, worker runtime adoption, delivery outcome, and remaining uncertainty. Then set coordination to `WAITING_FOR_CHATGPT_REVIEW`.
