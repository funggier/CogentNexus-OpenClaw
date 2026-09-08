# CNX-20260904-239 — Rollover-Prepare Failure Diagnostic Preservation TDD Repair

## Authority and boundary

- Task: `CNX-20260904-239`
- Mode: `TASK239_ROLLOVER_PREPARE_FAILURE_DIAGNOSTIC_PRESERVATION_TDD_REPAIR`
- Fresh authority remote before publication: `5393c933fb0ada0136ffd14f99d718076af90631`
- Execution date: `2026-09-04`
- Scope: repository-only TDD repair
- Live installer, plugin, controller, Gateway, provider, Ticket, outbox, recovery, Dashboard, Discord, process, release, tag, asset, and published runtime state were not mutated.

## Baseline RED evidence

The accepted Task-238 source still captured `$prepareOutput` without merging child stderr and discarded it before throwing the generic wrapper error. A test-only commit was created and executed before production edits:

- RED commit before rebase: `15f241d94ca52510f7ce6716eb20879075fbb937`
- Result: `2 failed, 1 passed`
- Failure 1: rollover-prepare invocation did not merge stderr (`2>&1`).
- Failure 2: no bounded diagnostic helper/limit existed.
- The nonzero fail-closed test passed.
- Production source was unchanged at the RED boundary.

## Repair

Only `scripts/install.ps1` was changed in production code. The repair:

1. Captures combined child stdout/stderr for `rollover-prepare` using `2>&1 | Out-String`.
2. Adds `Get-BoundedInstallerDiagnostic` with a 4096-character upper bound.
3. Emits a deterministic placeholder when child output is empty.
4. Preserves the beginning and end of overlong diagnostics with `[child diagnostic truncated]` in between.
5. Includes the bounded child diagnostic in the existing failure message while retaining the original stage, exit-code handling, argument list, ordering, ownership checks, hash attestations, transaction checks, and fail-closed behavior.

The regression test in `tests/test_task239_rollover_diagnostics.py` executes the PowerShell helper against empty, short, and long output; it is not only a source-text assertion.

## Verification

Focused regression and existing observability contract:

```text
6 passed in 0.24s
```

Full repository validation:

```text
508 passed, 5 skipped, 4 subtests passed in 97.90s (0:01:37)
```

Plugin validation:

```text
Test Files  58 passed (58)
Tests       284 passed (284)
evaluation: passed: true
mixed-plugin artifact verification: PASS (45 config properties, 5 tools)
ticket DB bootstrap: PASS (9 required tables + v095 registration fence)
package: openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz
packedFileCount: 196
```

Additional checks:

```text
PowerShell parser: PS_SYNTAX=PASS
git diff --check: PASS
worktree: clean before report publication
```

Final candidate plugin fingerprint, computed after the repair:

```text
1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

This exactly matches the Task-239 authority candidate fingerprint. The repair is installer-source-only and did not alter the candidate plugin payload identity.

## Zero-mutation ledger

- Installer starts/invocations/retries: `0`
- Direct rollover operations: `0`
- Manual plugin/lifecycle/Gateway/managed-state repair: `0`
- Ticket/outbox/recovery/SQLite writes: `0`
- Dashboard/Discord/API semantic sends: `0`
- Semantic replay/resend/recovery replay: `0`
- Provider/model substitution: `0`
- Process termination: `0`
- Reset/uninstall/reinstall: `0`
- Release/tag/asset mutation: `0`
- Force-push/history rewrite: `0`
- Task-237/Task-238 forensic evidence mutation: `0`

## Publication

- Report path: `docs/operations/coordination/reports/CNX-20260904-239-rollover-prepare-failure-diagnostic-preservation-tdd-repair.md`
- Repair commit after rebase: `ec29020632091aae3b50149b51303a36fde26310`
- RED test commit after rebase: `2c5d68384df11e38b9cea5e565c247324c4c5f44`
- No release or runtime requalification was performed.

## Disposition

`PASS_ROLLOVER_PREPARE_DIAGNOSTIC_PRESERVATION_TDD_REPAIRED`

The repository-only diagnostic-preservation repair is verified. Task 238’s historical installer failure remains immutable and un-rerun. Any installer retry, live state repair, exact-candidate install, or requalification requires a separate successor authority.

STOP for independent review.
