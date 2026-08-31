# CNX-20260827-086 — Fix Production Pending-Rollover Gate Nesting

Result: `PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

## Execution and scope

Task 086 was executed as source/test-only under the explicit coordination authorization `TASK0...ZED`.

Fresh evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-state-20260827T000829Z`

Fresh coordination execution HEAD:

`08a53963820bd27f8418e66d5a574b12e87bd9f7`

Task-085 implementation base was present and ancestry-verified:

`6b5c9d56a48d4affe67c2bb718898378edee6e8a`

Task-085 report and review were present and ancestry-verified. The worktree was clean before editing.

No file under `plugins/cogentnexus-openclaw/**` was modified.

## RED — real production AST against Task-085

The Task-085 production script was extracted from the exact base and analyzed with PowerShell `System.Management.Automation.Language.Parser` and AST ancestor traversal.

Evidence:

- rollover commands found: `3`
- rollover commands descended from an `if` depending on `$actions.installPlugin`: `true`
- exact RED reason: `rollover is nested under installPlugin gate`

This reproduced the independent review finding against the real production script rather than only testing the lifecycle helper.

The RED did not result from parser/setup failure.

## GREEN — minimal production correction

Changed production structure in `scripts/install.ps1` from the Task-085 effective shape:

```powershell
if ($actions.installPlugin) {
    # package install
    if ($classification.mode -eq "upgrade") {
        if ($actions.rolloverPlugin) {
            # rollover
        }
    }
}
```

to independent sibling action gates:

```powershell
if ($actions.installPlugin) {
    # candidate npm-pack / OpenClaw plugin install / disable
}

if ($classification.mode -eq "upgrade" -and $actions.rolloverPlugin) {
    # rollover-plan / rollover-apply
}
```

The package-install block remains controlled by `$actions.installPlugin`. The rollover implementation is not duplicated and is now controlled independently by `$actions.rolloverPlugin`.

The existing Ticket DB bootstrap remains outside the package-install gate as accepted by Task 085.

Added the focused production AST helper:

`scripts/analyze-installer-lifecycle-ast.ps1`

It parses the actual installer, locates package install, rollover-plan/apply and strict resolve-plugin commands, and reports their `IfStatementAst` ancestors and source offsets.

Updated the existing installer contract expectation to assert the new sibling gate.

## GREEN AST and ordering evidence

Against the corrected real `scripts/install.ps1`:

- rollover-plan/apply commands are descendants of a condition containing `$actions.rolloverPlugin`;
- rollover-plan/apply commands are not descendants of any condition depending on `$actions.installPlugin`;
- npm-pack/OpenClaw plugin-install operations remain descendants of `$actions.installPlugin`;
- rollover-plan/apply precedes the later strict `resolve-plugin --openclaw-state` call;
- PowerShell AST parser completed successfully;
- PowerShell 5.1 syntax completed successfully.

The production action resolver remains the single lifecycle truth table:

| mode | pending | exact | installPlugin | rolloverPlugin |
|---|---:|---:|---:|---:|
| fresh | false | false | true | false |
| legacy | false | false | true | false |
| upgrade | false | false | true | true |
| upgrade | true | false | false | true |
| upgrade | false | true | false | false |
| any | SkipPlugin | any | false | false |

The impossible `pending=true + exact=true` state remains rejected.

Therefore:

- pending recovery reaches rollover with `installPlugin=false`;
- ordinary upgrade performs package installation first, then rollover;
- already-exact performs neither;
- fresh/legacy preserve plugin creation and do not enter upgrade rollover;
- pending rollover completes before strict unique resolution and ownership publication.

## Regression verification

Full Python suite:

`373 passed, 2 skipped, 4 subtests passed`

This includes Task-084/085 classification, attestation, namespace, ownership, installer, recovery, transaction, semantic/delivery/security and npm-pack boundary tests plus the new production AST test.

Baseline:

`CogentNexus-OpenClaw v0.9.3 baseline consistency: PASS (Bridge v0.9.3)`

Python compile:

`pass`

`git diff --check`:

`pass`

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

### PowerShell 5.1

- `install.ps1` syntax: passed
- `analyze-installer-lifecycle-ast.ps1` syntax: passed
- production AST nesting/order regression: passed

## Payload preservation

Final diff verification reported:

`plugin_payload_diff=zero`

No file under:

`plugins/cogentnexus-openclaw/**`

changed relative to the Task-085 base.

Implementation files are limited to:

- `scripts/install.ps1`
- `scripts/analyze-installer-lifecycle-ast.ps1`
- `tests/test_installer_transaction_wiring.py`
- `tests/test_namespace_install_contract.py`

No version bump was made.

## Live preservation

No live installer, install-over, uninstall, reset, cleanup, plugin-generation mutation, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session mutation, semantic message, Dashboard/WebChat/CLI send, direct Ollama probe, provider/model/timeout change, restart, reboot, merge, tag or release was performed.

Final read-only live snapshot:

- controller: `passthrough`
- controller generation: `13`
- controller SHA-256: `84684c86e2af0653062a6ea27e283b8a4d188cf5f50de2049747f57df035558f`
- ownership manifest remains bound to prior generation `g-5593cbcfff5b35d5`
- ownership manifest SHA-256: `3428c74b9f51389de7a1934630102896bae90c060b2b65e51fd2dbc1380b3bed`
- AGENTS managed markers: `0`
- installer/apply concurrent process: `0`
- live mutation by Task 086: `0`
- semantic/provider activity by Task 086: `0`

The accepted Task-083 two-generation PASSTHROUGH topology was deliberately not normalized.

## Publication fence

Implementation commit:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Report-only commit:

The single subsequent report-only commit containing this file; its exact hash is recorded by the publication verification below.

Only this file is to be included in the report-only commit:

`docs/operations/coordination/reports/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`

Final disposition:

`PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Only the next independently authorized live-recovery task may invoke the supported installer once against the preserved Task-083 topology. That task must prove exact source/live parity, complete pending rollover without npm-pack/plugin install or a third generation, restore MANAGED/startup/Supervisor/AGENTS, prove health/parity, observe five natural no-flash ticks, and prove Dashboard/WebChat owner-surface readiness without semantic messages.
