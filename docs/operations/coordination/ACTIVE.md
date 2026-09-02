# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK229_ALREADY_EXACT_WINDOWS_INSTALLER_REENTRY_COMPLETION`
Current disposition: `TASK228_ACCEPTED__ONE_CONTROLLED_ALREADY_EXACT_INSTALLER_REENTRY_AUTHORIZED`
Task ID: `CNX-20260902-229`
Parent task: `CNX-20260902-228`
Repair parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parents: `CNX-20260902-224`, `CNX-20260902-227`, `CNX-20260902-228`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted repair and source authority

Exact live installer source for Task 229:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-228 report:

`reports/CNX-20260902-228-retained-inventory-provenance-reconciliation.md`

Task-228 independent review:

`reviews/CNX-20260902-228-retained-inventory-provenance-reconciliation-review.md`

Accepted disposition:

`ACCEPT_PASS_HISTORICAL_TASK223_ARTIFACT_RECONCILED__ONE_CONTROLLED_ALREADY_EXACT_INSTALLER_REENTRY_AUTHORIZED`

## Active Task 229

Execute:

`tasks/CNX-20260902-229-already-exact-windows-installer-reentry-completion.md`

Task 229 authorizes exactly one normal installer invocation only after fresh preflight proves:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

The installer must be sourced from exact repaired commit `9a8510f...` so the live skill tree receives the Task-226 producer repair.

Expected plugin/rollover live mutation counts from the one invocation:

```text
openclaw plugins install: 0
rollover-prepare: 0
rollover-finalize: 0
```

The installer itself may perform its documented non-plugin/ownership/policy/Host lifecycle. Manual lifecycle repair outside the one installer invocation is forbidden.

## Historical evidence boundary

The Task-223 transaction, matching inventory and backup are immutable forensic evidence. They must not be finalized, edited, moved, renamed, deleted, archived, replaced, or reused. Task 229 must hash them before and after the installer and prove exact preservation.

## Runtime / Discord boundary

Task 229 permits one direct one-shot Windows Scheduled Task installer execution after all preflight gates pass.

It does **not** permit:

- installer retry/second invocation;
- skip/link installer override flags;
- manual plugin or rollover actions;
- manual cnxclaw/Gateway lifecycle repair;
- stale-evidence cleanup;
- manual SQLite write;
- process termination;
- provider/model substitution;
- Release/tag/asset mutation;
- product/source/test/workflow edit;
- force push/history rewrite;
- Discord Send/API semantic traffic.

Discord budget: `0 Sends`.

## Stop boundary

Hermes must publish:

`reports/CNX-20260902-229-already-exact-windows-installer-reentry-completion.md`

Then stop for independent ChatGPT review before any semantic/durable-delivery acceptance or historical evidence cleanup.
