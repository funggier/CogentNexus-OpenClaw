# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK227_TASK223_ALREADY_EXACT_REENTRY_ADJUDICATION`
Current disposition: `TASK226_ACCEPTED__ALREADY_EXACT_REENTRY_REQUALIFICATION_REQUIRED`
Task ID: `CNX-20260902-227`
Parent task: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parent: `CNX-20260902-224`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted repair authority

Task-226 accepted production repair:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint remains:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-226 report:

`reports/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair.md`

Task-226 independent review:

`reviews/CNX-20260902-226-rollover-prepare-attestation-fail-closed-repair-review.md`

Accepted disposition:

`ACCEPT_PASS_REPAIR_GREEN__ALREADY_EXACT_REENTRY_REQUALIFICATION_REQUIRED`

## Active Task 227

Execute:

`tasks/CNX-20260902-227-task223-already-exact-reentry-adjudication.md`

Task 227 is read-only Windows/source adjudication. It must prove whether the preserved Task-223 partial state now follows the supported already-exact upgrade path:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

The retained Task-223 transaction is obsolete producer-defect evidence and must not be finalized, edited, deleted, moved, or reused.

## Runtime / Discord boundary

Task 227 authorizes:

- fresh GitHub/Actions/source reads;
- read-only Windows state inspection;
- read-only retained transaction/backup hashing;
- read-only `classify-install` with explicit inventory/source fingerprint;
- pure production action-resolver execution;
- external evidence capture under `%LOCALAPPDATA%\Temp`;
- coordination report publication.

Task 227 does **not** authorize:

- installer invocation;
- rollover prepare/finalize;
- plugin/config/ownership/transaction/backup mutation;
- cnxclaw lifecycle action;
- Gateway restart;
- SQLite write;
- process termination;
- provider/model substitution;
- Release/tag/asset mutation;
- force push/history rewrite;
- Discord Send/API semantic traffic.

Discord budget: `0 Sends`.

## Stop boundary

Hermes must publish:

`reports/CNX-20260902-227-task223-already-exact-reentry-adjudication.md`

Then stop for independent ChatGPT review before any installer retry.
