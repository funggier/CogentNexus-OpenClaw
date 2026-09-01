# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK216_DIRECT_SCHEDULED_TASK_TASK207_INSTALLER_REQUALIFICATION`
Current disposition: `TASK215_DIRECT_TERMINAL_PROPAGATION_ACCEPTED_WITH_DURATION_DEVIATION__INSTALLER_REQUALIFICATION_AUTHORIZED`
Task ID: `CNX-20260901-216`
Parent task: `CNX-20260901-215`
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

Known preserved old live generation before Task 216:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 215 reviewed result

Report:

`reports/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification.md`

Review:

`reviews/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification-review.md`

Accepted disposition:

`ACCEPT_WITH_DURATION_DEVIATION__DIRECT_TERMINAL_PROPAGATION_PROVEN__INSTALLER_REQUALIFICATION_AUTHORIZED`

Accepted facts:

- one direct temporary Scheduled Task was registered and started exactly once;
- direct action owned one PowerShell process with no nested PowerShell/wrapper/Popen/detached boundary;
- durable `DIRECT_START`, 11 heartbeat records, `DIRECT_END`, and intended exit code `23` were persisted;
- Scheduler reached terminal Ready and `LastTaskResult=23` with no retry;
- exact temporary task was removed and proved absent;
- product state remained preserved: PASSTHROUGH, generation 33, old fingerprint `f826...`, Gateway healthy, delivery/recovery READY;
- no installer/lifecycle/plugin/SQLite/Discord mutation occurred.

Evidence deviations retained explicitly:

- direct script elapsed `55.1713166s`, not the requested >=65s;
- task `ExecutionTimeLimit=PT3M`, not the requested >=5m.

These deviations prevent literal strict-contract PASS but do not negate the central terminal-propagation proof. Task 216 corrects the duration setting by requiring >=30 minutes and uses the real installer as the long-duration execution proof.

## Active Task 216

Hermes must execute:

`tasks/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification.md`

Task 216 authorizes one exact Task-207 installer execution using a temporary direct Scheduled Task-owned PowerShell runner.

Required boundaries:

1. fresh exact candidate checkout at `27fe0181...` and package/fingerprint revalidation;
2. re-prove PASSTHROUGH ordinary-upgrade preflight with live `f826...`, candidate `d067...`, `mode=upgrade`, no pending rollover;
3. register one unique Task-216 temporary task with `ExecutionTimeLimit >= PT30M`, `RestartCount=0`, no recurrence/retry;
4. one top-level PowerShell process only; runner invokes exact candidate `install.ps1` once in the same PowerShell process;
5. durable transcript/output must retain all seven installer stage START/COMPLETE pairs and final success/failure evidence;
6. Task Scheduler terminal `LastTaskResult=0` required for install success;
7. independently prove installed fingerprint exact `d067...`, plugin enabled/loaded, ownership coherent, OpenClaw pinned, MANAGED startup/Gateway/Ollama/delivery/recovery/SQLite healthy;
8. unregister only the exact temporary Task-216 task after terminal/postflight evidence;
9. no installer retry or lifecycle workaround.

## Discord budget

Task 216 authorizes `0 Discord Sends`.

Task-207 semantic Discord acceptance remains closed until Task-216 installation/provenance/managed convergence is independently reviewed PASS.

## Hard fence

One installer invocation maximum. No compensating lifecycle command, no manual plugin/ownership/transaction/SQLite mutation, no provider/model substitution, no OpenClaw upgrade, no source/test/workflow edit, no Release/tag mutation, no force push, and no Discord traffic.
