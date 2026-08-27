# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_SUPPORTED_PENDING_ROLLOVER_RECOVERY_RETRY`
Current authorization: `ONE_SUPPORTED_PENDING_RECOVERY_RETRY_AFTER_PUBLISHED_FIX_AUTHORIZED`
Task ID: `CNX-20260827-090`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md`](tasks/CNX-20260827-090-live-pending-rollover-recovery-retry-after-published-boundary-fix.md)

## Task 089 acceptance

Task 089 reported:

`PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

Implementation HEAD:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Report HEAD:

`ebd6df825f6b84e68edd2ba24869333154be48c6`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

Review path:

[`reviews/CNX-20260827-089-recover-and-publish-task088-implementation.md`](reviews/CNX-20260827-089-recover-and-publish-task088-implementation.md)

Publication fence is accepted:

- execution `25d6c673...` -> implementation `d6daf8f9...`: exactly `scripts/install.ps1` + focused test;
- implementation -> report: exactly one report-only commit;
- implementation is repository-resolvable and in direct ancestry;
- no plugin payload source changed.

## Accepted action-resolver repair

Production `scripts/install.ps1` now uses PowerShell-5.1-safe named hashtable splatting for the lifecycle resolver:

```powershell
$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

The Task-087 literal `"-Mode"` array-splat failure is removed from accepted source.

Task-086 production control flow remains:

- package install under `installPlugin`;
- rollover independently under `rolloverPlugin`;
- rollover not nested under `installPlugin`;
- rollover before strict `resolve-plugin`.

## Current live baseline

Preserve the Task-087 fail-closed topology until Task 090 mutates it through the one authorized supported installer invocation:

- controller PASSTHROUGH generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- ownership manifest -> prior `g-5593cbcfff5b35d5`;
- prior fingerprint `7e9189f8...`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- replacement/source fingerprint `8fd911e3...`;
- exactly two canonical generations;
- no third generation;
- Gateway healthy from accepted evidence;
- SQLite integrity accepted, Tickets/outbox zero;
- no semantic/provider activity.

Do not manually normalize this topology.

## Task 090 requirements

Use exact source:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Before mutation re-prove:

- exact two-generation topology;
- replacement fingerprint == exact source fingerprint;
- `mode=upgrade`;
- `pendingRollover=true`;
- `pluginAlreadyExact=false`;
- `installPlugin=false`;
- `rolloverPlugin=true`;
- named action-resolver boundary no longer reproduces `Mode="-Mode"`.

Exactly one supported installer invocation is authorized. Retry count must remain zero.

The pending path must prove:

- no `npm pack`;
- no artifact selection/install;
- no `openclaw plugins install`;
- no third generation;
- reviewed rollover-plan/apply retires prior generation;
- canonical generations converge `2 -> 1`;
- surviving generation is the existing source-exact replacement.

After successful rollover the supported installer must restore:

- MANAGED;
- startup;
- Supervisor;
- AGENTS managed block;
- exact ownership/runtime bindings;
- source/live plugin+skill parity;
- Gateway/Ollama/SQLite health.

Then observe at least five natural PT1M ticks and require:

`NO_FLASH_MULTI_TICK_PROVEN`

Finally prove read-only:

`DASHBOARD_OWNER_SURFACE_READY`

without sending any semantic message.

## Hard semantic/mutation fence

Outside the one supported installer invocation: no uninstall/reset/manual cleanup/manual rollover/manual plugin mutation, no manual controller/startup/Supervisor/AGENTS/ownership/config/runtime repair, no SQLite/Ticket/session mutation, no Dashboard/WebChat send, `chat.send`, `openclaw agent`, `sessions_send`, channel send, direct Ollama probe, provider/model/timeout change, restart/reboot, merge/tag/release.

Any nonzero installer result must stop the task without retry.

## Successor gate

Only independent acceptance of:

`PASS_LIVE_PENDING_RECOVERY_PARITY_NO_FLASH_OWNER_SURFACE_READY`

may authorize the final one-message authenticated Dashboard/WebChat semantic acceptance task.
