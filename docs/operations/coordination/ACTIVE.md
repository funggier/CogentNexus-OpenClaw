# Active Coordination Task

Status: `BLOCKED_HUMAN_DECISION`  
Execution mode: `MANUAL_AUTHORIZATION_REQUIRED`  
Task ID: `CNX-20260823-036`  
Updated: 2026-08-23 23:29 ICT  
Owner: ChatGPT  
Executor: none until authorized

## Report and review

[`reports/CNX-20260823-036-configure-task027-procmon-pmc.md`](reports/CNX-20260823-036-configure-task027-procmon-pmc.md)

[`reviews/CNX-20260823-036-configure-task027-procmon-pmc.md`](reviews/CNX-20260823-036-configure-task027-procmon-pmc.md)

Task 036 is reviewed `BLOCKED` as `BLOCKED_CLEANUP_UNVERIFIED`.

## Proven boundary

The verified retained Procmon 4.1 binary was launched once with `/NoConnect /NoFilter /AcceptEula`. Elevated UI control was unavailable, so no filter was configured and no `.PMC` was exported.

No `.PMC`, `.PML`, `.CSV`, backing file, target stimulation, restoration, worktree/Git mutation, watcher/Supervisor change, or CogentNexus/OpenClaw/Ollama runtime action was recorded.

After the operator closed the visible GUI, task-owned Procmon PIDs 51880 and 59348 remained. No force or process-tree kill was used.

## Human decision required

Decide whether to authorize one cleanup-only Task 037.

The recommended phase would revalidate exact ownership and absence of any other Procmon instance, then use the verified retained `Procmon64.exe /Terminate` exactly once as a graceful Procmon shutdown. It would verify zero Procmon processes and no unexpected driver/service/capture artifacts afterward.

It would not authorize `Stop-Process`, `taskkill`, process-tree/force kill, reboot, capture, filter configuration, restoration, or runtime action.

No cleanup command, repeated Task 036 attempt, PMC configuration, or trace is authorized by the current state.

## Duplicate-execution fence

Do not repeat Task 036, relaunch Procmon, modify the retained evidence, or attempt any cleanup while this human-decision gate is active.
