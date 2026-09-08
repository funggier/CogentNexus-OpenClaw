# CNX-20260906-283 — Verify Supported OpenClaw Session Delete Boundary

## Disposition

`PASS_SOURCE_BOUNDARY_DEFINED__NO_LIVE_DELETE__WAITING_FOR_CHATGPT_REVIEW`

This report records source/read-only verification of the installed OpenClaw `2026.7.1-2` session deletion boundary. No live `sessions.delete`, reset, semantic send, CNX durable mutation, or transcript mutation was performed.

## Authority and provenance

- coordination branch: `agent/v0.9.3-full-stabilization`
- remote HEAD at preflight: `f0cedbe1f5a48a51ba107bdeb9eaf641a24fd49d`
- active task: `CNX-20260906-283`
- candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- installed OpenClaw version: `2026.7.1-2`
- verification time: `2026-09-06T17:51:56Z` (UTC system timestamp immediately before report publication)

Installed source files and SHA-256:

- `dist/sessions-UcKjjh_n.js`: `be4c2aaf36a763a6e2108c988451f3952053aef3c12f768c5aa4f1ffd8308ee7`
- `dist/schema-BuOFpc7K.js`: `b5b672dd1ce3579e2b030567ef192355374c052934cb4e252b793e08647d54ab`
- `dist/server-methods-NpEcZnvp.js`: `88f1af472efff2845c67922c8d2aabb8e1232c78ce7402b3d431eb8964da592a`
- `dist/control-ui/assets/sessions-page-Bf1UvuWh.js`: `45e21c8b669627a7d8b5b560809b928e930669fbafc1959f0b9064c6abe991ee`

## Verified supported boundary

The installed server method registry includes `sessions.delete` and `sessions.reset` as separate methods. The Control UI session page invokes a bulk client operation `sessions.deleteMany`, after an explicit confirmation, and removes only entries returned in the server response's `deleted` list.

The actual Gateway handler for `sessions.delete` performs, in order:

1. Validate the request against `SessionsDeleteParamsSchema`.
2. Require a non-empty session key.
3. Reject WebChat session mutation unless the client is the Control UI.
4. Resolve the requested agent and canonical/store target.
5. Reject deletion of the main session.
6. Default `deleteTranscript` to `true`.
7. Optionally enforce `archivedOnly:true`.
8. Check expected session identity/lifecycle fields before mutation.
9. Reject a plugin-runtime ownership mismatch.
10. Release/clean up session work through the lifecycle boundary.
11. Re-read and re-check expected identity after cleanup.
12. Call the lifecycle deletion primitive with the expected entry and CAS fields.
13. Emit the gateway session-end plugin hook and session-unbound lifecycle event only when `deleted:true`.
14. Return `{ok:true,key,deleted,archived}`.

The handler's changed-before-delete response is an invalid request with reason `SESSION_LIFECYCLE_CHANGED`; it does not silently select a different session.

## Exact request schema

The installed schema accepts only these fields:

```json
{
  "key": "string",
  "agentId": "string (optional)",
  "deleteTranscript": "boolean (optional)",
  "expectedSessionId": "string (optional)",
  "expectedLifecycleRevision": "string (optional)",
  "expectedSessionUpdatedAt": "number >= 0 (optional)",
  "emitLifecycleHooks": "boolean (optional)",
  "archivedOnly": "boolean (optional)"
}
```

Unknown fields are rejected by the schema. `sessions.reset` accepts only `key`, optional `agentId`, and optional `reason` (`new` or `reset`); it is not a Delete substitute.

## Authorization/client boundary

Installed `method-scopes` logic proves the following:

- `operator.admin` authorizes the method.
- A minimal `operator.write` request is permitted only when `archivedOnly:true` and every field is in the write-safe set: `key`, `agentId`, `deleteTranscript`, `archivedOnly`.
- Any request containing internal fencing controls such as `expectedSessionId`, `expectedLifecycleRevision`, `expectedSessionUpdatedAt`, or `emitLifecycleHooks` requires `operator.admin`.
- A request without `archivedOnly:true` requires `operator.admin`.
- Non-operator or insufficient-scope clients are rejected by the gateway authorization layer.
- WebChat clients are explicitly rejected for session mutation; the Control UI is the supported client exception.

Therefore a future exact-target experiment must use a Control UI/operator-admin-capable Gateway client and include the exact identity/lifecycle fencing values. A bare `cnxclaw.cmd session cancel` invocation is not the supported OpenClaw Delete boundary.

## Exact target observed read-only

Fresh `openclaw sessions list --json` showed:

- key: `agent:main:discord:channel:1391855033993138217`
- session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- status: `done`
- session store count: `9`

Fresh CNX read-only inspection showed:

- Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- Ticket status: `completed`
- `delivery_confirmed_at` present
- one exact owner-generation-0 `cnx_assistant_delivery` row, status `delivered`
- gateway health HTTP `200`, `{"ok":true,"status":"live"}`
- Ollama health HTTP `200`, model `qwen3.5:9b` present
- SQLite `pragma integrity_check`: `ok`

The SQLite schema has no `sessions` table; OpenClaw session identity is held in the OpenClaw session store (`C:\Users\CDQ-P\.openclaw\agents\main\sessions\sessions.json`) and was therefore verified through the supported `openclaw sessions list --json` interface rather than an invented SQL query.

## Bounded future proposal (not authorized by this task)

A separate future task would need to authorize exactly one Gateway `sessions.delete` request bound to a fresh preflight snapshot, with at minimum:

```json
{
  "key": "agent:main:discord:channel:1391855033993138217",
  "agentId": "main",
  "deleteTranscript": true,
  "expectedSessionId": "5438cad2-52b1-4fcf-9145-2d3c65f6ddf2",
  "expectedLifecycleRevision": "<fresh exact value>",
  "expectedSessionUpdatedAt": "<fresh exact numeric value>",
  "emitLifecycleHooks": true,
  "archivedOnly": false
}
```

The placeholders must be replaced only from the same fresh pre-mutation snapshot. If any key, session ID, lifecycle revision, updated timestamp, client authorization, or protected-owner exclusion is ambiguous, the future task must stop without mutation. Post-call readback must require an explicit `deleted:true` result and verify the exact session entry/transcript/lifecycle consequences; `ok:true` alone is insufficient.

This proposal is documentation only. Task283 did not call the method and did not modify live state.

## Hard-fence ledger

- live `sessions.delete`: `0`
- live reset: `0`
- `cnxclaw session cancel` retry: `0`
- Hermes semantic sends: `0`
- protected Ticket/session mutation: `0`
- manual SQLite/Ticket/session/transcript/config mutation: `0`
- recovery replay/redelivery/disposition: `0`
- installer/install-over/uninstall: `0`
- Gateway/Ollama/service mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Evidence and stop boundary

The source inspection was performed against the installed runtime, not inferred from a generic API. Task283 is complete at the source/read-only boundary. Publish this report, verify its remote identity, and stop. No live Delete is authorized by Task283.
