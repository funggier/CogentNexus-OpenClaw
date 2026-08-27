# Active Coordination Task

Status: `AWAITING_OPERATOR_DESIGN_APPROVAL`
Execution mode: `COORDINATION_BOUNDED_STATE_GATED_RETRY_POLICY_PENDING_APPROVAL`
Current authorization: `NO_FINAL_SEMANTIC_SUCCESSOR_AUTHORIZED`
Task ID: `PENDING_CNX-20260827-098`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator approval and successor publication

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 097 result

Report:

`41a119b686daa4fc64b8f8481329a1be78462641`

Reported result:

`BLOCKED_FRESH_SESSION_ENTRY_FAILURE`

Independent decision:

`ACCEPT`

Disposition:

`ACCEPT_BLOCKER_STATE_UNVERIFIED_UI_RETRY_DUPLICATED_FRESH_SESSION_ENTRY`

Review:

[`reviews/CNX-20260827-097-prove-post-task-dashboard-owner-fresh-session-readiness.md`](reviews/CNX-20260827-097-prove-post-task-dashboard-owner-fresh-session-readiness.md)

Publication fence is valid: execution `f3a6bb9783d508a2b7d57162728018b7955d4b81` -> report `41a119b686daa4fc64b8f8481329a1be78462641` is one report-only commit.

## What Task 097 proved

The Dashboard/control surface was authenticated and visibly ready before the New Session action. Live MANAGED generation 24, exact plugin fingerprint, SQLite integrity, Ticket/outbox/event counts and retired Task-092 evidence remained stable.

No semantic message or provider inference occurred.

The blocker was an input-correlation race: the first background New Session click returned `unverifiable` but was delayed rather than absent. A foreground re-issue then caused two new Dashboard sessions to materialize. The strict one-transition Task-097 acceptance criterion therefore was not met.

The two empty sessions are evidence and must not be cleaned up merely to normalize the run.

## Pending bounded retry-policy design

The operator proposed allowing limited retries when the first error is simple and non-impacting.

Recommended state-gated policy:

1. read-only operations: up to 2 retries (3 attempts total) when no mutation is possible;
2. state-changing low-impact operations: at most 1 retry (2 attempts total), but only after a bounded grace period and fresh state verification prove attempt 1 produced no effect;
3. if attempt 1's effect appears during verification, treat it as completed and do not retry;
4. ambiguous or partially mutated state is not retryable;
5. semantic sends/provider inference/install/uninstall/reset/destructive cleanup and other externally visible non-idempotent effects remain single-attempt unless a task-specific idempotency proof explicitly authorizes retry;
6. every retry records attempt number, failure reason, wait/grace interval, fresh pre-retry state and retry-eligibility proof.

The final semantic send itself remains one-message/one-nonce only under the current acceptance design.

## Hard fence while awaiting approval

Until the operator approves this retry-policy design:

- do not create/run Task 098;
- do not retry New Session;
- do not send a semantic message or generate a nonce;
- do not call provider/Ollama directly;
- do not install/reset/repair/cleanup;
- do not delete or normalize Task-097 empty sessions;
- do not mutate controller/startup/Supervisor/AGENTS/config/runtime/SQLite or retired Task-092 evidence.

## Successor logic

After explicit approval, publish a narrow readiness successor using the state-gated retry policy. It should first observe current Dashboard/session state, then establish one fresh staged session without semantic send. Only independent PASS may release the final authenticated one-message fresh-session semantic acceptance.
