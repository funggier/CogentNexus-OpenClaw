# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO_WITH_INTERACTIVE_GATE`  
Task ID: `CNX-20260823-036`  
Updated: 2026-08-23 21:25 ICT  
Owner: ChatGPT  
Executor: Codex with human UAC/GUI assistance

## Active task

[`tasks/CNX-20260823-036-configure-task027-procmon-pmc.md`](tasks/CNX-20260823-036-configure-task027-procmon-pmc.md)

## Predecessor report and review

[`reports/CNX-20260823-035-capture-task027-procmon-attribution.md`](reports/CNX-20260823-035-capture-task027-procmon-attribution.md)

[`reviews/CNX-20260823-035-capture-task027-procmon-attribution.md`](reviews/CNX-20260823-035-capture-task027-procmon-attribution.md)

Task 035 is `BLOCKED` as `BLOCKED_EXACT_FILTER_NOT_PROVABLE`; the blocker is resolved only for the newly authorized configuration-only phase.

## Human authorization

The operator explicitly authorized:

`1 อนุญาต Task 036 ตั้งค่า Procmon .PMC แบบโต้ตอบเท่านั้น ห้ามเริ่ม capture`

This authorization is fully bounded by the immutable Task 036 specification.

## Purpose

Use the already verified retained Microsoft-signed `Procmon64.exe` to create one exact-path, filesystem-only, Drop-Filtered-Events `.PMC` while capture remains inactive for the entire task.

A later separate task must inspect and validate the saved `.PMC` before any capture is considered.

## Mandatory no-capture gate

Launch only with the documented:

`/NoConnect /NoFilter /AcceptEula`

Before configuration, visually prove Capture Events is inactive/disconnected, zero event rows are present, the event counter is not advancing, and no PML/backing file exists.

If capture is active or no-capture state is uncertain at any point, stop with `BLOCKED_NO_CAPTURE_GUARANTEE`. Do not filter or save captured events.

## Exact configuration

- `Path begins with C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027` — Include
- File System Activity — enabled
- Registry Activity — disabled
- Network Activity — disabled
- Process and Thread Activity — disabled
- Profiling Events — disabled
- Drop Filtered Events — enabled
- Boot logging/backing file/capture — disabled

Export exactly:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\task027-exact-filesystem-dropfiltered.pmc`

Then close Procmon normally and prove a clean poststate.

## Safety boundary

No capture, PML, backing file, CSV, target touch/stimulation, restoration/materialization, worktree/Git mutation, watcher/Supervisor/task/config change, CogentNexus/OpenClaw/Ollama runtime action, process-tree operation, force-kill, boot logging, PsExec, UAC bypass, policy change, reboot, force push, merge, tag, or release.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after preflight, before UAC, after GUI no-capture proof, after exact configuration proof, after `.PMC` export, after normal close/poststate, and at any blocker.

Progress updates are not pause points except at UAC/interactive or defined safety gates.

## Duplicate-execution fence

If the matching Task 036 report exists at freshly fetched HEAD, do not repeat any Task 036 action.

If the exact local `.PMC` already exists without a report, do not overwrite or trust it; stop with `BLOCKED_CONFIG_ALREADY_EXISTS`.

Do not repeat Task 035 download/acquisition or remove the retained Task 035 directory.
