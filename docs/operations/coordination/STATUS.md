# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator approved state-gated bounded retries and the bounded Task-100 foreground/input readiness design; continuation remains authorized through final authenticated semantic acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Task 096 live deployment remains accepted.

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Accepted plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN`.

## Task 099 result and review

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Independent disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Exact authenticated fresh target established by Task 099:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

Task 099 stopped before any semantic send because the exact OpenClaw Firefox window could not be proven foreground while another Firefox window/process was foreground. Semantic send count remained 0; no Ticket/route/provider/durable-delivery/outbox effect was created. Its generated nonce is retired.

This is an OS/UI foreground-targeting blocker, not evidence of a semantic-pipeline regression. Task 092 previously proved the real Dashboard send/Ticket/provider/visible-reply path; Task 093 repaired the later durable-staging defect and Task 096 installed that repair live.

## Active Task 100

[`tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`](tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md)

Execution mode:

`READ_ONLY_DASHBOARD_FOREGROUND_INPUT_TARGET_READINESS`

Authorization:

`TASK099_ACCEPTED_BOUNDED_FOREGROUND_READINESS_APPROVED`

Task 100 sends zero semantic content and generates no nonce.

It must uniquely correlate the exact Firefox OpenClaw Dashboard top-level window/HWND to the accepted target session, acquire that exact HWND as the actual Windows foreground input window, and prove the intended Dashboard composer can be focused/selected while remaining empty.

Required readiness token:

`DASHBOARD_FOREGROUND_COMPOSER_READY_NO_SEND`

Required PASS token:

`PASS_DASHBOARD_FOREGROUND_INPUT_TARGET_READY_NO_SEND`

## Retry policy v1

- read-only operations: maximum 3 attempts total;
- low-impact focus/window-activation operations: maximum 2 attempts total;
- attempt 2 requires at least 3 seconds grace and fresh evidence proving attempt 1 did not already take effect;
- if attempt 1 appears late, treat it as success and do not retry;
- ambiguous/partial/delayed state is not retryable;
- semantic sends/provider inference/install/reset/destructive effects remain single-attempt unless separately proven idempotent and explicitly authorized.

## Hard fence

Task 100 performs no semantic send, provider/Ollama inference, install/reset/repair/cleanup, session cleanup, plugin-generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, prior-evidence rewrite, restart/reboot, merge/tag/release or force push.

Credential values must not be read, copied, printed, logged, requested or re-entered by the executor.

## Successor logic

Only independent acceptance of:

`PASS_DASHBOARD_FOREGROUND_INPUT_TARGET_READY_NO_SEND`

may authorize a new final authenticated semantic task.

That successor must re-verify the exact target session + exact foreground OpenClaw HWND + empty focused composer before nonce generation, then send one brand-new nonce exactly once. It must prove one Ticket accepted/routed before one correlated Ollama inference, durable final-payload staging before native delivery, one exact visible reply, exact `response_ready -> delivery_confirmed -> completed`, no duplicate effect, and post-completion New Session continuity using state-gated retry only for session-management actions.
