# Coordination Channel Status

**State:** `PREPARING_TASK_035`  
**Updated:** 2026-08-23 20:30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator  
**Execution trigger:** automatic watcher or manual `ต่อ`

## Participants and technical ownership

- **ChatGPT** — root-cause analysis, fix direction, exact task design, evidence review, and next-step decisions
- **Codex** — local-machine proof, bounded execution, validation, and execution reports
- **Human operator** — final authority and approval for destructive, elevated, or materially broader actions

Codex may perform cause analysis or design a fix only when the task explicitly states that ChatGPT lacks necessary local access or capability.

## Active transition

Task `CNX-20260823-034` is accepted as `PASS_SOURCE_CAPABILITY_MAPPED_NO_ACTOR`.

The human operator explicitly authorized Task `CNX-20260823-035` to use official Microsoft Sysinternals Process Monitor under its exact bounded scope. The Task 035 specification is published. `ACTIVE.md` is changed to `READY_FOR_CODEX` only after all ChatGPT-owned status records are consistent.

See [`ACTIVE.md`](ACTIVE.md).

## Task 035 boundary

Task 035 may:

- download the official Process Monitor ZIP into a task-specific temporary directory;
- verify SHA256, x64 identity, version, and valid Microsoft Authenticode signature;
- elevate only the verified `Procmon64.exe` if required;
- capture at most 10 minutes after proving an exact Task027 filesystem filter with filtered events dropped;
- retain filtered PML/CSV/config/provenance evidence locally until ChatGPT review.

Task 035 may not broadly capture the system, restore or touch the 382 absent paths, provoke activity, change watcher/Supervisor/task configuration, or touch CogentNexus/OpenClaw/Ollama runtime.

## Handoff rule

Codex must freshly read `ACTIVE.md`, the exact task, and the duplicate fence before execution. It publishes only the matching report and stops for ChatGPT review.

A repeated trigger must not repeat acquisition, trace, or any already-completed side effect when a matching report exists.

## Progress rule

During execution Codex reports meaningful progress approximately every 3 minutes and immediately after preflight, provenance verification, elevation/EULA, exact-filter proof, capture start/stop, export/cleanup, and blocker.
