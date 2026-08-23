# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `AUTO`  
Task ID: `CNX-20260823-035`  
Updated: 2026-08-23 20:31 ICT  
Owner: ChatGPT  
Executor: Codex

## Active task

[`tasks/CNX-20260823-035-capture-task027-procmon-attribution.md`](tasks/CNX-20260823-035-capture-task027-procmon-attribution.md)

## Predecessor review

[`reviews/CNX-20260823-034-trace-task027-filesystem-io-and-audit-source.md`](reviews/CNX-20260823-034-trace-task027-filesystem-io-and-audit-source.md)

Task 034 is `ACCEPT` as `PASS_SOURCE_CAPABILITY_MAPPED_NO_ACTOR`.

## Human authorization

The operator explicitly authorized:

`1 อนุญาต Task 035 ใช้ Procmon ตามขอบเขตนี้`

This authorization is fully bounded by the immutable Task 035 specification.

## Purpose

Task 035 acquires only the official portable Microsoft Sysinternals Process Monitor package, verifies SHA256/version/x64 identity and valid Microsoft Authenticode provenance, then attempts one exact-path filesystem trace of the Task027 worktree for at most 10 minutes.

ChatGPT owns cause/fix analysis. Codex performs proof and validation only.

## Mandatory capture gate

No recording may begin unless Codex proves that the exact Task027 path Include filter, filesystem-only scope, and drop-filtered-events state are loaded before capture.

If this cannot be proven, or if interactive elevation/filter setup is required, Codex stops with the exact defined blocker. It must not capture broadly and filter afterward.

## Safety boundary

No restoration/materialization/touch; no event provocation; no worktree or Git mutation; no watcher/Supervisor/task change; no CogentNexus/OpenClaw/Ollama runtime action; no process action except the verified task-owned Procmon lifecycle; no boot logging, PsExec, UAC bypass, persistent service, process-tree operation, force push, merge, tag, or release.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after duplicate/identity preflight, official-download provenance, elevation/EULA, exact-filter proof, capture start/stop, export/cleanup, actor evidence, or blocker. Progress updates are not pause points except at an explicit safety or interactive gate.

## Duplicate-execution fence

If `docs/operations/coordination/reports/CNX-20260823-035-capture-task027-procmon-attribution.md` already exists at freshly fetched HEAD, do not repeat download, extraction, launch, trace, termination, export, or cleanup. Stop awaiting ChatGPT review.
