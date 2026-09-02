# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK228_RETAINED_INVENTORY_PROVENANCE_RECONCILIATION`
Current disposition: `TASK227_ACCEPTED_BLOCK__PROVENANCE_RECONCILIATION_REQUIRED`
Task ID: `CNX-20260902-228`
Parent task: `CNX-20260902-227`
Repair parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parent: `CNX-20260902-224`
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

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

## Task-227 accepted result

Task-227 report:

`reports/CNX-20260902-227-task223-already-exact-reentry-adjudication.md`

Independent review:

`reviews/CNX-20260902-227-task223-already-exact-reentry-adjudication-review.md`

Accepted disposition:

`ACCEPT_BLOCKED_STALE_EVIDENCE_DRIFT__PROVENANCE_RECONCILIATION_REQUIRED`

Task 227 re-proved the supported already-exact diagnostic path:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

but did not authorize installer re-entry because the matching retained Task-223 inventory file was observed present after Task 224 had recorded it absent.

## Active Task 228

Execute:

`tasks/CNX-20260902-228-retained-inventory-provenance-reconciliation.md`

Task 228 is read-only provenance reconciliation. It must determine whether the matching retained inventory is:

- a historical Task-223 artifact;
- a post-Task223 mutation/restore;
- or provenance-unresolved.

The observed inventory LastWriteTime equals the historical Task-223 `plugin-rollover-finalize` stage-start instant, but timestamp correlation alone is not authority. Task 228 must inspect metadata, copied contents, Task-223 stage evidence, and the retained Task-224 absence probe before classification.

## Runtime / Discord boundary

Task 228 authorizes read-only GitHub/source/Windows/evidence inspection, external evidence copies under `%LOCALAPPDATA%\Temp`, pure helper calculations, and coordination report publication.

Task 228 does **not** authorize:

- installer invocation;
- stale transaction/inventory/backup cleanup or mutation;
- rollover prepare/finalize;
- plugin/config/ownership mutation;
- cnxclaw lifecycle action;
- Gateway restart;
- SQLite write;
- process termination;
- provider/model substitution;
- Release/tag/asset mutation;
- product/source/test/workflow edits;
- force push/history rewrite;
- Discord Send/API semantic traffic.

Discord budget: `0 Sends`.

## Stop boundary

Hermes must publish:

`reports/CNX-20260902-228-retained-inventory-provenance-reconciliation.md`

Then stop for independent ChatGPT review before any cleanup or installer retry.
