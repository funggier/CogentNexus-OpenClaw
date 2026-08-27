# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `READ_ONLY_AUTHENTICATED_DASHBOARD_STATE_GATED_FRESH_SESSION_READINESS`
Current authorization: `TASK097_ACCEPTED_STATE_GATED_RETRY_POLICY_APPROVED`
Task ID: `CNX-20260827-098`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-098-state-gated-fresh-session-readiness.md`](tasks/CNX-20260827-098-state-gated-fresh-session-readiness.md)

## Task 097 accepted blocker

Task 097 report:

`41a119b686daa4fc64b8f8481329a1be78462641`

Independent disposition:

`ACCEPT_BLOCKER_STATE_UNVERIFIED_UI_RETRY_DUPLICATED_FRESH_SESSION_ENTRY`

The authenticated Dashboard/control surface and live health were sound. The failure was an input-correlation race: a delayed first New Session click returned `unverifiable`, then an immediate re-issue caused two empty Dashboard sessions to materialize. No semantic/provider/Ticket/outbox effect occurred.

The two empty sessions remain untouched evidence; do not delete them merely to normalize session count.

## Operator-approved retry policy v1

From Task 098 forward:

1. read-only operations may use up to 3 attempts total;
2. low-impact state-changing operations may use at most 2 attempts total;
3. before a second state-changing attempt, wait a bounded grace interval and prove from fresh state that attempt 1 produced no effect;
4. if attempt 1's effect appears during verification, treat it as completed and do not re-issue;
5. ambiguous/partial/delayed mutation is not retryable;
6. semantic send/provider inference/install/uninstall/reset/destructive cleanup and other high-impact non-idempotent effects remain single-attempt unless a later task explicitly proves idempotency and authorizes retry;
7. each retry must record attempt, reason, grace interval, fresh state and eligibility evidence;
8. `unverifiable` means state unknown, not `not executed`.

For New Session in Task 098, an `unverifiable` first action requires at least a 5-second wait and fresh session/UI verification before retry eligibility can be decided.

## Task 098 preferred path

Task 098 must first inspect the current authenticated Dashboard/session inventory.

If one currently selected Task-097-created empty Dashboard session can be proven fresh, empty, distinct from Main/Task-092 and associated with zero Ticket/outbox/provider effect, use it as the readiness target and do **not** create another session.

Only if current state cannot establish a unique fresh target may Task 098 use New Session under the state-gated bounded retry policy.

Required readiness token:

`DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND`

Required PASS token:

`PASS_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN` from Task 096.

## Hard fence

Task 098 is readiness-only.

No semantic send/nonce, provider/Ollama inference, install/reset/repair/cleanup, session deletion, plugin-generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, Task-092 rewrite, restart/reboot, merge/tag/release or force push is authorized.

The token/password value must never be read, printed, copied, logged, requested or re-entered by the executor.

## Successor gate

Only independent acceptance of:

`PASS_STATE_GATED_DASHBOARD_FRESH_SESSION_READY_NO_SEND`

may authorize the final authenticated one-message semantic acceptance.

The final semantic send remains exactly one new nonce and one user send with no resend. State-gated retry may apply only to low-impact/read-only surrounding operations such as session-management verification.