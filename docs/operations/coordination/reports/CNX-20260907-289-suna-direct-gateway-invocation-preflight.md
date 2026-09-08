# CNX-20260907-289 — Suna Direct Gateway Invocation Preflight

## Disposition

`NEEDS_CHATGPT__DIRECT_PATH_REQUIRES_CREDENTIAL_AND_FENCE_DRIFT__NO_DELETE`

Suna performed only the authorized read-only direct Gateway preflight. No Chat UI input was opened or used, no credential value was displayed/copied/extracted, and no `sessions.delete` or other live mutation was attempted. The preflight cannot hand off to Task290 because both the inherited session fence drifted and the supported direct CLI path requires explicit credential material that is not available through a non-secret selection mechanism.

## Authority and provenance

- task: `CNX-20260907-289-suna-direct-gateway-invocation-preflight.md`
- parent: `CNX-20260907-288`
- executor: `Suna`
- next actor: `ChatGPT` review/authority decision
- branch: `agent/v0.9.3-full-stabilization`
- fresh remote HEAD: `0730dfaf5b27be89024f2e09e6ceba16d7c4ea91`
- installed OpenClaw: `2026.7.1-2` (`0790d9f`)
- fresh observation window: `2026-09-06T23:07:09Z` onward

## Supported direct invocation findings

Fresh installed help for `openclaw gateway call` showed this supported shape:

```text
openclaw gateway call [options] <method>
method: health/status/system-presence/cron.*
--json
--params <json>
--timeout <ms>
--url <url>
--token <token>
--password <password>
```

The command has no device-identity selector, paired-node selector, or non-secret `Windows Node (CDQ-P)` option. A harmless direct call succeeded:

```text
openclaw gateway call health --json --timeout 5000
```

It returned `ok: true`, loaded plugins without errors, and reported Discord configured/running. A harmless `status` call also succeeded. However, `openclaw gateway status` and `probe` continued to report `connected-no-operator-scope` and missing `operator.read` for the current default CLI connection.

The only supported authentication inputs exposed by this direct CLI are `--token`/`--password` (or their environment/config sources). Current environment checks did not provide `OPENCLAW_GATEWAY_TOKEN` or `OPENCLAW_GATEWAY_PASSWORD`. Extracting, displaying, guessing, or copying a paired token/password is forbidden by the task. The Control UI/browser path is explicitly forbidden after the Task288 Chat UI misroute and was not used.

Redacted device metadata still shows the paired `Windows Node (CDQ-P)` entry with roles `operator,node` and scopes `operator.admin,operator.pairing`; this advertises a paired scope but does not give the current CLI connection that scope.

## Fresh inherited-fence re-read

The prior Task287 handoff values were not reused after the direct health/status probe exposed changed session state. Fresh `openclaw sessions list --json` returned:

- target key: `agent:main:discord:channel:1391855033993138217`
- current session ID: `c7a72073-64e4-4c2b-ba83-58f030e6eef0`
- current numeric updatedAt: `1788736576078`
- current status: `failed`
- agent ID: `main`
- kind: `group`
- protected key: `agent:main:discord:channel:1531199905673252946`
- protected session ID: `60bed85d-5b84-4834-84cb-592044f87b1e`
- protected numeric updatedAt: `1788400079344`
- protected status: `done`

The prior handoff used session ID `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2` and updatedAt `1788702655250`; those values are stale and are ineligible for Task290. The target session fence therefore fails closed.

## Durable read-only context

The setup Ticket remained read-only and unchanged in the runtime SQLite database:

- Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- owner key: target key above
- status: `completed`
- response_ready_at: `2026-09-06T13:50:43.243Z`
- delivery_confirmed_at: `2026-09-06T13:50:55.341502+00:00`
- protected Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- protected owner key: protected key above

No database write, transcript write, Ticket mutation, replay, or recovery action was performed.

## Health and host observations

- direct `gateway call health`: `ok: true`
- Gateway service: registered/running; loopback `127.0.0.1:18789`; connectivity `ok`
- Gateway HTTP health: previously fresh read-only probe returned HTTP 200 `{"ok":true,"status":"live"}`
- Ollama HTTP `/api/tags`: previously fresh read-only probe returned HTTP 200 with `qwen3.5:9b` present
- Node service: Scheduled Task `missing`, runtime `stopped`; no install/start/restart attempted

## Hard-fence ledger

- `sessions.delete`: `0`
- reset/cancel substitute: `0`
- semantic sends: `0`
- credential readout/change: `0`
- Ticket/session/SQLite/transcript mutation: `0`
- protected/prior session mutation: `0`
- replay/redelivery: `0`
- installer/release/force push: `0`

## Required decision

Stop at `NEEDS_CHATGPT`. ChatGPT must adjudicate the stale fence and authorize a new exact target/fence plus an approved non-secret direct Gateway client path before any successor Task290. Do not retry the Chat UI, do not use the stale Task287 values, do not guess credentials, and do not call `sessions.delete`.

Actor completed: `Suna`  
Actor next: `ChatGPT` review/authority decision  
Task290 handoff: `NOT AUTHORIZED`  
ChatGPT required: `YES`
