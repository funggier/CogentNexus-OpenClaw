# CNX-356 — Effective Admission Boundary Feasibility Report

## Classification

`UNRESOLVED / BLOCKED`

The installed OpenClaw Gateway does not advertise `hooks.status` in its supported Gateway-call method surface. Per the task decision rule, no `hooks.status` invocation was attempted and no repair or replacement diagnostic was implemented.

## Authority and exact SHAs

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-356-effective-admission-boundary-feasibility`
- Starting remote HEAD: `805ba323c904c4d90a0c5e0923fe9628334085d1`
- Starting HEAD verified as the requested SHA: yes
- Starting HEAD descends from current `origin/main`: yes
- `origin/main` at observation: `ffbfb4c9bdef4bbde81a5bef9078f9b05f6d8c57`
- Branch/main merge-base: `ffbfb4c9bdef4bbde81a5bef9078f9b05f6d8c57`
- Task file: `docs/operations/coordination/tasks/CNX-20260915-356-effective-admission-boundary-feasibility.md`

The branch was observed with unrelated local drift in the operator checkout; the report was prepared in a clean detached worktree at the exact starting remote SHA. No unrelated files were included.

## Installed Gateway/process identity

Fresh read-only supported CLI observations:

- Installed OpenClaw CLI/Gateway version: `2026.7.1-2`
- Build identifier: `0790d9f`
- Gateway service: Scheduled Task, registered
- Gateway command identity: `C:\Program Files\nodejs\node.exe C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`
- Gateway bind: loopback `127.0.0.1:18789`
- Gateway PID reported by `openclaw gateway status`: `17080`
- Runtime state: `Ready`
- Connectivity probe: `ok`
- Health probe: `ok: true`
- Loaded plugin list from health included `cogentnexus-openclaw`; health reported no plugin errors.
- Gateway lifecycle action: none; no restart, stop, start, or reload was performed.

The process identity and health observations are coarse runtime evidence only; they do not establish hook registry membership.

## Supported Gateway method inventory relevant to this probe

The installed supported command surface was read from:

```text
openclaw.cmd gateway call --help
```

The installed help advertises:

```text
method: health/status/system-presence/cron.*
```

It also exposes the supported call options `--json`, `--params <json>`, `--timeout <ms>`, `--url <url>`, and credential-bearing options. Credential options were not used or inspected.

Therefore, `hooks.status` is **not advertised as a supported method** by the installed Gateway CLI. No undocumented method probing was performed.

## `hooks.status` result

- Installed Gateway advertises `hooks.status`: **no**
- `hooks.status` invoked: **no**, because it was not in the supported method inventory
- Live hook registry result: unavailable
- CogentNexus `before_agent_run` live membership: not proven
- pluginId/source/hook key/events/loadable/enabled/filePath/handlerPath: not available from this supported surface
- priority: not assessed and not inferred
- CNX-344 causality: not assessed and not inferred

The source-level existence of a `hooks.status` handler is not runtime evidence for this installed Gateway and does not change this classification.

## Evidence boundary

The health response directly established only that the Gateway was healthy and that the plugin ID `cogentnexus-openclaw` was loaded without reported plugin errors. It did **not** expose the effective `registry.hooks` contents, hook registration fields, handler identity, or priority. Consequently, the CNX-355 Level-3 effective hook-membership gap remains open.

## No-secret accounting

- No credential, token, password, or secret value was read, copied, printed, persisted, guessed, or supplied.
- The health output was used only for the redacted facts recorded above; credential-bearing fields were not retained in this report.
- No session, transcript, Ticket, SQLite, delivery, provider, model, routing, or authentication state was read or mutated.

## Hard-fence accounting

- CogentNexus production source changes: `0`
- OpenClaw source changes: `0`
- New Gateway methods/instrumentation: `0`
- Permission/scope changes: `0`
- Gateway lifecycle changes: `0`
- Plugin install/enable/disable changes: `0`
- Provider/model/auth/routing changes: `0`
- Semantic Dashboard/provider requests: `0`
- CNX-344 replay/resend: `0`
- Ticket/SQLite/session/transcript/delivery mutations: `0`
- v0.9.5 tag/history changes: `0`
- Force-pushes: `0`

## Changed paths

Only this report is intended to be published:

```text
docs/operations/coordination/reports/CNX-20260915-356-effective-admission-boundary-feasibility-report.md
```

## Next authority

Stop for independent ChatGPT review. A future task would require explicit authority to use an already-supported authenticated observability path if one becomes available; this spike does not implement a replacement diagnostic or repair.
