# CNX-20260906-284 — Bounded Disposable OpenClaw Session Delete

## Disposition

`BLOCKED_PREFLIGHT_MISSING_LIFECYCLE_REVISION__NO_LIVE_DELETE__WAITING_FOR_CHATGPT_REVIEW`

Task284 authorized exactly one supported Gateway `sessions.delete` attempt only if every same-run Phase A fence passed. The exact session key, session ID, updatedAt, terminal Ticket, durable delivery, and service health were confirmed. Phase A failed because the fresh OpenClaw session-store entry contains no `lifecycleRevision` field, while Task284 requires an exact fresh lifecycle revision in the fenced request. No live Delete was invoked.

## Authority and execution provenance

- branch: `agent/v0.9.3-full-stabilization`
- preflight remote HEAD: `f90f47f27f1d633fe44588dd9d72fecfd14b0c43`
- active task: `CNX-20260906-284`
- candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- OpenClaw version: `2026.7.1-2` (`0790d9f`)
- preflight time: `2026-09-06T18:02:14Z`
- final classification time: `2026-09-06T18:03:56Z`

## Phase A evidence

### Exact session identity

Fresh `openclaw sessions list --json` returned the exact target:

- key: `agent:main:discord:channel:1391855033993138217`
- session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- status: `done`
- session file: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\5438cad2-52b1-4fcf-9145-2d3c65f6ddf2.jsonl`
- updatedAt: `1788702655250`
- agent ID: `main`
- origin surface: `discord`

The raw session inventory was captured at:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-task284-sessions-before.json`

The session store was read-only inspected at:

`C:\Users\CDQ-P\.openclaw\agents\main\sessions\sessions.json`

The target's complete store entry includes `sessionId` and `updatedAt`, but no `lifecycleRevision` property. The store file SHA-256 at inspection was:

`bfe842f44bdd5c6462928b28a2d7c805c41f3a7b4365d1ef8273d71bb5f28fa6`

This is a required-field absence, not a guessed empty value. Hermes did not synthesize a revision or omit the required fencing field.

### CNX Ticket and delivery

Read-only SQLite inspection showed:

- Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- owner key: `agent:main:discord:channel:1391855033993138217`
- status: `completed`
- lease/lifecycle generation: `0`
- `delivery_confirmed_at`: `2026-09-06T13:50:55.341502+00:00`
- delivery row: exactly one, `direct_result`, status `delivered`
- delivery owner generation: `0`
- exact idempotency key: `cnxclaw-direct-result:CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a:g0`
- ticket outbox rows for target: `0`
- SQLite integrity check: `ok`

The target Ticket is terminal and durably delivered. This does not waive the missing session lifecycle-revision fence.

### Protected owner and health

The protected old Ticket/session remained a distinct owner and was not touched:

- Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner key: `agent:main:discord:channel:1531199905673252946`

Fresh service probes:

- Gateway `http://127.0.0.1:18789/health`: HTTP `200`, `{"ok":true,"status":"live"}`
- Ollama `http://127.0.0.1:11434/api/tags`: HTTP `200`; `qwen3.5:9b` present
- Host/supervisor persisted state was inspected read-only; no recovery or active lifecycle mutation was started

### Authorization boundary

Task284 requires a supported Control UI/operator-admin-capable Gateway path and exact request values including:

- `key`
- `agentId`
- `deleteTranscript`
- `expectedSessionId`
- `expectedLifecycleRevision`
- `expectedSessionUpdatedAt`
- `emitLifecycleHooks`
- `archivedOnly`

The installed source contract confirms internal expected-identity fields are admin-scoped. The fresh runtime entry supplied no `expectedLifecycleRevision`, so the request could not be constructed without violating literal-preservation and fail-closed rules.

## Phase B result

Not attempted.

- `sessions.delete` calls: `0`
- `sessions.reset` calls: `0`
- `cnxclaw session cancel` retries: `0`
- alternate/guessed Gateway calls: `0`

This is a preflight block, not a Delete success or failure. No transcript archive, session removal, lifecycle hook, tombstone, revocation, or generation change was produced.

## Hard-fence ledger

- Delete attempts: `0` (Task284 maximum not consumed because Phase A failed)
- reset attempts: `0`
- Hermes semantic sends: `0`
- protected Ticket/session mutation: `0`
- prior sacrificial session mutation: `0`
- manual SQLite/Ticket/session/transcript/config mutation: `0`
- replay/redelivery/disposition: `0`
- installer/install-over/uninstall: `0`
- Gateway/Ollama/service mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Required successor clarification

A successor task must define how the installed OpenClaw runtime exposes the lifecycle revision for this exact session, or explicitly authorize a different supported fencing strategy after source review. It must not invent an empty revision, reuse a stale value, omit the field, or spend the one-shot Delete attempt without a complete fresh fence.

Task284 therefore stops at the mandatory preflight gate with no live mutation.
