# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_FINAL_DASHBOARD_DURABLE_DELIVERY_SINGLE_ATTEMPT`
Current authorization: `CNX-20260830-151_FINAL_DASHBOARD_DURABLE_DELIVERY_ACCEPTANCE`
Task ID: `CNX-20260830-151`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex with explicit operator manual gates

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md`](tasks/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md)

Task 151 is Phase P of the Full Stabilization and Final Acceptance Plan: the final single-attempt real Firefox Dashboard semantic/durable-delivery acceptance.

## Task-150 disposition

Task-150 report:

`docs/operations/coordination/reports/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance-review.md`

Review disposition: **ACCEPT**.

Task 150 proved the installed operator runtime sequence `stop → start → restart → disable → enable` exactly once each with correct maintenance/managed/passthrough semantics, real Gateway process boundary, healthy final MANAGED Ollama state, unchanged accepted provenance, SQLite integrity, semantic rows `0`, pending `0`, and Dashboard Sends `0`.

Accepted production implementation remains:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Expected installed plugin fingerprint remains:

`12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`

## Task-151 execution contract

This task is single-attempt.

Before semantic input, re-prove fresh GitHub authority, accepted installed provenance, healthy MANAGED Gateway/Ollama/recovery/delivery/SQLite state, zero unexplained active work, exact baseline counts, authenticated Firefox Dashboard, exact fresh/empty target session, empty composer, and freshly rediscovered exact PID/HWND.

Manual gates are mandatory:

1. operator manually clicks the exact `Message Assistant` composer once with the real mouse;
2. executor re-verifies focus/session/composer and exact prompt;
3. only after explicit executor authorization does operator manually activate Send exactly once.

After the one Send, no second Send/resend/alternate semantic channel is authorized. All further work is observation/read-only.

PASS requires exactly one Ticket, one direct model call, one visible exact ACK, one durable `cnx_assistant_delivery` direct-result row, native delivery confirmation, Ticket `completed`, no duplicate inference/delivery, telemetry privacy PASS, and final healthy runtime/SQLite/pending `0`.

A visible ACK without the durable row/confirmation/completion is FAIL, matching the Task-137 lesson. Task-138's durable-capture repair is specifically under live acceptance here.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-151-final-dashboard-durable-delivery-acceptance.md`

Then stop for independent ChatGPT review. Phase Q/final acceptance/release publication is not automatic.

## Hard fence

No second Dashboard Send/resend; no alternate semantic transport; no manual semantic/database mutation; no reset/uninstall/install/reinstall; no runtime lifecycle commands; no crash/recovery injection; no manual plugin/config/controller/ownership/process/service/task normalization; no reboot; no credentials/secrets; no merge/tag/release; no force push.
