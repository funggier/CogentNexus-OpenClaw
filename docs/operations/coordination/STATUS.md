# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK215_DIRECT_SCHEDULED_TASK_TERMINAL_PROPAGATION_QUALIFICATION`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + authenticated Windows harness qualification through Hermes  
**Active task:** `CNX-20260901-215`  
**Parent:** `CNX-20260901-214`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK214_SCHEDULED_LAUNCH_PARTIAL__TASK215_DIRECT_TERMINAL_QUALIFICATION_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Current repository-GREEN repaired candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-207 candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

## Task 214 reviewed boundary

Task-214 report disposition was `PASS_DURABLE_SCHEDULED_TASK_LAUNCH__TERMINAL_PROPAGATION_UNPROVEN`.

Independent review narrows acceptance to:

`ACCEPT_PARTIAL__SCHEDULED_TASK_LAUNCH_PROVEN__TERMINAL_PROPAGATION_NOT_QUALIFIED`

The temporary Scheduled Task successfully created a harmless PowerShell process and persisted `CHILD_START`, then was cleaned up exactly. But required terminal evidence was missing: no end marker, no child exit-code file, and Scheduler `LastTaskResult=1` rather than expected/equivalent 23. Product state remained unchanged and healthy at its preserved PASSTHROUGH boundary.

## Active Task 215

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-215-task214-direct-scheduled-task-terminal-propagation-qualification.md`

Task 215 removes the wrapper/nested-child boundary entirely. One temporary Scheduled Task runs one harmless PowerShell script directly. The script itself persists start/identity evidence, periodic heartbeat evidence through the intended >=65-second lifetime, terminal marker, `intended-exit-code.txt=23`, then exits 23.

PASS requires:

- exactly one task start;
- direct process/task alive beyond 10 seconds and heartbeat through >=55 seconds;
- `DIRECT_START` and `DIRECT_END` persisted;
- intended exit-code file equals 23;
- terminal Scheduler state proven;
- `LastTaskResult=23` or exactly proven equivalent representation;
- exact temporary task cleanup;
- no CogentNexus/OpenClaw/SQLite/Discord product-state mutation.

No CogentNexus installer is authorized in Task 215. Installer qualification/install-over requires a later successor only after independent Task-215 PASS review.

## Discord budget

`0 Discord Sends`.

## Hard fence

No installer/install-over, no lifecycle command, no OpenClaw plugin/config mutation, no Gateway restart, no ownership/staging/transaction/backup edits, no SQLite writes, no provider/model/config mutation, no product source/test/workflow mutation, no Release/tag mutation, no force push, and no Discord traffic.
