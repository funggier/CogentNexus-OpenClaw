# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTANCE`
Current authorization: `TASK098_ACCEPTED_ONE_FRESH_DASHBOARD_SESSION_ONE_SEMANTIC_MESSAGE_AUTHORIZED`
Task ID: `CNX-20260827-099`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-099-final-authenticated-fresh-session-semantic-acceptance.md`](tasks/CNX-20260827-099-final-authenticated-fresh-session-semantic-acceptance.md)

## Task 098 accepted

Task 098 report:

`bd068ca94e10525bd0a0743b6c1916cb56de78a0`

Independent disposition:

`ACCEPT_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`

Review:

[`reviews/CNX-20260827-098-state-gated-fresh-session-readiness.md`](reviews/CNX-20260827-098-state-gated-fresh-session-readiness.md)

Publication fence is valid: execution `2902e3e5720d621767925b36bc83691b103f2ec2` -> report `bd068ca94e10525bd0a0743b6c1916cb56de78a0` is one report-only commit.

Task 098 used the preferred no-extra-action path: one of the Task-097-created empty Dashboard sessions was already selected, authenticated, distinct from Main/Task-092, empty/staged and associated with zero Ticket/outbox/provider effect. No New Session action or retry was needed.

Readiness token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

## Final Task 099 semantic contract

Exactly one semantic user message is authorized through the authenticated selected Dashboard target.

Before nonce generation, Task 099 must re-snapshot the **exact selected Dashboard session ID/key** and prove it is still fresh/empty, distinct from Main/Task-092/Task-076, owner-authenticated and free of stale/fallback state.

If exact target identity is ambiguous, stop before nonce/send.

Only after that preflight generate one new `CNXSEM3-...` nonce and send exactly:

`ตอบกลับข้อความนี้เพียงว่า <NEW_NONCE>`

Semantic send count must remain exactly 1. No resend/retry under any result.

Required end-to-end proof:

- one fresh Dashboard session;
- exactly one Ticket;
- Ticket accepted and routed before correlated Ollama inference;
- exactly one correlated `ollama/qwen3.5:9b` inference;
- exact final assistant payload durably staged before native delivery;
- exactly one visible nonce reply;
- `response_ready -> delivery_confirmed -> completed` for the exact Ticket/run/session;
- no duplicate Ticket/route/provider/outbox/reply/promotion effect;
- after completion, New Session continuity with zero additional semantic/provider effect.

## Retry policy v1

Read-only operations may use up to 3 attempts total.

Low-impact state-changing session-management operations may use at most 2 attempts total, with attempt 2 allowed only after at least a bounded grace period and fresh state proving attempt 1 had no effect.

If attempt 1 appears late, treat it as completed and do not retry. Ambiguous/partial effects are not retryable.

The semantic message itself remains single-attempt.

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN`.

## Hard fence

No second semantic message, CLI owner substitute, direct Ollama/provider probe, install/reset/repair/cleanup, session deletion/normalization, plugin-generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, Task-092 rewrite, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Credential values must remain private and must not be read, copied, logged, requested or re-entered by the executor.

## Required success token

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Final gate

Only independent acceptance of a valid Task-099 report and report-only publication fence may close final OpenClaw semantic acceptance. A visible correct reply by itself is insufficient.
