# CNX-20260827-089 — Recover and Publish Task-088 Implementation Safely

Result: `PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

## Scope and authorization

Task 089 was executed as source/test-only under authorization `TASK0...ZED`.

Fresh evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T011020Z`

Execution HEAD:

`25d6c673a760cc80ed080990ca1290657f725795`

Task-088 report and REWORK review were verified as ancestors of the execution HEAD. The reported Task-088 implementation object `93854acb3e4fae63abcd52ac85799a77d67498c6` was not available in the fresh/local Git object database, so the repair was recreated through fresh RED/GREEN rather than pushed from detached side history.

No live installer, install-over, uninstall, reset, cleanup, generation mutation, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session mutation, semantic message, Dashboard/WebChat/CLI send, direct Ollama probe, provider/model/timeout change, restart, reboot, merge, tag, release or force-push was performed by Task 089.

## RED — published source reproduces blocker

Using Windows PowerShell 5.1 and the real production resolver:

```powershell
$actionArgs=@('-Mode','upgrade')
$actionArgs += '-PendingRollover'
& $resolver @actionArgs
```

Observed:

```text
exit code: 1
Cannot validate argument on parameter 'Mode'.
The argument "-Mode" does not belong to the set "fresh,legacy,upgrade" specified by the ValidateSet attribute.
FullyQualifiedErrorId: ParameterArgumentValidationError
```

The direct correct named invocation succeeded and returned the pending action row:

```json
{"mode":"upgrade","pendingRollover":true,"pluginAlreadyExact":false,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":true}
```

Evidence files:

- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T011020Z\red.txt`
- `C:\Users\CDQ-P\AppData\Local\Temp\cnx-next-20260827T011020Z\named.txt`

## GREEN — recreated minimal repair

`scripts/install.ps1` now uses named hashtable transport compatible with Windows PowerShell 5.1:

```powershell
$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

The resolver business logic and truth table were unchanged. Task-086 sibling install/rollover gates and ordering were preserved. No broad installer refactor was made.

A production-boundary regression was added to `tests/test_installer_transaction_wiring.py`, proving against actual `install.ps1` source that:

- named hashtable transport is used;
- no string-token array remains for action resolver invocation;
- named `Mode`, `PendingRollover`, `PluginAlreadyExact` and `SkipPlugin` keys are present;
- the resolver output remains consumed through `$actions.installPlugin` and `$actions.rolloverPlugin`;
- Task-086 AST invariants remain intact.

## Verification

Focused boundary and preserved lifecycle suite:

`42 passed`

Full Python suite:

`374 passed, 2 skipped, 4 subtests passed in 65.88s`

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

No file under `plugins/cogentnexus-openclaw/**` was changed relative to the accepted Task-086 source `71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`.

Final check:

`plugin_payload_diff=zero`

No version bump was made.

## Publication verification

Implementation was committed and pushed before this report.

Implementation commit:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Fresh repository compare from execution HEAD to implementation contained exactly:

```text
M scripts/install.ps1
M tests/test_installer_transaction_wiring.py
```

No other file and no plugin payload path was included.

This report is the only file in the subsequent report-only commit. The implementation-to-report compare was verified after publication.

## Live preservation

Task 089 performed no live-changing operation. The accepted Task-087 two-generation PASSTHROUGH topology was not normalized or retried. No Task-089 semantic/provider activity occurred.

## Final result and successor fence

`PASS_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

This result makes the repaired source eligible for independent acceptance. It does not itself authorize another live recovery attempt. Only independent acceptance of this exact published implementation may authorize one further supported live recovery attempt against the preserved two-generation topology, with fresh read-only preflight and the one-shot/no-retry rule.
