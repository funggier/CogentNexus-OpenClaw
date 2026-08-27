# Active Coordination Task

Status: `AWAITING_OPERATOR_DESIGN_APPROVAL`
Execution mode: `DASHBOARD_FOREGROUND_INPUT_TARGET_READINESS_PENDING_APPROVAL`
Current authorization: `NO_NEW_SEMANTIC_SEND_AUTHORIZED`
Task ID: `PENDING_CNX-20260827-100`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator design approval

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 099 independent review

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Review:

[`reviews/CNX-20260827-099-final-authenticated-fresh-session-semantic-acceptance.md`](reviews/CNX-20260827-099-final-authenticated-fresh-session-semantic-acceptance.md)

Publication fence is valid: execution `44c343bc86df8020393f19ce971dff723e4384b5` -> report `d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac` is one report-only commit.

## What Task 099 established

Task 099 successfully identified the exact authenticated fresh/empty Dashboard target before send:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

The accepted MANAGED generation 24 / exact plugin fingerprint / healthy durable baseline remained intact.

A fresh Task-099 nonce was generated, but the exact OpenClaw Firefox window could not be proven to be the foreground input target. A separate Firefox window/process was foreground. The executor therefore correctly refused to type/send into an unverifiable composer.

Semantic send count remained `0`; no Ticket, route, provider inference, durable payload, visible semantic reply, or outbox settlement was created by Task 099.

The Task-099 nonce is retired and must not be reused.

## Important historical comparison

Task 092 previously proved the authenticated Dashboard semantic path itself can execute: one fresh Dashboard session, one semantic send, one Ticket, Ticket-before-provider ordering, one `ollama/qwen3.5:9b` inference, and one exact visible nonce response.

Task 092 failed later at durable delivery completion. That defect was repaired by Task 093 and the repaired source was installed and accepted live in Task 096.

Task 099 failed earlier than that path, at OS/UI foreground targeting. It is therefore not evidence of a semantic-pipeline or Task-093 regression.

## Pending bounded Task-100 design

Proposed successor is readiness-only and sends zero semantic content.

It should:

1. enumerate/correlate the exact Firefox OpenClaw Dashboard window to the authenticated target session without reading credentials;
2. verify the exact target session remains empty/staged and semantically untouched;
3. acquire the exact OpenClaw window as the actual foreground HWND before composer interaction;
4. verify the intended Dashboard composer is focusable/selected and empty without typing semantic test content;
5. use retry policy v1 only for low-impact focus/activation operations: at most two attempts, with a grace interval and fresh foreground/window/session verification before attempt 2;
6. if another window remains foreground, target identity is ambiguous, or any input action is unverifiable, stop with zero nonce/send;
7. make no product/runtime/SQLite/session cleanup mutation and no provider call.

Only independent PASS of this input-target readiness may authorize a new final semantic task with a brand-new nonce and exactly one send.

## Hard fence pending approval

Until the operator approves this bounded design:

- do not create/run Task 100;
- do not generate another semantic nonce;
- do not send or retry Task-099 semantic content;
- do not use CLI/channel/provider substitutes;
- do not install/reset/repair/cleanup;
- do not delete/normalize Dashboard sessions;
- do not mutate controller/startup/Supervisor/AGENTS/config/runtime/SQLite or retired evidence.
