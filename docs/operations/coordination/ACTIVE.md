# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_BOUNDED_COMMAND_FIX`  
Task ID: `CNX-20260824-048`  
Updated: 2026-08-24 18:02 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Authoritative coordination files

Only these full repository paths are execution gates:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 048 gate.

## Active task

[`tasks/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md`](tasks/CNX-20260824-048-diagnose-openclaw-plugin-inventory-timeout.md)

## Predecessor report and review

[`reports/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md`](reports/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md)

[`reviews/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md`](reviews/CNX-20260824-047-diagnose-openclaw-plugin-inventory-timeout.md)

Task 047 is reviewed `ACCEPT_SAFE_SPECIFICATION_STOP`. It ran no plugin probes because an abbreviated path allowed the non-authoritative project STATUS file to be selected.

## Task 048 scope

- localize the exact OpenClaw `plugins list --json` failure boundary;
- use at most three bounded native read-only probes plus safe offline microprobes if needed;
- if root cause is command selection, arguments, invocation, output parsing, timeout wrapper, or a repository-owned command wrapper, apply the smallest correction and prove it once;
- otherwise report the localized cause or bounded uncertainty without repair.

## Human authority

The operator approved option `1`: command-surface correction may proceed without another pause after proof.

This does not authorize `registry --refresh`, `doctor --fix`, live OpenClaw config/registry/database/global-package changes, OpenClaw upgrade, plugin mutation, CogentNexus lifecycle, legacy removal, or fresh installation.

Task 046 destructive authority remains consumed. A later removal/fresh-install attempt requires a new task and new explicit operator authorization.

## Safety

Preserve legacy CogentNexus state, OpenClaw/Gateway, Ollama/models, user data, AGENTS, scheduler, unrelated plugins/projects, primary repository, HermesAgent, Ecosystem, staged-capability-loop, and retained Procmon evidence.

A timeout wrapper may terminate only the exact diagnostic child it created and its verified descendants. The final report commit must be report-only.
