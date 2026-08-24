# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `CNX-20260824-046`  
Updated: 2026-08-24 15:02 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Active task

[`tasks/CNX-20260824-046-remove-legacy-and-fresh-install-current.md`](tasks/CNX-20260824-046-remove-legacy-and-fresh-install-current.md)

## Predecessor report and review

[`reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`](reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md)

[`reviews/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`](reviews/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md)

Task 045 is reviewed `ACCEPT_SAFE_PREMUTATION_STOP` with result `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`.

## Human authorization

The operator directed removal before reinstall, approved the narrowed design, and reconfirmed `1`.

Authorized outcome:

- externally back up and hash-verify proven legacy CogentNexus;
- enter native/PASSTHROUGH;
- remove only exact legacy launcher/skill/state/plugin/config/load-path/scheduled-task identities;
- require exact fresh classification;
- install reviewed current CogentNexus-OpenClaw v0.9.3 once;
- exact-verify new ownership/runtime and unrelated-data safety.

## Execution boundary

Task 046 is not install-over migration and must not run `clean-reinstall.ps1`.

The fresh installer may run once only after exact legacy removal and `fresh` classification. No destructive retry or automatic restore is authorized.

If native plugin inventory still times out, ownership/backup/handoff is unproved, or state is mixed/unowned, stop before removal.

## Safety

- “Clear” applies only to proven legacy CogentNexus identities.
- Preserve OpenClaw, Ollama, models, unrelated workspace/user data, and HermesAgent.
- No broad wildcard/parent-directory deletion or force-kill.
- No primary-repository checkout/reset/clean/worktree action.
- No Procmon/Task 027/038 access.
- No Ecosystem, staged-capability-loop, merge, tag, Release, or archive action.
- Scheduled ChatGPT/Codex execution remains operator-controlled.
