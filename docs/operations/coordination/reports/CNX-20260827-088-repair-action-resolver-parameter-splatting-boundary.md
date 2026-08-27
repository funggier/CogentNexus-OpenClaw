# CNX-20260827-088 — Repair Action-Resolver Parameter-Splatting Boundary

Result: `PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`

## Execution and scope

Task 088 was executed as source/test-only under authorization `TASK0...ZED`.

Fresh evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T003854Z`

Coordination execution HEAD:

`08f748965450e1ab9e77de8ead9fcd3c2e726fb0`

Task-087 blocker report and accepted review were ancestry-verified. A clean isolated worktree was created from the current coordination HEAD.

No live installer, install-over, uninstall, reset, cleanup, generation mutation, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session mutation, semantic message, Dashboard/WebChat/CLI send, direct Ollama probe, provider/model/timeout change, restart, reboot, merge, tag or release was performed by Task 088.

## RED — exact PowerShell 5.1 array-splat failure

Against the accepted Task-086 source behavior, the production-shaped caller was reproduced locally using the real production resolver:

```powershell
$actionArgs=@('-Mode','upgrade')
if ($pendingRollover) { $actionArgs += '-PendingRollover' }
& $resolver @actionArgs
```

Required pending tuple:

```text
mode=upgrade
pendingRollover=true
pluginAlreadyExact=false
SkipPlugin=false
```

Observed result:

```text
exit code: 1
Cannot validate argument on parameter 'Mode'.
The argument "-Mode" does not belong to the set "fresh,legacy,upgrade" specified by the ValidateSet attribute.
FullyQualifiedErrorId: ParameterArgumentValidationError
```

This RED reproduced the exact Task-087 blocker without using live OpenClaw state.

The resolver itself was then called through correct named-parameter hashtable splatting:

```powershell
$args=@{ Mode='upgrade'; PendingRollover=$true }
& $resolver @args
```

Observed result:

```json
{"mode":"upgrade","pendingRollover":true,"pluginAlreadyExact":false,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":true}
```

This isolated the defect to caller argument transport rather than resolver business logic.

## GREEN — minimal production fix

`scripts/install.ps1` now uses a PowerShell-5.1-safe named-parameter hashtable:

```powershell
$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

The resolver truth table was not changed. No literal `"-Mode"` string token is passed through an array. No broad installer refactor was made.

## Boundary regression coverage

Added production-boundary assertions against the actual `scripts/install.ps1` source proving:

- the caller uses a named hashtable;
- `Mode` is assigned as a named key;
- switch values are assigned as named keys;
- no string-token array is used for resolver invocation;
- the same `$actions.installPlugin` and `$actions.rolloverPlugin` outputs remain consumed;
- the Task-086 production AST helper still proves package install remains install-gated;
- rollover remains a sibling gate under `$actions.rolloverPlugin`;
- rollover has no `$actions.installPlugin` ancestor;
- rollover precedes strict `resolve-plugin`.

The existing executable action truth-table coverage was preserved for:

- fresh;
- legacy;
- ordinary upgrade;
- pending recovery;
- already exact;
- SkipPlugin;
- impossible pending+exact.

## Verification

Focused Task-088 boundary and preserved rollover/classification suite:

`42 passed`

Full Python suite:

`374 passed, 2 skipped, 4 subtests passed`

Baseline:

`CogentNexus-OpenClaw v0.9.3 baseline consistency: PASS (Bridge v0.9.3)`

Python compile: passed.

`git diff --check`: passed.

PowerShell 5.1 syntax:

`PS51_SYNTAX_PASS`

Production AST/control-flow regression: passed.

### Node 24 / npm 11

- clean `npm ci`: passed
- full plugin suite: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- mixed-plugin artifact verification: passed
- Ticket DB bootstrap: passed
- package contents: `176` files

### Node 22 / npm 12

- clean `npm ci`: passed
- full plugin suite: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- mixed-plugin artifact verification: passed
- Ticket DB bootstrap: passed
- package contents: `176` files

## Payload preservation

No file under:

`plugins/cogentnexus-openclaw/**`

was modified relative to exact Task-086 source `71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`.

Final check:

`plugin_payload_diff=zero`

Implementation files:

- `scripts/install.ps1`
- `tests/test_installer_transaction_wiring.py`

No version bump was made.

## Live preservation

Task 088 performed no live-changing operation. The preserved Task-087 post-failure topology was not normalized or retried.

Read-only live snapshot retained from the accepted Task-087 post-failure evidence:

- controller: `passthrough`, generation `13`;
- controller SHA-256: `84684c86e2af0653062a6ea27e283b8a4d188cf5f50de2049747f57df035558f`;
- ownership manifest remains bound to prior `g-5593cbcfff5b35d5`;
- ownership manifest SHA-256: `3428c74b9f51389de7a1934630102896bae90c060b2b65e51fd2dbc1380b3bed`;
- active replacement remains `g-7257c4555ca8ad21` and disabled;
- canonical generations remain `2`;
- AGENTS managed markers remain `0`;
- Supervisor remains absent;
- Gateway remains healthy from accepted evidence;
- no Task-088 semantic/provider activity.

## Mutation accounting

- Task-088 live installer invocations: `0`
- Task-088 installer retries: `0`
- Task-088 manual repair/cleanup/rollover: `0`
- Task-088 live generation mutation: `0`
- Task-088 controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session mutation: `0`
- Task-088 semantic messages: `0`
- Task-088 Dashboard/WebChat/CLI sends: `0`
- Task-088 direct Ollama/provider probes: `0`
- Task-088 provider/model/timeout changes: `0`
- Task-088 restart/reboot: `0`

## Publication fence

Implementation commit:

`93854acb3e4fae63abcd52ac85799a77d67498c6`

The implementation commit contains only the production caller fix and focused tests. It contains no coordination report and no plugin payload changes.

The report-only commit following this implementation commit contains only:

`docs/operations/coordination/reports/CNX-20260827-088-repair-action-resolver-parameter-splatting-boundary.md`

Final result token:

`PASS_ACTION_RESOLVER_PARAMETER_BOUNDARY_REPAIRED`

Only an independently accepted successor task may authorize another single supported live recovery attempt against the preserved two-generation topology. That attempt must use the exact accepted Task-088 source, re-prove baseline, invoke the supported installer exactly once, and stop/report on any nonzero result.
