# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_KNOWN_WORKING_DASHBOARD_INPUT_AND_FINAL_SEMANTIC_ACCEPTANCE`
Current authorization: `OPERATOR_APPROVED_KNOWN_WORKING_INPUT_REPRODUCTION_AND_FINAL_SEMANTIC_CONTINUATION`
Task ID: `CNX-20260827-100`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Operator-approved Task 100 expansion

The operator reported that current testing has reached a known-working Dashboard input method: Codex can now type into the real OpenClaw composer and understands the interaction sequence.

The operator explicitly approved expanding Task 100 so it no longer stops at readiness-only. Task 100 must first reproduce and document the working input method, then continue the existing final semantic acceptance in the same task.

## Task 099 accepted blocker carried forward

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Independent disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Exact target established by Task 099:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

Task 099 semantic send count was `0`; no Ticket/provider/delivery effect occurred and its nonce is retired.

## Active Task 100

[`tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`](tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md)

Task 100 now has two consecutive obligations:

1. reproduce the known-working Dashboard input method and record it under `Known-working Dashboard input method` without exposing secrets;
2. once the composer is clean/empty and durable baseline unchanged, continue final semantic acceptance immediately in the same task.

A non-sent `CNXINPUT-READY` sentinel may be used to prove composer targeting, then must be cleared before nonce generation. No Send may occur during the sentinel proof.

If a non-sent operator/Codex test draft is already present, do not publish its text. Prove it caused no durable semantic/provider effect, clear it, and verify the composer is empty. If any test content was actually sent, stop and correlate that effect rather than creating another send.

## Final semantic contract

Only after the input method is reproduced and the exact target/composer is clean:

- generate one new `CNXSEM4-...` nonce;
- send exactly one Dashboard message;
- no resend under any result;
- prove exactly one Ticket accepted/routed before one `ollama/qwen3.5:9b` inference;
- prove exact durable final payload staging before native delivery;
- prove exactly one visible nonce;
- prove `response_ready -> delivery_confirmed -> completed` for the exact Ticket/run/session;
- prove no duplicate Ticket/route/provider/outbox/reply/promotion effect;
- after completed only, prove New Session continuity with zero additional semantic/provider effect.

Required method token:

`DASHBOARD_KNOWN_WORKING_INPUT_METHOD_PROVEN`

Required final success token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Retry policy v1

Read-only operations: maximum 3 attempts total.

Low-impact pre-send UI operations such as focus/click/activation/non-sent typing/clearing: maximum 2 attempts total, with grace + fresh state required before attempt 2.

If attempt 1 takes effect late, do not retry. Ambiguous/partial state blocks retry.

Semantic Send remains exactly one attempt.

Post-completion New Session may use state-gated retry policy for session-management only.

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Exact plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live baseline remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health and `NO_FLASH_MULTI_TICK_REPROVEN`.

## Hard fence

No second semantic send, Task-099 nonce reuse, CLI/channel owner substitute, direct provider/Ollama probe, synthetic Ticket, install/reset/repair/cleanup, session normalization, plugin-generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, prior-evidence rewrite, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Credential values remain private and must not be read, copied, printed, logged, requested or re-entered by the executor.

## Publication requirement

Task 100 publishes one report-only commit at:

`docs/operations/coordination/reports/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`

The report must document the current working Dashboard input sequence so later executions do not have to rediscover it.

## Final gate

Only independent acceptance of the Task-100 report may close final semantic acceptance. Visible UI success alone is insufficient; durable staging, delivery confirmation and terminal completion are mandatory.
