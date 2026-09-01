# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK215_DIRECT_SCHEDULED_TASK_TERMINAL_PROPAGATION_QUALIFICATION`
Current disposition: `TASK214_PARTIAL_ACCEPTED__SCHEDULED_TASK_LAUNCH_PROVEN__TERMINAL_PROPAGATION_UNQUALIFIED`
Task ID: `CNX-20260901-215`
Parent task: `CNX-20260901-214`
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

Known live old generation remains:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 214 reviewed result

Report:

`reports/CNX-20260901-214-task213-durable-windows-launcher-qualification.md`

Review:

`reviews/CNX-20260901-214-task213-durable-windows-launcher-qualification-review.md`

Accepted disposition:

`ACCEPT_PARTIAL__SCHEDULED_TASK_LAUNCH_PROVEN__TERMINAL_PROPAGATION_NOT_QUALIFIED`

Accepted facts:

- one corrected temporary Scheduled Task was registered and started exactly once;
- the task created harmless PowerShell PID `19056` and durably persisted `CHILD_START`;
- exact temporary task was unregistered and proved absent;
- product state was preserved: PASSTHROUGH, generation 33, old fingerprint `f826...`, Gateway healthy, delivery/recovery READY;
- no installer/lifecycle/plugin/SQLite/Discord mutation occurred.

Task-214 PASS criteria were not fully met because the intended >=65-second terminal path was not proven:

```text
CHILD_END: absent
child exit-code file: absent
Scheduler LastTaskResult: 1
expected/equivalent: 23
```

The nested wrapper -> child boundary remains a confounder. The launcher is not authorized for the CogentNexus installer yet.

## Active Task 215

Hermes must execute:

`tasks/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification.md`

Task 215 is HARNESS-ONLY and removes nested process mechanics.

Required topology:

```text
Windows Scheduled Task
  -> one harmless PowerShell script directly
```

The direct script must itself persist `DIRECT_START`, PID/creation/context, periodic heartbeat evidence through >=55 seconds, `DIRECT_END`, and `intended-exit-code.txt=23`, then terminate with `exit 23`.

Task Scheduler must prove one run, sustained >=65-second lifetime, terminal/non-running state and `LastTaskResult=23` (or exactly proven equivalent representation). Exact task cleanup and product-state preservation are required.

If direct terminal propagation passes, a later separately reviewed successor may authorize the Task-207 installer using the qualified execution model. Task 215 itself does not install anything.

## Discord budget

Task 215 authorizes `0 Discord Sends`.

Task-207 semantic acceptance remains closed until exact installation/provenance/managed convergence is independently proven.

## Hard fence

No CogentNexus installer/install-over, no lifecycle action, no OpenClaw plugin/config mutation, no Gateway restart, no ownership/staging/transaction/backup mutation, no SQLite writes, no provider/model/config substitution, no product source/test/workflow mutation, no Release/tag mutation, no force push, and no Discord traffic.
