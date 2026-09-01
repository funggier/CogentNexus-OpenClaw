# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK216_DIRECT_SCHEDULED_TASK_TASK207_INSTALLER_REQUALIFICATION`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + authenticated Windows installer/provenance evidence through Hermes  
**Active task:** `CNX-20260901-216`  
**Parent:** `CNX-20260901-215`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK215_DIRECT_TERMINAL_PROPAGATION_ACCEPTED_WITH_DURATION_DEVIATION__TASK216_INSTALLER_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Current repository-GREEN repaired candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-207 candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

## Task 215 reviewed boundary

Task-215 report disposition:

`PASS_DIRECT_SCHEDULED_TASK_TERMINAL_PROPAGATION`

Independent review accepts the core result but retains two evidence deviations:

`ACCEPT_WITH_DURATION_DEVIATION__DIRECT_TERMINAL_PROPAGATION_PROVEN__INSTALLER_REQUALIFICATION_AUTHORIZED`

Proven direct topology:

```text
Windows Scheduled Task
  -> one top-level powershell.exe
  -> direct PowerShell script
```

Observed terminal proof:

```text
DIRECT_START: present
heartbeats: 11
DIRECT_END: present
script elapsed: 55.1713166s
intended exit: 23
Scheduler terminal state: Ready
LastTaskResult: 23
start count: 1
retry: none
cleanup: exact task absent
```

The task spec requested >=65 seconds and >=5-minute execution limit; actual values were 55.17 seconds and PT3M. These deviations are not erased. They do not invalidate the proven direct terminal-propagation boundary. Task 216 therefore uses an execution limit >=30 minutes and the real installer as the long-duration execution proof.

## Active Task 216

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification.md`

Task 216 must:

- prepare/fresh-verify exact candidate `27fe0181...` and candidate fingerprint `d067...`;
- re-prove the ordinary safe upgrade preflight from the preserved PASSTHROUGH old generation `f826...`;
- register exactly one temporary Task-216 Scheduled Task with `ExecutionTimeLimit >= PT30M`, no recurrence/retry;
- use one top-level Scheduled Task-owned PowerShell runner and invoke exact candidate `install.ps1` once in that same process;
- durably capture runner result and all seven installer diagnostic stage pairs plus final terminal line;
- require Scheduler `LastTaskResult=0` for success;
- independently prove installed fingerprint `d067...`, plugin enabled/loaded, ownership exact, OpenClaw pinned, controller MANAGED, startup/Gateway/Ollama/delivery/recovery/SQLite healthy;
- clean only the exact temporary Task-216 installer task;
- stop for ChatGPT review.

No installer retry or lifecycle workaround is authorized.

## Discord budget

`0 Discord Sends`.

Discord semantic requalification remains a separate successor after Task-216 install/provenance/managed health is independently reviewed PASS.

## Hard fence

One installer invocation maximum. No compensating lifecycle command, manual plugin/ownership/transaction/SQLite mutation, provider/model substitution, OpenClaw upgrade, product source/test/workflow mutation, Release/tag mutation, force push, or Discord traffic.
