# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK238_TASK237_ROLLOVER_PREPARE_TERMINAL_FORENSIC_ADJUDICATION`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 238 is read-only forensic adjudication with zero installer and zero semantic budget  
**Active task:** `CNX-20260904-238`  
**Parent:** `CNX-20260904-237`  
**Repository/TDD parent:** `CNX-20260903-235`  
**Installer safety / attestation repair parent:** `CNX-20260902-226`  
**Historical direct-extension ownership repair:** `CNX-20260829-140`  
**Historical installer failure lineage:** `CNX-20260902-223`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK237_INSTALLER_TERMINAL_FAIL_ACCEPTED__EXACT_PREPARE_INVARIANT_FORENSICS_REQUIRED`

## Exact authority

Accepted repository candidate remains:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected candidate plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Task-237 post-failure predecessor plugin fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` remains unchanged at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-237 report disposition:

`FAIL_INSTALLER_TERMINAL`

Task-237 independent review verdict:

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_PREPARE_EXACT_INVARIANT_UNPROVEN__READ_ONLY_FORENSIC_SUCCESSOR_REQUIRED`

## Preserved live state

Task-237 terminal boundary to preserve and re-prove read-only:

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

Do not manually re-enable managed mode or repair plugin identity.

## Active Task 238

Execute:

`docs/operations/coordination/tasks/CNX-20260904-238-task237-rollover-prepare-terminal-forensic-adjudication.md`

Required sequence:

```text
fresh authority + state preservation
-> inspect/hash Task-237 evidence
-> recover rollover id/token
-> inventory backup + transaction artifacts
-> compare Task-237 backup/current retired identities
-> eliminate rollover-prepare invariants in source order
-> prove exact root cause or explicit evidence blocker
-> classify prepare-output observability defect
-> report
-> STOP for independent review
```

## Zero-mutation fence

```text
installer registration/start/invocation: 0
direct rollover-prepare/finalize: 0
manual plugin lifecycle mutation: 0
manual managed/lifecycle/Gateway repair: 0
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

Do not rerun the installer or rollover prepare to improve observability.

## Required outcome

Task 238 must either prove the exact failing `rollover-prepare` invariant from retained evidence, or stop explicitly as `BLOCKED_EXACT_PREPARE_ERROR_UNPROVEN`/other permitted blocker. It must also classify whether the installer's captured-but-not-emitted `$prepareOutput` is a source-level observability defect.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-238-task237-rollover-prepare-terminal-forensic-adjudication.md`

Then stop for independent ChatGPT review. No installer retry or semantic acceptance is authorized from this status.
