# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO_WITH_UAC_GATE`  
Task ID: `CNX-20260823-037`  
Updated: 2026-08-23 23:34 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-037-graceful-cleanup-task036-procmon.md`](tasks/CNX-20260823-037-graceful-cleanup-task036-procmon.md)

## Predecessor report and review

[`reports/CNX-20260823-036-configure-task027-procmon-pmc.md`](reports/CNX-20260823-036-configure-task027-procmon-pmc.md)

[`reviews/CNX-20260823-036-configure-task027-procmon-pmc.md`](reviews/CNX-20260823-036-configure-task027-procmon-pmc.md)

Task 036 is reviewed `BLOCKED` as `BLOCKED_CLEANUP_UNVERIFIED`.

## Human authorization

The operator explicitly authorized:

`อนุญาต Task 037 ตรวจสอบ ownership และใช้ Procmon64.exe /Terminate ได้ 1 ครั้ง เฉพาะเมื่อยืนยันว่าไม่มี Procmon อื่น ห้าม force-kill และห้าม capture`

This authorization is fully bounded by the immutable Task 037 specification.

## Purpose

Resolve the residual Task 036 Procmon state without capture or force.

Reported residual identity:

- PID 51880 — exact retained `Procmon64.exe /NoConnect /NoFilter /AcceptEula`
- PID 59348 — child of PID 51880

## Mandatory ownership gate

Freshly inventory every Procmon process.

- If none remain: do not invoke `/Terminate`; verify and report clean.
- If every surviving Procmon process is exactly and exclusively attributable to Task 036, the verified retained `Procmon64.exe /Terminate` may be invoked once.
- If any extra process, changed PID identity/ancestry, PID reuse, unreadable ownership, unexpected capture/config artifact, or uncertainty exists: block without action.

PID or process name alone is insufficient proof.

## One-shot fence

The exact retained executable may be invoked with `/Terminate` at most once across Task 037.

Never retry after timeout, uncertain outcome, UAC interruption, or failure.

No `Stop-Process`, `taskkill`, Task Manager End Task, WMIC/CIM termination, process-tree/force kill, service/driver stop/delete, reboot, logoff, PsExec, UAC bypass, or policy change.

## Safety boundary

No capture, Procmon GUI configuration launch, `.PMC` creation/overwrite, PML/backing file/CSV, target touch/stimulation, restoration/materialization, worktree/Git mutation, watcher/Supervisor change, retained-evidence cleanup, CogentNexus/OpenClaw/Ollama runtime action, force push, merge, tag, or release.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after inventory, binary identity proof, ownership decision, before the one-shot graceful action, after bounded poststate verification, and at any blocker.

## Duplicate-execution fence

If the matching Task 037 report exists at freshly fetched HEAD, do not repeat inventory for action, `/Terminate`, or any side effect. Stop awaiting ChatGPT review.
