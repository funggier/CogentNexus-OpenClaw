# Review — CNX-20260827-089 Recover and Publish Task-088 Implementation Safely

Decision: `ACCEPT`

Disposition: `ACCEPT_ACTION_RESOLVER_BOUNDARY_PUBLISHED_SAFE`

Reviewed report HEAD:

`ebd6df825f6b84e68edd2ba24869333154be48c6`

Implementation HEAD:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Execution coordination HEAD:

`25d6c673a760cc80ed080990ca1290657f725795`

## Publication fence

Accepted.

Fresh repository verification shows:

- `25d6c673... -> d6daf8f9...` is exactly one implementation commit;
- implementation files are exactly:
  - `scripts/install.ps1`
  - `tests/test_installer_transaction_wiring.py`;
- no file under `plugins/cogentnexus-openclaw/**` changed;
- `d6daf8f9... -> ebd6df82...` is exactly one report-only commit adding the Task-089 report;
- the implementation commit is repository-resolvable and is the direct parent of the report commit.

This closes the publication failure that invalidated Task 088.

## Independent source review

The published `scripts/install.ps1` now uses PowerShell 5.1-safe named hashtable splatting:

```powershell
$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
```

The broken string-token array form containing literal `"-Mode"` is no longer present in this production caller.

The lifecycle resolver itself remains unchanged, preserving the previously reviewed truth table:

- fresh -> install only;
- legacy -> install only;
- ordinary upgrade -> install + rollover;
- pending recovery -> rollover only;
- already exact -> neither;
- SkipPlugin -> neither;
- impossible pending+exact -> fail closed.

## Preserved production rollover structure

Task-086 behavior remains present:

- package creation/installation is under `$actions.installPlugin`;
- upgrade rollover is independently under `$actions.rolloverPlugin`;
- rollover is not nested under `$actions.installPlugin`;
- rollover occurs before strict `resolve-plugin` and ownership publication.

Thus the preserved live pending topology can reach rollover with:

- `installPlugin=false`;
- `rolloverPlugin=true`.

## Regression evidence

Task 089 reports fresh isolated-worktree verification including:

- exact Windows PowerShell 5.1 RED reproduction of the Task-087 array-splat failure against published predecessor source;
- successful named invocation of the real production resolver;
- focused boundary/lifecycle suite: `42 passed`;
- full Python: `374 passed, 2 skipped, 4 subtests passed`;
- Node 24/npm 11: `49 files, 257 tests passed` plus validation/package/bootstrap gates;
- Node 22/npm 12: `49 files, 257 tests passed` plus validation/package/bootstrap gates;
- PowerShell 5.1 syntax and production AST/control-flow regression passed;
- baseline consistency and `git diff --check` passed;
- plugin payload diff remained zero.

Independent review additionally verified the published Git ancestry and resulting source rather than relying on the report token alone.

## Live-state disposition

Task 089 was source/test-only. It did not retry or normalize the live Task-087 state.

The accepted live baseline therefore remains:

- controller PASSTHROUGH generation 13;
- ownership manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement -> `g-7257c4555ca8ad21`;
- exactly two canonical generations;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- no semantic/provider activity from Tasks 087–089.

## Successor authorization

Task 089 releases exact source:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

for one separately fenced supported live recovery attempt.

That successor must re-prove the preserved two-generation topology and exact source fingerprint before mutation, invoke the supported installer exactly once, and stop on any nonzero result without retry.

For the pending path it must prove:

- classification = `upgrade + pendingRollover=true + pluginAlreadyExact=false`;
- lifecycle actions = `installPlugin=false + rolloverPlugin=true`;
- no `npm pack`;
- no npm artifact install;
- no `openclaw plugins install`;
- no third generation;
- existing old generation is retired through reviewed rollover;
- existing source-exact replacement becomes the unique canonical generation.

Only after successful rollover may it continue MANAGED/startup/Supervisor/AGENTS restoration, exact source/live parity, owned-runtime health, five natural PT1M no-flash ticks and read-only authenticated Dashboard/WebChat owner-surface readiness.

Final semantic acceptance remains a separate task and is not authorized by this review.
