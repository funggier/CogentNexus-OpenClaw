# CNX-20260907-293 — Verify Human-Initiated Clean Recreation

## Disposition

`NEEDS_CHATGPT__RECREATION_CREATED__DURABLE_DELIVERY_UNCONFIRMED__NO_RETRY`

The user-created Discord message produced a fresh OpenClaw session and CNX lifecycle generation. Model inference and response-ready events occurred, but durable assistant delivery did not settle during the bounded observation window. The target remains non-clean for acceptance. Hermes performed no send, replay, redelivery, disposition, reset, or mutation.

## Authority and observation

- branch: `agent/v0.9.3-full-stabilization`
- authority HEAD before Task293: `46d7b57b89c8d169223a40c1f7b85e5a0544baa3`
- active task: `CNX-20260907-293`
- candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- human message was already sent before Hermes execution, as recorded by the task authority
- bounded observer start: approximately `2026-09-07T02:39:48Z`
- bounded observation window: 1500 seconds; expired after approximately 25 minutes
- final read-only capture: `2026-09-07T03:05:17Z`

## Fresh OpenClaw recreation

The target key was reused by the human-created Discord channel session, but the session identity was new:

- key: `agent:main:discord:channel:1391855033993138217`
- new session ID: `2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5`
- session status: `done`
- OpenClaw session file: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5.jsonl`
- session updatedAt: `1788748629658`
- model: `ollama/qwen3.5:9b`

The previous deleted session ID `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2` did not reappear. The new session was not created by Hermes.

Raw before/after inventory evidence:

- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task293-sessions.json`
- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-task293-sessions-after.json`

## CNX lifecycle binding

Fresh target `cnx_sessions` row after recreation:

```json
{
  "session_key": "agent:main:discord:channel:1391855033993138217",
  "state": "active",
  "generation": 2,
  "created_at": "2026-09-06T13:45:36.714Z",
  "updated_at": "2026-09-07T02:35:10.520Z",
  "deleted_at": null,
  "delete_reason": null,
  "session_id": "2b841ed6-c2dc-4699-b5ac-9e2716e6d5d5"
}
```

This proves a fresh generation-2 lifecycle and exact binding to the new OpenClaw session ID. The prior generation-1 deletion tombstone was not manually altered by Hermes.

## New Ticket and event order

New Ticket:

- ID: `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`
- owner key: `agent:main:discord:channel:1391855033993138217`
- lease generation at Ticket row: `0`
- final Ticket status: `accepted`
- failure class: `interrupted`
- failure message: `Direct response delivery was not confirmed before deadline`
- `delivery_confirmed_at=null`
- final updatedAt: `2026-09-07T03:04:57.582403+00:00`

Observed durable event order:

1. `accepted` — `2026-09-07T02:35:10.529Z`
2. `routed` — `2026-09-07T02:35:10.534Z`
3. `direct_model_call_started` — `2026-09-07T02:35:10.666Z`
4. `direct_model_call_ended` / `completed` — `2026-09-07T02:37:09.466Z`
5. `response_ready` — `2026-09-07T02:37:09.577Z`
6. `direct_redelivery_timeout` — `2026-09-07T02:39:11.999Z`
7. `direct_recovery_runtime_started` — `2026-09-07T02:39:16.293Z`
8. `direct_recovery_response_ready` — `2026-09-07T02:39:41.789Z`
9. repeated `assistant_delivery_retry` events through `2026-09-07T03:04:57.582403+00:00`

The model/recovery path reached response-ready, but that is not durable delivery proof.

## Durable delivery boundary

At final read-only capture:

```json
{
  "status": "pending",
  "owner_generation": 2,
  "idempotency_key": "cnxclaw-direct-result:CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc:g2",
  "attempt_count": 43,
  "last_error": "OpenClaw Gateway RPC chat.history returned no JSON output (exit=0, stdout=none, stderr=empty)",
  "delivered_at": null
}
```

- `cnx_assistant_delivery` row count: `1`, still `pending`
- `delivery_confirmed_at`: `null`
- `ticket_outbox` rows: `0`
- durable delivery: **not confirmed**
- observer saw no terminal successful delivery during the bounded window

This is a delivery-boundary failure/non-clean outcome, not a model timeout and not a clean recreation acceptance PASS. The visible Discord response, response-ready event, and recovery response-ready event were not promoted to durable delivery proof.

## Protected and prior state

Protected owner remained distinct and unchanged:

- Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner key: `agent:main:discord:channel:1531199905673252946`
- Ticket status: `accepted`
- failure class: `interrupted`
- delivery confirmation: `null`
- `cnx_sessions`: `active`, generation `1`
- protected `session_id`: `null`

The prior generation-1 target tombstone was not mutated by Hermes. No replay, recovery disposition, redelivery, cancellation, reset, or deletion was performed.

## Health

Final direct read-only probes:

- Gateway: HTTP `200`, `{"ok":true,"status":"live"}`
- Ollama: HTTP `200`; `qwen3.5:9b` present
- SQLite integrity: `ok`

## Hard-fence ledger

- human semantic send: `1` (operator action, pre-authorized and not performed by Hermes)
- Hermes semantic sends: `0`
- session creation by Hermes: `0`
- `sessions.delete`: `0`
- reset/cancel substitute: `0`
- replay/redelivery/disposition: `0`
- manual Ticket/SQLite/session/transcript mutation: `0`
- protected Ticket/session mutation: `0`
- installer/install-over/uninstall: `0`
- Gateway/Ollama/service mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Stop boundary and next review

Do not resend a Discord message, retry `chat.history`, replay recovery, redeliver, cancel, reset, or delete this generation. A successor task must explicitly address the observed Gateway `chat.history` no-JSON delivery boundary and define whether a new clean acceptance target is allowed. Task293 stops with `NEEDS_CHATGPT`.
