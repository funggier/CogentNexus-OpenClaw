# CNX-20260904-239 — Rollover-Prepare Failure Diagnostic Preservation TDD Repair

Status: `READY_FOR_HERMES`
Executor: Hermes / authenticated repository operator
Coordinator / independent reviewer: ChatGPT
Parent task: `CNX-20260904-238`
Installer-failure parent: `CNX-20260904-237`
Repository/TDD parent: `CNX-20260903-235`
Installer safety / attestation repair parent: `CNX-20260902-226`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT

## Authority

Task-238 final disposition:

`BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`

Task-238 observability classification:

`OBSERVABILITY_DEFECT_PROVEN`

Independent Task-238 review verdict:

`ACCEPT_BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN__OBSERVABILITY_DEFECT_PROVEN__TDD_OBSERVABILITY_REPAIR_REQUIRED`

Accepted product candidate entering this task:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected plugin payload fingerprint entering this task:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Do not assume the fingerprint remains unchanged after Task 239; compute it from the final candidate and explain whether the installer-only source edit is or is not inside the plugin payload identity contract.

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Preserved live boundary

Task 239 is repository-only. The live Windows boundary from Task 238 must not be normalized or mutated:

```text
controller = passthrough
generation = 39
Gateway = healthy
provider = ollama
Delivery = READY / pending 0
Recovery = READY
SQLite integrity = ok
candidate plugin = not installed
predecessor plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Fresh read-only evidence may be observed if needed, but no live product mutation is authorized.

## Objective

Repair only the proven installer observability defect that caused Task 237 to retain the generic wrapper failure while losing the actionable Python `rollover-prepare` child diagnostic.

The repair must preserve enough bounded diagnostic information to identify the failing Python invariant on a future authorized run while leaving all rollover, ownership, installer, retry and fail-closed semantics unchanged.

This task is **not** authorized to discover the missing Task-237 runtime exception by rerunning the operation.

## Proven defect

Current candidate behavior is effectively:

```powershell
$prepareOutput = (& python ... "rollover-prepare" ... | Out-String)
$rolloverPrepareExit = $LASTEXITCODE
Complete-InstallerDiagnosticStage ... -ExitCode $rolloverPrepareExit
if ($rolloverPrepareExit -ne 0) {
    throw "ownership-safe plugin generation rollover pre-install proof failed"
}
```

This loses diagnostic evidence because:

1. captured `$prepareOutput` is not emitted/persisted in the nonzero path;
2. stderr is not merged with stdout, so Python traceback/error output written to stderr may not enter `$prepareOutput` at all.

A working same-file reference already exists in `recovery-preflight`, which uses `2>&1 | Out-String` and includes the captured child diagnostic in its fail-closed error.

## Hard fences

### Authorized repository work

- fresh GitHub/source/Actions reads;
- disposable clone/worktree at current authoritative branch HEAD;
- tests and test fixtures;
- production edit limited to installer diagnostic preservation if RED proves it;
- minimal helper only if required to bound/redact diagnostics consistently;
- focused and full validation;
- commit/push normal fast-forward commits to the working branch;
- Task-239 report publication.

### Not authorized

```text
live installer registration/start/invocation: 0
live rollover-prepare/finalize calls: 0
manual plugin lifecycle mutation: 0
manual managed re-enable/lifecycle/Gateway repair: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
Task-237 orphan-backup cleanup/mutation: 0
Task-223/Task-233 evidence mutation: 0
reset/uninstall/reinstall: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

No live repair is permitted even if repository tests pass.

## Phase A — fresh authority and exact baseline

Before editing:

1. fresh-fetch branch HEAD, `ACTIVE.md`, `STATUS.md`, Task-238 report/review;
2. confirm Task 239 remains active and unsuperseded;
3. confirm accepted predecessor product source is still `ffb0dd4...` with only reviewed coordination drift after it;
4. confirm public `v0.9.3` unchanged;
5. inspect exact current `scripts/install.ps1` and existing `tests/test_installer_observability_contract.py`;
6. identify the smallest production surface that can preserve the child diagnostic without changing execution order or exit semantics.

If unexpected product/source/test/workflow drift exists before Task-239 work, stop and report `BLOCKED_PREFLIGHT_DRIFT`.

## Phase B — meaningful RED first

Use TDD strictly: test-only commit first, then verify the test fails for the intended missing behavior.

