# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK214_DURABLE_WINDOWS_LAUNCHER_QUALIFICATION`
Current disposition: `TASK213_HARNESS_ROOT_CAUSE_ACCEPTED__DURABLE_LAUNCHER_QUALIFICATION_REQUIRED`
Task ID: `CNX-20260901-214`
Parent task: `CNX-20260901-213`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Current repaired product candidate

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Known old live generation remains:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 213 accepted result

Report:

`reports/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication.md`

Review:

`reviews/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication-review.md`

Accepted disposition:

`ACCEPT_PASS_DETACHED_LAUNCH_HARNESS_DEFECT_PROVEN__QUALIFY_DURABLE_WINDOWS_LAUNCHER_BEFORE_INSTALLER`

Accepted facts:

- Task-212 executed installer/repair source files were byte-identical to Task-207 candidate source at the relevant boundaries;
- ignored generated build output in that retained checkout was not candidate-proven and is not accepted as package provenance;
- Task-212 launcher used `Popen` with `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`, `stdin=DEVNULL`, redirected streams, no wait, and immediate launcher return;
- a harmless PowerShell child using the same mechanics reproduced Task-212 behavior: expected >=65s lifetime, but gone before 10s, stdout/stderr 0 bytes, no markers;
- this proves the detached launcher topology is defective/incompatible in the current executor environment without implicating CogentNexus product code;
- live product remains PASSTHROUGH on old fingerprint `f826...`, Gateway healthy, delivery/recovery READY, SQLite `ok`, Task-205 recovery cancelled/inert.

## Active Task 214

Hermes must execute:

`tasks/CNX-20260901-214-task213-durable-windows-launcher-qualification.md`

Task 214 is HARNESS-ONLY.

It must qualify a temporary uniquely named Windows Scheduled Task using a harmless PowerShell child before any new installer authorization.

Required proof:

1. fresh read-only product preservation gate;
2. create harmless synthetic child + wrapper in external evidence root;
3. register exactly one uniquely named Task-214 temporary Scheduled Task;
4. read back exact task action/settings/principal before execution;
5. start it exactly once;
6. prove child remains alive beyond 10 seconds and reaches intended >=65-second lifetime;
7. prove stdout/stderr start and terminal markers are durably captured;
8. prove PID + creation time + executable + argv identity;
9. prove wrapper child exit code `23` and Task Scheduler terminal `LastTaskResult` reconciliation;
10. unregister only the exact temporary Task-214 task;
11. prove no task/process residue and no CogentNexus/OpenClaw semantic/product-state change.

Even on PASS, Task 214 must not run the CogentNexus installer. A separate Task 215 will be required.

## Discord budget

Task 214 authorizes `0 Discord Sends`.

Task-207 semantic acceptance remains closed until installation/provenance/managed convergence is proven.

## Hard fence

No CogentNexus installer/install-over, no lifecycle enable/disable/start/stop/restart/reset/uninstall, no OpenClaw plugin mutation, no Gateway restart, no ownership/staging/transaction/backup mutation, no SQLite writes, no provider/model/config mutation, no product source/test/workflow edit, no Release/tag mutation, no force push, and no Discord traffic.
