# CNX-20260907-292 — Suna Fresh Read-Only Recreation Preflight

## Disposition

`PASS_READONLY_RECREATION_PREFLIGHT__PROPOSAL_ONLY__WAITING_FOR_CHATGPT_REVIEW`

Task292 completed a fresh read-only preflight after the confirmed user deletion. The disposable target is absent from the OpenClaw inventory, and the CNX lifecycle row is a deleted generation-1 tombstone with an explicit deletion timestamp and reason. Protected state is distinct and unchanged. The state is safe enough to propose a separately authorized clean recreation task, but Task292 did not create a session, send a message, or authorize recreation.

## Authority and timestamps

- branch: `agent/v0.9.3-full-stabilization`
- preflight remote HEAD: `c944a99cf829c1dcab3c56adc977845a41d4c972`
- active task: `CNX-20260907-292`
- candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- fresh preflight start: `2026-09-07T01:42:17Z`
- classification/report time: `2026-09-07T01:43:04Z`

## OpenClaw inventory

Fresh `openclaw sessions list --json` returned `count=8`, `totalCount=8`.

The target key and old session ID were absent:

- target key absent: `agent:main:discord:channel:1391855033993138217`
- old session ID absent: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- no replacement session was present for the target key

Remaining inventory included the protected owner key, but not the deleted target.

Raw inventory evidence:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-task292-sessions.json`

## CNX lifecycle/tombstone

Read-only SQLite inspection used `mode=ro` and `pragma integrity_check` returned `ok`.

The `cnx_sessions` schema is:

- `session_key`
- `state`
- `generation`
- `created_at`
- `updated_at`
- `deleted_at`
- `delete_reason`
- `session_id`

Fresh target row:

```json
{
  "session_key": "agent:main:discord:channel:1391855033993138217",
  "state": "deleted",
  "generation": 1,
  "created_at": "2026-09-06T13:45:36.714Z",
  "updated_at": "2026-09-07T00:54:15.815Z",
  "deleted_at": "2026-09-07T00:54:15.815Z",
  "delete_reason": "OpenClaw owner session deleted",
  "session_id": "c7a72073-64e4-4c2b-ba83-58f030e6eef0"
}
```

The old OpenClaw session ID is absent from the OpenClaw inventory. The CNX tombstone's `session_id` is a lifecycle tombstone identity and is not treated as an active OpenClaw replacement session.

## Old Ticket and delivery

Target setup Ticket remains terminal and durably delivered:

- Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- owner key: `agent:main:discord:channel:1391855033993138217`
- status: `completed`
- generation: `0`
- `delivery_confirmed_at`: `2026-09-06T13:50:55.341502+00:00`
- one `cnx_assistant_delivery` row, status `delivered`
- exact idempotency key: `cnxclaw-direct-result:CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a:g0`
- target `ticket_outbox` rows: `0`

No recovery, replay, redelivery, or disposition was performed by Task292.

## Protected owner non-interference

Protected Ticket/session remained distinct and untouched:

- Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner key: `agent:main:discord:channel:1531199905673252946`
- Ticket status: `accepted`
- failure class: `interrupted`
- `delivery_confirmed_at=null`
- `cnx_assistant_delivery` rows: `0`
- `cnx_sessions` state: `active`
- protected CNX generation: `1`
- protected `cnx_sessions.session_id`: `null`

The protected Ticket was read only and was not used as a recreation target.

## Health and scope

Fresh direct probes:

- Gateway `http://127.0.0.1:18789/health`: HTTP `200`, `{"ok":true,"status":"live"}`
- Ollama `http://127.0.0.1:11434/api/tags`: HTTP `200`; `qwen3.5:9b` present
- SQLite integrity: `ok`

`openclaw gateway probe` reported `connected-no-operator-scope` and missing `operator.read` for diagnostics. This is an observability limitation only in Task292: no mutation or operator-admin operation was required or attempted. It must be resolved before any future operation that needs Gateway mutation authority.

## Proposal-only future boundary

A future clean recreation task may be drafted for ChatGPT review, but must separately authorize all of the following:

1. Freshly verify the deleted target key remains absent and the CNX generation-1 tombstone remains unchanged.
2. Define a genuinely new disposable Discord target/session, distinct from the protected owner and all prior sacrificial keys.
3. Require the human to send exactly one benign setup message; Hermes must not send it.
4. Correlate the new OpenClaw key/ID to a new CNX generation and Ticket.
5. Observe read-only until terminal durable delivery, including exact Ticket, generation, delivery, recovery, and outbox rows.
6. Stop at review if delivery is absent or ambiguous; no Delete/reset/replay/redelivery may be inferred.

This is a proposal for a successor task only. No new session was created and no Discord message was sent in Task292.

## Hard-fence ledger

- session creation/recreation: `0`
- `sessions.delete`: `0`
- reset: `0`
- Hermes semantic sends: `0`
- protected Ticket/session mutation: `0`
- manual SQLite/Ticket/session/transcript/config mutation: `0`
- replay/redelivery/disposition: `0`
- installer/install-over/uninstall: `0`
- Gateway/Ollama/service mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Stop boundary

Task292 is complete at the read-only proposal boundary. Publish this report, set coordination to `WAITING_FOR_CHATGPT_REVIEW`, and stop. A future recreation requires a separately named and authorized successor task.
