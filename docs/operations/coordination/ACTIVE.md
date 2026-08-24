# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL`  
Task ID: `CNX-20260824-047`  
Updated: 2026-08-24 16:18 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Active task

[`tasks/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md`](tasks/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md)

## Predecessor report and review

[`reports/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`](reports/CNX-20260824-046-remove-legacy-and-fresh-install-current.md)

[`reviews/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`](reviews/CNX-20260824-046-remove-legacy-and-fresh-install-current.md)

Task 046 is reviewed `ACCEPT_SAFE_PREMUTATION_STOP` with result `BLOCKED_NATIVE_PLUGIN_INVENTORY_TIMEOUT`.

## Task 047 scope

Read-only diagnosis of the OpenClaw `plugins list --json` timeout:

- map installed OpenClaw `2026.7.1-2 (0790d9f)` to its exact upstream call path;
- inspect persisted registry/index/config/path metadata with secrets redacted;
- run at most three distinct bounded native CLI probes;
- use process-local lifecycle tracing and persisted-registry bypass only for comparison;
- if required, time offline synchronous boundaries from a temporary script;
- identify the first failing boundary or report bounded uncertainty.

## Authority

No new human authorization is required for this read-only diagnostic task. The operator must manually signal Codex because scheduled execution remains disabled.

Task 046 destructive removal/install authority is consumed. Task 047 authorizes no repair, removal, or installation.

## Safety

- Preserve legacy CogentNexus live state, OpenClaw, Ollama/models, Gateway, user data, AGENTS, scheduler, unrelated plugins/projects, primary repository, HermesAgent, Ecosystem, staged-capability-loop, and retained Procmon evidence.
- No plugin registry refresh, `doctor --fix`, config/state/database write, lifecycle action, Procmon, dump, ACL/ownership/antivirus change, or broad scan.
- A bounded timeout wrapper may terminate only the exact diagnostic child it created and its verified descendants.
- Publish exactly the one Task 047 report file.
