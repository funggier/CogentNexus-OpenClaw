# CNX-20260907-287 — Suna Fresh Preflight Handoff

## Disposition

`PASS_PREFLIGHT_HANDOFF_TO_LUNA__CNX-20260907-288_READY`

Suna completed the authorized read-only preflight only. No `sessions.delete` call or other live mutation was made. The immutable values below are handed to Luna for the separately authorized one-shot Task288 operation.

## Authority and provenance

- task: `CNX-20260907-287-use-paired-admin-identity-fenced-delete.md`
- executor: `Suna`
- next executor: `Luna`
- reviewer/escalation: `ChatGPT`
- branch: `agent/v0.9.3-full-stabilization`
- fresh remote HEAD at preflight: `88c15aa508d55699ad1dc5a67474f0f028ad411e`
- fresh preflight observation: `2026-09-06T23:07:09Z` onward
- accepted live candidate in ACTIVE.md: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

## Immutable target fencing values

Fresh `openclaw sessions list --json` returned:

- exact key: `agent:main:discord:channel:1391855033993138217`
- current session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- numeric updatedAt: `1788702655250`
- status: `done`
- agent ID: `main`
- kind: `group`
- `lifecycleRevision`: absent; it was not synthesized

Luna must use exactly these values for Task288 and must omit `expectedLifecycleRevision`.

## Ticket and durable delivery gate

Read-only SQLite inspection used `file:...?...mode=ro` against the live CogentNexus runtime database:

- database: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`
- SQLite integrity check: `ok`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- owner session key: exact target key above
- Ticket status: `completed`
- `response_ready_at`: `2026-09-06T13:50:43.243Z`
- `delivery_confirmed_at`: `2026-09-06T13:50:55.341502+00:00`
- `cnx_assistant_delivery`: 1 row, 1 delivered
- target `ticket_outbox`: 0 rows
- target `cnx_direct_recovery`: `mode=redeliver`, `state=cancelled`, `attempt_count=1`, `owner_generation=0`

A first query attempted nonexistent `tickets.generation`; the actual schema has no such column. The query was corrected to the live schema without mutation; this limitation is recorded rather than inferred away.

## Protected-state exclusion

Fresh read-only inspection confirmed the protected state remained distinct and was not modified:

- protected Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- protected owner key: `agent:main:discord:channel:1531199905673252946`
- protected session entry: session key distinct, `generation=1`, `session_id` absent in `cnx_sessions`
- protected Ticket status: `accepted`
- protected Ticket delivery: 0 `cnx_assistant_delivery` rows
- protected Ticket outbox: 0 rows
- protected recovery: `mode=redeliver`, `state=pending`, `attempt_count=0`, `owner_generation=1`

Luna must not touch this protected Ticket or session.

## Operator-admin and non-WebChat path

Fresh redacted device metadata showed:

- paired display name: `Windows Node (CDQ-P)`
- client ID: `node-host`
- roles: `operator`, `node`
- scopes: `operator.admin`, `operator.pairing`
- credential values were not printed, copied, extracted, rotated, revoked, or changed

The supported path is the local OpenClaw Gateway client over loopback `ws://127.0.0.1:18789`, not WebChat. Fresh `openclaw gateway status`/`probe` showed the Gateway reachable and local connect `ok`; the current default CLI probe reports `connected-no-operator-scope`, but the paired operator-admin identity is the authorized client identity for Luna's Task288 path. No credential material was exposed by Suna.

## Health and host evidence

- Gateway Scheduled Task: registered; runtime `Ready`; connectivity `ok`; Gateway HTTP `/health`: HTTP 200, `{"ok":true,"status":"live"}`
- `openclaw gateway health`: `OK`; Discord configured
- Ollama `/api/tags`: HTTP 200; models included `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`
- OpenClaw Node Scheduled Task: `missing`; runtime `stopped` with `The system cannot find the file specified`; no install/start/restart was attempted

The missing Node host service is recorded as a host observation and does not authorize repair or any alternate client path. Luna must stop if the authorized paired Gateway path cannot be established without new credential material.

## Hard-fence ledger

- `sessions.delete`: `0` (Suna did not call it)
- reset: `0`
- cancel substitute: `0`
- semantic sends: `0`
- credential exposure/change: `0`
- Ticket/session/SQLite/transcript mutation: `0`
- protected/prior session mutation: `0`
- replay/redelivery/disposition: `0`
- installer/release/force push: `0`

## Luna handoff contract

Task288 is now the active successor task. Luna may make at most one supported `sessions.delete` call using only the exact key, session ID, and numeric updatedAt above, with `agentId=main`, `deleteTranscript=true`, `emitLifecycleHooks=true`, `archivedOnly=false`, and no lifecycleRevision field. Any error, timeout, permission failure, fencing mismatch, or `deleted:false` consumes the attempt and requires stop without retry.

Actor completed: `Suna`  
Actor next: `Luna`  
ChatGPT review required after Task288 report: `YES`
