# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `CNX-20260824-049`  
Updated: 2026-08-24 18:58 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 049 gate.

## Active task

[`tasks/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md`](tasks/CNX-20260824-049-backup-remove-legacy-stop-at-fresh.md)

## Predecessor report and review

[`reports/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md`](reports/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md)

[`reviews/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md`](reviews/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md)

Task 048 is reviewed `ACCEPT_BOUNDED_NONREPRODUCTION`. Native registry/list returned valid JSON and identified exact legacy plugin ownership; no repair was justified.

## Human authorization

The operator approved option `1` for the successor design:

- create a verified external backup;
- if the native inventory gate fails again, use the bounded repair ladder;
- hand off legacy management to PASSTHROUGH/native;
- uninstall/remove only proven legacy CogentNexus;
- reach and prove CogentNexus classifier `mode=fresh`;
- stop and report before any current CogentNexus-OpenClaw installation.

## Mandatory stop

Task 049 must not invoke `scripts/install.ps1`, `clean-reinstall.ps1`, any Release installer, or create current-product artifacts.

Installation requires report review, a successor task, and new explicit operator approval.

## Safety

Preserve OpenClaw/Gateway, Ollama/models, user data, AGENTS, unrelated plugins/projects, primary repository, HermesAgent, Ecosystem, staged-capability-loop, and retained Procmon evidence.

No OpenClaw upgrade/reinstall, manual SQLite edit, broad deletion, force kill, or automatic restore. The final report commit must be report-only.
