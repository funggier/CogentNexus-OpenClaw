# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-23 21:25 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator  
**Execution trigger:** automatic watcher or manual `ต่อ`

## Participants and technical ownership

- **ChatGPT** — root-cause analysis, fix direction, exact task design, evidence review, and next-step decisions
- **Codex** — local-machine proof, bounded execution, validation, and execution reports
- **Human operator** — final authority and approval for destructive, elevated, interactive, or materially broader actions

Codex may perform cause analysis or design a fix only when the task explicitly states that ChatGPT lacks necessary local access or capability.

## Task 035 outcome

Task `CNX-20260823-035` is reviewed as `BLOCKED_EXACT_FILTER_NOT_PROVABLE`.

The official Process Monitor package was downloaded once and verified as version 4.1 with valid Microsoft Authenticode provenance. Procmon was not launched and no capture occurred.

## Human authorization for Task 036

The operator explicitly authorized:

`1 อนุญาต Task 036 ตั้งค่า Procmon .PMC แบบโต้ตอบเท่านั้น ห้ามเริ่ม capture`

Task `CNX-20260823-036` is published as a configuration-only phase using the retained verified `Procmon64.exe`.

It permits:

- UAC/EULA only for the exact retained Microsoft-signed binary;
- documented `/NoConnect /NoFilter /AcceptEula` launch;
- visual proof that capture is inactive before configuration;
- one exact Task 027 Path-begins-with Include rule;
- filesystem activity only, with Registry, Network, Process/Thread, and Profiling disabled;
- Drop Filtered Events;
- export of one task-specific `.PMC`;
- normal close and clean poststate proof.

It does not permit capture, PML/backing file, target stimulation/touch, restoration, watcher/Supervisor changes, or CogentNexus/OpenClaw/Ollama runtime action.

A later separate task must inspect and validate the `.PMC` before any bounded trace.

## Handoff and duplicate fence

Codex must freshly read [`ACTIVE.md`](ACTIVE.md), the exact [Task 036](tasks/CNX-20260823-036-configure-task027-procmon-pmc.md), the Task 035 report/review, and the duplicate/partial-execution fence before action.

Do not repeat Task 035 acquisition. If the Task 036 report or local output `.PMC` already exists, follow the exact non-repeat/blocker rules.

## Progress rule

During execution Codex reports meaningful progress approximately every 3 minutes and immediately after preflight, before UAC, after GUI no-capture proof, after filter/config proof, after export, after close/poststate, and at any blocker.
