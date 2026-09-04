# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK238_TASK237_ROLLOVER_PREPARE_TERMINAL_FORENSIC_ADJUDICATION`
Current disposition: `TASK237_INSTALLER_TERMINAL_FAIL_ACCEPTED__EXACT_PREPARE_INVARIANT_FORENSICS_REQUIRED`
Task ID: `CNX-20260904-238`
Parent task: `CNX-20260904-237`
Repository/TDD parent: `CNX-20260903-235`
Installer safety / attestation repair parent: `CNX-20260902-226`
Historical direct-extension ownership repair: `CNX-20260829-140`
Historical installer failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Exact repository/live authority

Accepted source candidate remains:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected candidate plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Task-237 post-failure predecessor plugin fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-237 independent review verdict:

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_PREPARE_EXACT_INVARIANT_UNPROVEN__READ_ONLY_FORENSIC_SUCCESSOR_REQUIRED`

## Preserved live boundary

Expected fresh read-only state from Task 237:

```text
controller = passthrough
generation = 39
Gateway healthy
provider = ollama
Delivery READY, pending = 0
Recovery READY
SQLite integrity = ok
candidate plugin not installed
semantic submissions = 0
```

Fresh live evidence wins. Do not normalize or repair drift.

## Active Task 238

Execute:

`tasks/CNX-20260904-238-task237-rollover-prepare-terminal-forensic-adjudication.md`

Required high-level flow:

```text
fresh authority + preservation gate
-> hash/read Task-237 evidence
-> recover rollover id/token
-> inventory Task-237 backup/transaction artifacts
-> compare backup/current retired tree and payload identities
-> eliminate prepare invariants in source order
-> classify exact prepare root cause or evidence blocker
-> classify swallowed prepare-output observability defect
-> report
-> STOP for independent review
```

## Hard fence

Task 238 is read-only forensic work.

```text
installer registrations/starts/invocations: 0
direct rollover-prepare/finalize calls: 0
manual plugin lifecycle mutation: 0
manual managed re-enable/lifecycle/Gateway repair: 0
manual Ticket/outbox/recovery/SQLite writes: 0
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
process termination: 0
provider/model substitution: 0
Task-237/Task-223/Task-233 evidence mutation: 0
reset/uninstall/reinstall: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

Do not rerun the installer merely to recover diagnostics.

## Stop boundary

Hermes must publish:

`reports/CNX-20260904-238-task237-rollover-prepare-terminal-forensic-adjudication.md`

Then stop for independent ChatGPT review.