The RED must prove, at minimum, that a nonzero `plugin-rollover-prepare` child failure cannot currently preserve the actionable child diagnostic required for postmortem analysis.

The regression should cover both diagnostic channels where practical:

- child stdout marker;
- child stderr marker / Python-style error marker;
- nonzero child exit remains nonzero/fail-closed;
- generic installer failure still exists but must no longer be the only retained diagnostic.

Prefer a production-shaped behavioral harness around the relevant installer fragment or PowerShell execution boundary. A static contract assertion may supplement it but must not be the sole proof if a reliable behavioral harness is feasible.

Required RED properties:

```text
RED commit changes tests/fixtures only
production source unchanged
failure is because actionable child diagnostic is lost
failure is not due to quoting, fixture, environment, or syntax error
```

Record exact RED commit SHA and command/output in the report.

If a correct regression already passes on the current product source, stop and re-evaluate the hypothesis rather than editing production.

## Phase C — minimal GREEN repair

After genuine RED only, make the smallest owning-boundary production change.

Expected design direction, subject to evidence:

- capture `rollover-prepare` stderr with stdout (`2>&1`) or an equivalent explicit mechanism;
- preserve a bounded child diagnostic on nonzero exit before/within the fail-closed terminal error;
- retain child exit code and `CNXCLAW_INSTALL_STAGE_COMPLETE` record;
- keep the generic stable stage/failure identity for machine searchability;
- do not retry the child command;
- do not alter arguments, transaction path, backup token, ownership checks, hash checks, staging order, plugin install order, or managed/passthrough lifecycle semantics.

### Diagnostic safety/bounding contract

The final diagnostic path must not blindly dump unbounded child output.

Define and test a bounded representation. It should:

- trim surrounding whitespace;
- preserve enough tail/head text to include the actionable Python exception;
- impose an explicit maximum character/byte bound suitable for installer transcript retention;
- provide a stable placeholder when child output is empty;
- avoid intentionally adding secrets/environment/config dumps;
- preserve deterministic machine-searchable context such as stage name and child exit code.

If a helper is introduced, keep it local/minimal and test it directly where practical.

## Phase D — GREEN verification

At minimum run:

1. focused Task-239 regression;
2. complete `tests/test_installer_observability_contract.py`;
3. relevant installer/rollover Python tests including generation rollover and installer transaction wiring;
4. repository Python test suite expected by current branch policy;
5. plugin `npm ci`, tests, build and `plugin:validate` where applicable;
6. `git diff --check`;
7. any packaged-installer/PowerShell acceptance smoke used by current branch.

Then push the exact final production candidate and require exact-SHA GitHub Actions:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

Do not authorize a live installer successor until the final candidate's required Actions are all terminal SUCCESS.

## Phase E — fingerprint and drift proof

Compute final plugin payload fingerprint from the final candidate using the repository's authoritative fingerprint tool.

Do not infer whether it changed. Record:

- predecessor product candidate SHA;
- RED SHA;
- production repair SHA;
- final candidate SHA;
- final plugin fingerprint;
- exact changed files for each commit;
- compare showing no unrelated production/test/workflow drift.

## PASS requirements

A PASS requires all of:

```text
meaningful test-only RED: proven
minimal production diagnostic repair: proven
stderr + stdout diagnostic preservation: proven
bounded diagnostic representation: proven
nonzero/fail-closed semantics unchanged: proven
rollover semantics unchanged: proven
no retry introduced: proven
focused GREEN: pass
full relevant validation: pass
final candidate Actions: all required SUCCESS
live installer invocations: 0
semantic submissions: 0
live product mutations: 0
```

Allowed final dispositions:

- `PASS_ROLLOVER_PREPARE_DIAGNOSTIC_PRESERVATION_TDD_REPAIRED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_RED_NOT_MEANINGFUL`
- `FAIL_REPAIR`
- `BLOCKED_CI`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260904-239-rollover-prepare-failure-diagnostic-preservation-tdd-repair.md`

Include:

- fresh authority;
- Task-238 accepted findings;
- exact RED test and output;
- minimal production diff rationale;
- bounded diagnostic contract;
- GREEN commands/results;
- exact candidate/fingerprint;
- Actions IDs/statuses;
- live zero-mutation and semantic-zero ledger;
- final disposition.

Then STOP for independent ChatGPT review.

Even after PASS, do not rerun the installer or perform Dashboard/Discord semantic acceptance until a separate reviewed deployment successor authorizes it.
