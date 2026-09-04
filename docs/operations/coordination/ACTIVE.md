# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK240_TASK239_CROSS_PLATFORM_POWERSHELL_TEST_HARNESS_PORTABILITY_REPAIR`
Current disposition: `TASK239_PASS_REJECTED__PRODUCTION_DIAGNOSTIC_REPAIR_FUNCTIONAL__CROSS_PLATFORM_TEST_HARNESS_REGRESSION_REQUIRES_TEST_ONLY_REPAIR`
Task ID: `CNX-20260904-240`
Parent task: `CNX-20260904-239`
Forensic parent: `CNX-20260904-238`
Installer-failure parent: `CNX-20260904-237`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated repository operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-239 findings

Task-239 production diagnostic repair candidate:

`ec29020632091aae3b50149b51303a36fde26310`

Task-239 RED commit:

`2c5d68384df11e38b9cea5e565c247324c4c5f44`

Candidate plugin fingerprint remains:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Independent review verdict:

`REJECT_PASS_CROSS_PLATFORM_VALIDATION_REGRESSION__PRODUCTION_DIAGNOSTIC_REPAIR_ACCEPTED_AS_FUNCTIONAL_CANDIDATE__TEST_HARNESS_PORTABILITY_REPAIR_REQUIRED`

The production repair is not authorized for additional modification in Task 240.

## Authoritative validation regression

Report HEAD `b70606460c6ea3d8d37a3a8317946aa5b1ceec35`:

```text
PS5.1 Acceptance Smoke = SUCCESS
Windows Installer Pack Smoke = SUCCESS
Validate = FAILURE
```

Validate run: `33830388146`.

Root cause is proven in the Task-239 regression test: it unconditionally invokes `powershell.exe` on Ubuntu/macOS. Windows Python 3.11 and 3.14 pass; non-Windows matrices fail with `FileNotFoundError` for `powershell.exe`.

## Active Task 240

Execute:

`tasks/CNX-20260904-240-task239-cross-platform-powershell-test-harness-portability-repair.md`

Required sequence:

```text
fresh authority
-> retain existing CI failure as RED
-> minimal test-only PowerShell capability/portability repair
-> focused Windows helper execution GREEN
-> non-Windows no false failure from absent powershell.exe
-> full validation
-> fingerprint unchanged
-> exact final SHA Actions GREEN (Validate + Installer Pack + PS5.1)
-> report
-> STOP for independent review
```

## Hard source fence

Task 240 must not modify production/runtime source, including `scripts/install.ps1`. It must not change workflows merely to mask the failing test. The authorized change is limited to the Task-239 test harness and directly necessary test support, if any.

## Preserved live boundary

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

No live normalization is authorized.

## Zero-effect budget

```text
live installer registrations/starts/invocations: 0
live rollover-prepare/finalize: 0
manual plugin/lifecycle/Gateway/managed mutation: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard/Discord/API semantic sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
forensic evidence cleanup/mutation: 0
release/tag/asset mutation: 0
force push/history rewrite: 0
```

## Stop boundary

Hermes must publish:

`reports/CNX-20260904-240-task239-cross-platform-powershell-test-harness-portability-repair.md`

Then stop for independent ChatGPT review. No live installer retry or semantic acceptance is authorized in Task 240.
