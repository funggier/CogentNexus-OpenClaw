# Active Coordination Task

Status: `BLOCKED_HUMAN_DECISION`  
Execution mode: `MANUAL_AUTHORIZATION_REQUIRED`  
Task ID: `CNX-20260823-035`  
Updated: 2026-08-23 21:12 ICT  
Owner: ChatGPT  
Executor: none until authorized

## Report and review

[`reports/CNX-20260823-035-capture-task027-procmon-attribution.md`](reports/CNX-20260823-035-capture-task027-procmon-attribution.md)

[`reviews/CNX-20260823-035-capture-task027-procmon-attribution.md`](reviews/CNX-20260823-035-capture-task027-procmon-attribution.md)

Task 035 is `BLOCKED` as `BLOCKED_EXACT_FILTER_NOT_PROVABLE`.

## Proven boundary

The official Process Monitor package was downloaded once to the retained Task 035 temporary directory. ZIP and `Procmon64.exe` hashes, version 4.1, and valid Microsoft Authenticode provenance were recorded.

Procmon was not launched. No EULA, registry, driver/service, capture, restoration, event provocation, watcher/Supervisor/runtime action, or Git/worktree mutation occurred.

## Human decision required

Decide whether to authorize one interactive configuration-only task using the already verified retained `Procmon64.exe`.

The configuration-only phase would:

- allow UAC/EULA only for the verified retained executable;
- open Procmon with capture disabled;
- configure the exact Task 027 Path-begins-with Include filter;
- restrict capture classes to filesystem activity;
- disable Registry, Network, and Profiling activity;
- enable Drop Filtered Events;
- save a task-specific `.PMC` inside the retained Task 035 directory;
- close Procmon and prove no residual process, capture, or unexpected driver/service state.

That phase would not start or retain a capture. A separate later task would inspect the saved `.PMC` before authorizing the bounded trace.

No interactive configuration or capture is authorized by the current state.

## Duplicate-execution fence

Do not repeat Task 035 download/acquisition. Do not launch Procmon or remove the retained Task 035 directory while this human-decision gate is active.
