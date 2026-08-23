# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260824-038`  
Updated: 2026-08-24 00:32 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260824-038-validate-operator-created-task027-procmon-pmc.md`](tasks/CNX-20260824-038-validate-operator-created-task027-procmon-pmc.md)

## Predecessor report and review

[`reports/CNX-20260823-037-graceful-cleanup-task036-procmon.md`](reports/CNX-20260823-037-graceful-cleanup-task036-procmon.md)

[`reviews/CNX-20260823-037-graceful-cleanup-task036-procmon.md`](reviews/CNX-20260823-037-graceful-cleanup-task036-procmon.md)

Task 037 is reviewed `ACCEPT` as `PASS_ALREADY_CLEAN_NO_TERMINATE`.

## Human authorization

The operator explicitly authorized:

`ได้เลยครับ สร้าง task ให้ codex ได้เลย`

This authorizes Task 038 validation and its matching report only.

## Purpose

Independently validate the operator-created exact-path Procmon `.PMC` artifact without launching Procmon or starting capture.

Required artifact:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\task027-exact-filesystem-dropfiltered.pmc`

Required size: `2051 bytes`

Required SHA256:

`61F3BBB57B65F8DC708E66BC15B5B808AB44E9DC770799E8C32ED40724AE6CBC`

Codex may inspect only the exact artifact bytes/metadata, narrow Procmon process/driver/service state, and the retained Task 035 directory for unexpected capture/config artifacts.

## Safety boundary

Do not launch Procmon or use `/LoadConfig`, `/OpenLog`, `/BackingFile`, or `/Terminate`.

No capture, PML, CSV, backing file, target stimulation/access, restoration/materialization, Git index/worktree mutation, watcher/Supervisor change, process termination, retained-evidence cleanup, or CogentNexus/OpenClaw/Ollama runtime/recovery/lifecycle action.

A PASS validates only the saved configuration artifact. It does not authorize capture.

## Duplicate-execution fence

If the matching Task 038 report exists at freshly fetched HEAD, do not repeat local inventory or read the `.PMC` again. Stop awaiting ChatGPT review.
