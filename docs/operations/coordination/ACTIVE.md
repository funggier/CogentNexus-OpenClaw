# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK224_ROLLOVER_FINALIZE_RETAINED_STATE_ADJUDICATION`
Current disposition: `TASK223_INSTALLER_TERMINAL_FAILURE_ACCEPTED__ROLLOVER_FINALIZE_ROOT_CAUSE_REQUIRED`
Task ID: `CNX-20260902-224`
Parent task: `CNX-20260902-223`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: Hermes / authenticated Windows forensic operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted candidate authority

Exact source candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted package identity:

```text
artifact ID: 9810139538
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
payload files: 192
payload fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

Task 222 package provenance remains accepted. Task 223 independently reproved this candidate before the single installer launch and the installed canonical plugin payload now reports the same exact fingerprint.

## Task-223 reviewed result

Report:

`reports/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification.md`

Independent review:

`reviews/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification-review.md`

Accepted disposition:

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_FINALIZE_ROOT_CAUSE_ADJUDICATION_REQUIRED`

Accepted facts:

- direct Scheduled Task launcher reached a coherent terminal result;
- exactly one installer invocation/start occurred;
- candidate installation itself completed and installed fingerprint is exact `e3bcce04...`;
- `plugin-disable-post-install` completed exit 0;
- `plugin-rollover-finalize` completed exit 1;
- no final installer success marker exists;
- latest Task-223 rollover transaction remains unresolved;
- no installer retry, lifecycle repair, Gateway restart, process kill, or Discord traffic occurred;
- controller remains PASSTHROUGH generation 33, startup adapter absent, Gateway/Ollama healthy, Delivery/Recovery READY, SQLite integrity `ok`.

The generic PowerShell error does not identify which Python finalizer predicate failed. Historical Tasks 143/144 repaired direct same-path defects, but current evidence does not yet prove either regression.

## Active Task 224

Hermes must execute:

`tasks/CNX-20260902-224-task223-rollover-finalize-retained-state-adjudication.md`

Task 224 is read-only forensics. It must:

1. preserve the Task-223 partial live state;
2. recover the first specific Python exception/traceback from the retained installer transcript if present;
3. hash/parse the exact retained transaction and matching inventory;
4. inspect the current ownership manifest, backup, installed plugin and inventory read-only;
5. reconstruct every `finalize_plugin_rollover_transaction()` pre-write predicate in candidate source order without invoking the finalizer;
6. identify the first exact failing predicate and compared values;
7. adjudicate the write/verify boundary read-only only if all pre-write predicates pass;
8. compare with Task-143/144 invariants without assuming regression;
9. classify source defect vs invalid transaction/state/inventory/manifest/backup/storage/write-boundary failure;
10. publish report and stop.

## Runtime / Discord boundary

Task 224 authorizes `0 Discord Sends` and `0 installer/finalizer/lifecycle invocations`.

No installer retry, rollover prepare/finalize, cnxclaw lifecycle action, OpenClaw plugin mutation, Gateway restart, ownership/transaction/backup/SQLite write, provider/model substitution, process termination, product/source edit, Release/tag mutation, or force push is authorized.
