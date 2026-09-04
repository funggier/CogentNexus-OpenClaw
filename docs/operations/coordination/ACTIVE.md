# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK239_ROLLOVER_PREPARE_FAILURE_DIAGNOSTIC_PRESERVATION_TDD_REPAIR`
Current disposition: `TASK238_BLOCKER_ACCEPTED__EXACT_RUNTIME_EXCEPTION_UNRECOVERABLE_FROM_RETAINED_EVIDENCE__OBSERVABILITY_REPAIR_ONLY_AUTHORIZED`
Task ID: `CNX-20260904-239`
Parent task: `CNX-20260904-238`
Installer-failure parent: `CNX-20260904-237`
Repository/TDD parent: `CNX-20260903-235`
Installer safety / attestation repair parent: `CNX-20260902-226`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated repository operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-238 boundary

Task-238 disposition:

`BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`

Task-238 observability classification:

`OBSERVABILITY_DEFECT_PROVEN`

Independent review:

`ACCEPT_BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN__OBSERVABILITY_DEFECT_PROVEN__TDD_OBSERVABILITY_REPAIR_REQUIRED`

Task-237 backup token retained as evidence:

`c6aaf93db7c34f718d01302477a292e1`

Current retained backup/live retired tree hash:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

The matching current hashes do not prove the hashes matched during the original Task-237 execution. Do not guess the lost exact runtime exception.

## Repository authority entering Task 239

Accepted predecessor product candidate:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Entering plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task 239 must compute the final candidate fingerprint rather than assume whether an installer-source-only repair changes plugin identity.

## Preserved live boundary

Task 239 is repository-only. Live state must not be normalized:

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

Fresh live evidence wins, but no live mutation is authorized.

## Active Task 239

Execute:

`tasks/CNX-20260904-239-rollover-prepare-failure-diagnostic-preservation-tdd-repair.md`

Required flow:

```text
fresh authority
-> inspect proven observability defect + working recovery-preflight precedent
-> test-only meaningful RED
-> verify stdout/stderr child diagnostic loss
-> minimal bounded diagnostic preservation repair
-> focused GREEN
-> full relevant validation
-> exact final candidate + fingerprint proof
-> exact-SHA Actions GREEN
-> report
-> STOP for independent review
```

## TDD and behavior fence

Production source must not change before a genuine test-only RED is observed.

The repair may preserve bounded diagnostic output only. It must not change:

```text
rollover arguments
ownership boundaries
backup/hash/transaction semantics
plugin installation order
passthrough/managed lifecycle semantics
child retry cardinality
fail-closed behavior
```

## Live / semantic zero budget

```text
live installer registrations/starts/invocations: 0
live rollover-prepare/finalize calls: 0
manual plugin lifecycle mutation: 0
manual managed re-enable/lifecycle/Gateway repair: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
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

## Stop boundary

Hermes must publish:

`reports/CNX-20260904-239-rollover-prepare-failure-diagnostic-preservation-tdd-repair.md`

Then stop for independent ChatGPT review.

Even on PASS, do not rerun the installer or perform Dashboard/Discord semantic acceptance without a separate reviewed successor.
