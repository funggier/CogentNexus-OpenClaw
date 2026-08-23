# Coordination Channel Status

**State:** `PREPARING_TASK_037`  
**Updated:** 2026-08-23 23:34 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator  
**Execution trigger:** automatic watcher or manual `ต่อ`

## Participants and technical ownership

- **ChatGPT** — root-cause analysis, fix direction, exact task design, evidence review, and next-step decisions
- **Codex** — local-machine proof, bounded execution, validation, and execution reports
- **Human operator** — final authority and approval for destructive, elevated, interactive, or materially broader actions

Codex may perform cause analysis or design a fix only when the task explicitly states that ChatGPT lacks necessary local access or capability.

## Task 036 outcome

Task `CNX-20260823-036` is reviewed `BLOCKED` as `BLOCKED_CLEANUP_UNVERIFIED`.

No filter, `.PMC`, `.PML`, `.CSV`, backing file, capture artifact, target stimulation, worktree/runtime action, or force kill was recorded. Task-owned PIDs 51880 and 59348 remained after the visible GUI was closed.

## Human authorization for Task 037

The operator explicitly authorized:

`อนุญาต Task 037 ตรวจสอบ ownership และใช้ Procmon64.exe /Terminate ได้ 1 ครั้ง เฉพาะเมื่อยืนยันว่าไม่มี Procmon อื่น ห้าม force-kill และห้าม capture`

Task `CNX-20260823-037` is published as cleanup-only.

It must first inventory every Procmon process and prove exclusive Task 036 ownership. If zero Procmon processes exist, it skips `/Terminate` and verifies clean poststate. If ownership is exact and exclusive, it may invoke the verified retained `Procmon64.exe /Terminate` once only.

It does not permit a second `/Terminate`, `Stop-Process`, `taskkill`, Task Manager End Task, process-tree/force kill, service/driver deletion, reboot, capture, filter/PMC configuration, restoration, retained-evidence cleanup, or CogentNexus/OpenClaw/Ollama runtime action.

## Handoff and duplicate fence

Codex must freshly read [`ACTIVE.md`](ACTIVE.md), exact [Task 037](tasks/CNX-20260823-037-graceful-cleanup-task036-procmon.md), Task 036 report/review, and the one-shot fence before action.

If the matching Task 037 report exists, do not repeat any action. If ownership is ambiguous or any unrelated Procmon exists, block without invoking `/Terminate`.

## Progress rule

Report meaningful progress approximately every 3 minutes and immediately after process inventory, retained binary verification, ownership decision, before the one-shot command, after poststate verification, and at any blocker.
