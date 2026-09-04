# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK239_ROLLOVER_PREPARE_FAILURE_DIAGNOSTIC_PRESERVATION_TDD_REPAIR`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 239 is repository-only TDD observability repair with zero live installer and zero semantic budget  
**Active task:** `CNX-20260904-239`  
**Parent:** `CNX-20260904-238`  
**Installer-failure parent:** `CNX-20260904-237`  
**Repository/TDD parent:** `CNX-20260903-235`  
**Installer safety / attestation repair parent:** `CNX-20260902-226`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK238_BLOCKER_ACCEPTED__EXACT_RUNTIME_EXCEPTION_UNRECOVERABLE_FROM_RETAINED_EVIDENCE__OBSERVABILITY_REPAIR_ONLY_AUTHORIZED`

## Task-238 accepted findings

Task-238 final disposition:

`BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`

Observability classification:

`OBSERVABILITY_DEFECT_PROVEN`

Independent review verdict:

`ACCEPT_BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN__OBSERVABILITY_DEFECT_PROVEN__TDD_OBSERVABILITY_REPAIR_REQUIRED`

Task-237 rollover token recovered by forensics:

`c6aaf93db7c34f718d01302477a292e1`

A Task-237 backup exists but no matching transaction exists. Current backup and live retired project both hash to:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

and both retain payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

This localizes the lost Task-237 failure to prepare/copy/hash before transaction persistence but does not identify the original exact exception. Do not infer a hash mismatch or historical-defect recurrence without new evidence.

## Repository authority entering Task 239

Accepted predecessor product candidate:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Entering plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains unchanged at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task 239 must compute the final candidate fingerprint and must not assume whether it changes.

## Proven observability defect

The current `plugin-rollover-prepare` path captures stdout into `$prepareOutput`, does not merge stderr, and does not surface/persist `$prepareOutput` on nonzero exit before throwing the generic wrapper failure.

The same installer has a working `recovery-preflight` precedent using `2>&1 | Out-String` plus a fail-closed error that contains the child diagnostic.

## Preserved live state

Live state remains an evidence boundary and must not be normalized during Task 239:

```text
controller = passthrough
generation = 39
Gateway healthy
provider = ollama
Delivery READY / pending 0
Recovery READY
SQLite integrity = ok
candidate plugin not installed
predecessor plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Fresh read-only evidence wins, but live mutation is not authorized.

## Active Task 239

Execute:

`docs/operations/coordination/tasks/CNX-20260904-239-rollover-prepare-failure-diagnostic-preservation-tdd-repair.md`

Required sequence:

```text
fresh repository authority
-> inspect observability defect + same-installer working precedent
-> test-only meaningful RED
-> verify lost stdout/stderr child diagnostic
-> minimal bounded diagnostic-preservation production repair
-> focused GREEN
-> full relevant validation
-> exact final candidate + fingerprint
-> exact-SHA Actions GREEN
-> report
-> STOP for independent review
```

## TDD requirement

No production source edit before a meaningful test-only RED.

The repair must preserve existing fail-closed/nonzero behavior and must not change rollover arguments, ownership boundaries, backup/hash/transaction semantics, plugin install order, lifecycle semantics, or retry cardinality.

## Zero live-effect budget

```text
live installer registration/start/invocation: 0
live rollover-prepare/finalize: 0
manual plugin lifecycle mutation: 0
manual managed/lifecycle/Gateway repair: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
Task-237 orphan backup cleanup/mutation: 0
Task-223/Task-233 evidence mutation: 0
reset/uninstall/reinstall: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-239-rollover-prepare-failure-diagnostic-preservation-tdd-repair.md`

Then stop for independent ChatGPT review. Even on PASS, no live installer retry or semantic acceptance is authorized without a separate successor.
