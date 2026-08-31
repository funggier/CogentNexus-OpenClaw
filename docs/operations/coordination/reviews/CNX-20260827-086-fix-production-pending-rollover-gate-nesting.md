# Review — CNX-20260827-086 Fix Production Pending-Rollover Gate Nesting

Decision: `ACCEPT`

Disposition: `ACCEPT_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

Reviewed report HEAD:

`1430d0a23ee2c477fdb5c2015f262c9df09c83df`

Implementation HEAD:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

Execution coordination HEAD:

`08a53963820bd27f8418e66d5a574b12e87bd9f7`

## Publication fence

Accepted.

- `08a53963... -> 71f48c1a...`: exactly one implementation commit.
- Production/source changes are limited to:
  - `scripts/install.ps1`
  - `scripts/analyze-installer-lifecycle-ast.ps1`
  - `tests/test_installer_transaction_wiring.py`
  - `tests/test_namespace_install_contract.py`
- No file under `plugins/cogentnexus-openclaw/**` changed.
- `71f48c1a... -> 1430d0a2...`: exactly one report-only commit adding the Task-086 report.

## Independent source review

The Task-085 blocking nesting defect is corrected in the production script itself.

The package-install block remains guarded by:

`if ($actions.installPlugin)`

and closes before the rollover gate.

The rollover path is now an independent sibling:

`if ($classification.mode -eq "upgrade" -and $actions.rolloverPlugin)`

Therefore the pending-recovery tuple:

- `mode=upgrade`
- `pendingRollover=true`
- `pluginAlreadyExact=false`
- `installPlugin=false`
- `rolloverPlugin=true`

can reach rollover-plan/apply without entering npm-pack/OpenClaw plugin installation.

The rollover block appears before the later strict `resolve-plugin --openclaw-state` ownership-resolution call.

## AST regression quality

The new `scripts/analyze-installer-lifecycle-ast.ps1` parses the real production `scripts/install.ps1` with the PowerShell AST and reports command offsets plus all `IfStatementAst` ancestors.

The focused regression proves:

- rollover-plan/apply commands have a `rolloverPlugin` ancestor;
- rollover-plan/apply commands have no `installPlugin` ancestor;
- npm-pack/OpenClaw plugin-install commands remain under `installPlugin`;
- rollover commands occur before strict `resolve-plugin`.

This directly covers the caller-nesting class missed by Task 085 and does not duplicate lifecycle business logic in the test.

## Preserved predecessor behavior

Independent source inspection confirms Task-085 classification and source-attestation behavior remains present:

- one old generation differing from expected source -> normal upgrade, `pending=false`, `exact=false`;
- one source-exact manifest-owned generation -> `exact=true`;
- explicit expected source fingerprint must equal the active replacement for any attested pending topology;
- generic two-generation resolution remains ambiguous/fail-closed;
- plan/apply still retain inventory, manifest, wrapper, project-tree, source-fingerprint, plan-hash and rollback fences.

## Fresh verification evidence reported by executor

Task 086 reports fresh GREEN evidence from the isolated execution worktree:

- full Python: `373 passed, 2 skipped, 4 subtests passed`;
- Node 24/npm 11: `49 files, 257 tests passed`, validation/package/mixed-plugin/bootstrap gates passed;
- Node 22/npm 12: `49 files, 257 tests passed`, validation/package/mixed-plugin/bootstrap gates passed;
- PowerShell 5.1 syntax and production AST regression passed;
- baseline consistency passed;
- `git diff --check` passed;
- plugin payload diff remained zero.

The review additionally inspected the resulting production source and publication lineage rather than relying on the PASS token alone.

## Live-state disposition

Task 086 was source/test only. The accepted Task-083 live partial state remains deliberately unrepaired:

- controller PASSTHROUGH generation 13;
- manifest-owned prior generation `g-5593cbcfff5b35d5`;
- active disabled source-exact replacement `g-7257c4555ca8ad21`;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent.

No semantic message/provider probe was authorized or reported.

## Successor authorization

Task 086 releases exact source:

`71f48c1a134ee9b2646b4cc7f077abe9cae59ebb`

for one separately fenced supported live recovery attempt against the existing Task-083 two-generation topology.

That live successor must prove before mutation that the current registered replacement still matches the exact candidate-source fingerprint, then invoke the installer exactly once. For the pending path it must prove from execution evidence that:

- `installPlugin=false`;
- `rolloverPlugin=true`;
- no `npm pack` is executed;
- no `openclaw plugins install` is executed;
- no third plugin generation is created;
- the existing old generation is retired through the reviewed rollover mechanism;
- the existing source-exact replacement becomes the unique canonical generation.

Only after successful rollover may it continue normal MANAGED/startup/Supervisor/AGENTS restoration, source/live parity, owned-runtime health, five natural PT1M no-flash ticks and read-only Dashboard/WebChat owner-surface readiness.

Final semantic acceptance remains a separate task and is not authorized by this review.