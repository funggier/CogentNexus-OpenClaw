# CNX-20260906-285 — Fenced Delete Without Optional Lifecycle Revision

## Disposition

`BLOCKED_PREFLIGHT_GATEWAY_CLIENT_MISSING_OPERATOR_ADMIN__NO_LIVE_DELETE__WAITING_FOR_CHATGPT_REVIEW`

Task285 authorized one supported Gateway `sessions.delete` attempt only after all same-run preflight gates passed. The exact target identity and available fencing fields passed, but the authenticated Gateway client exposed by the installed CLI is `connected-no-operator-scope`; there is no evidence of the required `operator.admin` capability. Hermes therefore did not invoke `sessions.delete`.

## Authority and provenance

- branch: `agent/v0.9.3-full-stabilization`
- preflight remote HEAD: `56cb07b73e6e31aa7b7bb6f0cbe12399913e2ad4`
- active task: `CNX-20260906-285`
- candidate SHA: `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`
- installed OpenClaw: `2026.7.1-2` (`0790d9f`)
- preflight time: `2026-09-06T18:13:48Z`
- classification time: `2026-09-06T18:14:53Z`

## Phase A results

### Identity and fencing

Fresh `openclaw sessions list --json` returned:

- key: `agent:main:discord:channel:1391855033993138217`
- session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- status: `done`
- numeric updatedAt: `1788702655250`
- agent ID: `main`
- session store: `C:\Users\CDQ-P\.openclaw\agents\main\sessions\sessions.json`

The fresh session-store entry has no `lifecycleRevision` property. Per Task285, Hermes did not synthesize or send that optional field. The exact permitted fencing values were therefore:

```json
{
  "expectedSessionId": "5438cad2-52b1-4fcf-9145-2d3c65f6ddf2",
  "expectedSessionUpdatedAt": 1788702655250
}
```

### Ticket and durable delivery

Fresh read-only SQLite inspection showed:

- Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- owner session key: `agent:main:discord:channel:1391855033993138217`
- status: `completed`
- generation: `0`
- `delivery_confirmed_at`: `2026-09-06T13:50:55.341502+00:00`
- one owner-generation-0 `cnx_assistant_delivery` row, status `delivered`
- exact idempotency key: `cnxclaw-direct-result:CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a:g0`
- target outbox rows: `0`
- SQLite integrity: `ok`

### Protected state and health

The protected owner remained distinct and was inspected without mutation:

- protected Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- protected owner key: `agent:main:discord:channel:1531199905673252946`

Fresh health probes returned:

- Gateway HTTP health: `200`, `{"ok":true,"status":"live"}`
- Ollama HTTP health: `200`; `qwen3.5:9b` present
- installed host/supervisor state was read-only inspected

### Gateway authorization blocker

Fresh installed CLI output from `openclaw gateway probe` and `openclaw gateway status` reported:

- `Reachable: yes`
- `Capability: connected-no-operator-scope`
- local loopback connect: `ok`
- read probe: `limited - missing scope: operator.read`
- warning: read-probe diagnostics are limited by gateway scopes

Task285 requires an operator-admin-capable Gateway path. The installed source authorization contract also confirms that requests carrying `expectedSessionId` and `expectedSessionUpdatedAt` are internal fencing requests and require `operator.admin`; `operator.write` is insufficient for this request shape. The available client did not prove `operator.admin`, so Phase A item 6 failed.

Hermes did not inspect, print, or retain any credential. It did not guess a token/password, did not alter configuration, and did not retry with another client.

## Phase B result

Not attempted.

- Gateway `sessions.delete` calls: `0`
- reset calls: `0`
- `cnxclaw.cmd session cancel` retries: `0`
- WebChat or guessed CLI calls: `0`

This is a preflight permission block, not a Delete success/failure. No session, transcript, lifecycle, Ticket, or recovery state changed.

## Hard-fence ledger

- Delete attempts: `0` (one-shot authorization not consumed)
- reset attempts: `0`
- cancel substitute/retry: `0`
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

A successor task or operator-authorized setup must provide a supported non-WebChat Gateway client whose connection is provably `operator.admin` before retrying the one-shot Delete. Credential values must remain redacted. The future request must use the same-run exact key, session ID, and updatedAt, omit lifecycleRevision, and require explicit `deleted:true` plus post-readback. No Delete attempt was spent by this task.
