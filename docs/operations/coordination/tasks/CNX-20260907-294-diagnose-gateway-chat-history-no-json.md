# CNX-20260907-294 — Diagnose Gateway chat.history No-JSON Boundary

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-293`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Objective

Find the root cause of the installed OpenClaw Gateway `chat.history` call returning exit 0 with empty stdout during durable delivery, without mutating the pending Ticket or replaying delivery.

## Allowed work

- Read current GitHub state and exact installed/runtime source or client behavior.
- Inspect supported `chat.history` request/response contract and the exact caller/transport used by CNX.
- Reproduce only with isolated read-only diagnostics that do not send messages or alter durable state.
- Compare normal Discord response visibility with Gateway history availability.
- Publish evidence and a minimal repair proposal if a repository defect is proven.

## Prohibited

No semantic send, retry/replay/redelivery, Ticket disposition/cancel, SQLite/Ticket/session/transcript mutation, reset, session deletion/creation, credential exposure/change, installer, release, or force push.

## Completion

Publish a root-cause report. If a deterministic repository repair is proven, create a separate bounded TDD repair task; otherwise set `NEEDS_CHATGPT` with the exact missing decision.
