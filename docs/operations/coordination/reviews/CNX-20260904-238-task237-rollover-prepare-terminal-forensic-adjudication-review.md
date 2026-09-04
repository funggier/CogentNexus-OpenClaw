# CNX-20260904-238 — Independent Review

## Verdict

`ACCEPT_BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN__OBSERVABILITY_DEFECT_PROVEN__TDD_OBSERVABILITY_REPAIR_REQUIRED`

## Scope reviewed

Independent review of:

- `reports/CNX-20260904-238-task237-rollover-prepare-terminal-forensic-adjudication.md`
- exact candidate `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- Task-237 retained installer evidence and Task-238 forensic conclusions
- exact candidate `scripts/install.ps1`
- existing installer-observability regression surface

## Findings

### 1. The blocked forensic disposition is correct

Task 238 recovered the Task-237 rollover identity:

`c6aaf93db7c34f718d01302477a292e1`

and proved a Task-237-created backup exists at the external rollover-backup boundary while no matching transaction was persisted.

That localizes the original Task-237 failure to the `rollover-prepare` interval after backup creation/copy began and before successful transaction persistence.

However, the retained child diagnostic does not contain the Python exception from the original execution. The currently retained source and backup trees both hash to:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

and both retain payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Therefore current evidence cannot prove that a project-tree mismatch existed at the instant of Task 237, nor can it select another exact exception in that interval. A transient race/access condition remains possible but unproven.

It would be incorrect to relabel the failure as Task-140 recurrence, Task-223/226 recurrence, or `pre-install backup project-tree attestation mismatch` without the original child diagnostic.

### 2. Observability defect is independently proven

The candidate installer currently executes `rollover-prepare` as captured stdout:

```powershell
$prepareOutput = (& python ... "rollover-prepare" ... | Out-String)
$rolloverPrepareExit = $LASTEXITCODE
Complete-InstallerDiagnosticStage ... -ExitCode $rolloverPrepareExit
if ($rolloverPrepareExit -ne 0) {
    throw "ownership-safe plugin generation rollover pre-install proof failed"
}
```

Two evidence-loss properties are present:

1. `$prepareOutput` is not emitted or included in the failure record before the generic fail-closed throw;
2. unlike the existing `recovery-preflight` pattern in the same installer, the command does not merge stderr with `2>&1`, so a Python traceback/error written to stderr need not be captured by `$prepareOutput` at all.

The same installer already contains a working fail-closed precedent:

```powershell
$recoveryJson = (& python $ownershipScript recovery-preflight ... 2>&1 | Out-String)
...
if ($recoveryExit -ne 0) {
    throw "Recovery preflight failed ...: $recoveryJson"
}
```

This proves the repair can be constrained to diagnostic preservation without changing ownership or rollover semantics.

### 3. Task-238 execution respected the hard fence

Task 238 performed read-only evidence collection and hashing only. No installer, rollover-prepare/finalize, plugin lifecycle, managed re-enable, semantic Send, recovery replay, durable-state write, cleanup, reset/uninstall/reinstall, or release mutation was performed.

The preserved live boundary remains fail-closed:

```text
controller = passthrough
generation = 39
Gateway = healthy
provider = ollama
Delivery = READY / pending 0
Recovery = READY
SQLite integrity = ok
candidate plugin = not installed
predecessor plugin fingerprint = e3bcce04...
```

## Successor authorization

Authorize one repository-only TDD successor whose sole production purpose is to preserve a bounded actionable `rollover-prepare` child diagnostic on nonzero exit.

Required successor properties:

- RED test commit before production edit;
- RED must prove the current installer loses a synthetic child diagnostic on prepare failure;
- cover stderr as well as stdout;
- preserve the original nonzero exit/fail-closed behavior;
- diagnostic output must be bounded and suitable for retained installer transcripts;
- no retries or rollover-behavior changes;
- no ownership-boundary relaxation;
- no cleanup or normalization of Task-237 backup/evidence;
- full relevant GREEN and exact-SHA Actions before any live deployment successor;
- no live installer or semantic execution in the observability-repair task.

The existing `tests/test_installer_observability_contract.py` is an appropriate regression surface, but the successor should prefer a production-shaped behavioral assertion where practical rather than only checking for an arbitrary source string.

## Not authorized

This review does **not** authorize:

- rerunning Task-237 installer;
- calling `rollover-prepare` or `rollover-finalize` against live state;
- deleting the orphan Task-237 backup;
- manually returning the controller to managed mode;
- installing/copying/repairing the plugin manually;
- Dashboard or Discord semantic acceptance;
- Task-233 replay/settlement;
- reset/uninstall/reinstall;
- release/tag/asset mutation.

## Final review state

`TASK238_BLOCKER_ACCEPTED__EXACT_RUNTIME_EXCEPTION_UNRECOVERABLE_FROM_RETAINED_EVIDENCE__OBSERVABILITY_REPAIR_ONLY_AUTHORIZED`
