# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK241_TASK240_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK240_ACCEPTED__TASK239_DIAGNOSTIC_REPAIR_VALIDATED__BOUNDED_EXACT_CANDIDATE_INSTALL_OVER_AUTHORIZED`
Task ID: `CNX-20260904-241`
Parent task: `CNX-20260904-240`
Diagnostic parent: `CNX-20260904-239`
Forensic parent: `CNX-20260904-238`
Installer-failure parent: `CNX-20260904-237`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-240 boundary

Independent review verdict:

`ACCEPT_PASS_TEST_HARNESS_PORTABILITY_REPAIRED__TASK239_PRODUCTION_DIAGNOSTIC_REPAIR_VALIDATED__EXACT_CANDIDATE_READY_FOR_BOUNDED_LIVE_INSTALL_REQUALIFICATION`

Exact candidate:

`18a51b15768fb3d2196e65f1ef470c34aeef7f36`

Task-239 production diagnostic repair in candidate lineage:

`ec29020632091aae3b50149b51303a36fde26310`

Candidate plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Exact-candidate Actions:

```text
PS5.1 Acceptance Smoke       33832755287 = SUCCESS
Windows Installer Pack Smoke 33832755300 = SUCCESS
Validate                      33832755313 = SUCCESS (attempt 2)
```

Task 240 was test-only and did not alter production/runtime source or live state.

## Preserved live boundary

Fresh Windows read-only evidence wins. The retained Task-237/238 boundary is:

```text
controller = passthrough
generation = 39
candidate plugin not installed
predecessor plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
Gateway healthy
provider = ollama
Delivery READY / pending 0
Recovery READY
SQLite integrity = ok
```

Task-237 retained backup token:

`c6aaf93db7c34f718d01302477a292e1`

Do not mutate or clean it.

## Active Task 241

Execute:

`tasks/CNX-20260904-241-task240-exact-candidate-windows-install-over-requalification.md`

Required sequence:

```text
fresh GitHub authority
-> exact detached candidate checkout + clean/fingerprint proof
-> fresh read-only Windows preflight + retained evidence inventory
-> one installer registration/start/invocation maximum
-> INSTALLER_RETRY_GATE=CLOSED once execution starts
-> if failure: preserve bounded Task-239 child diagnostic + backup/transaction evidence and STOP
-> if success: prove installed fingerprint + rollover/finalization + managed convergence + full health
-> zero semantic side effects
-> report
-> STOP for independent review
```

## Installer one-shot budget

```text
installer Scheduled Task registrations: 1 maximum
installer Scheduled Task starts: 1 maximum
installer invocations: 1 maximum
installer execution retries after start: 0
manual rollover-prepare/finalize: 0
manual plugin mutation: 0
manual controller/Gateway/lifecycle normalization: 0
```

Use only the installer's supported parameter contract. Bind source by invoking `scripts/install.ps1` from the exact detached candidate checkout. Do not invent `--install-source-commit`.

## Semantic zero budget

```text
Dashboard human semantic submissions: 0
Dashboard automated/native/computer-use submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
```

## Hard fences

No reset, uninstall/fresh reinstall, release/tag/asset mutation, force push/history rewrite, product/source/test/workflow edit during live execution, Task-237 backup cleanup, historical evidence cleanup, process termination, provider/model substitution, or manual post-failure repair.

## Stop boundary

Hermes must publish:

`reports/CNX-20260904-241-task240-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review. Even on PASS, no semantic acceptance is authorized without a separate successor.
