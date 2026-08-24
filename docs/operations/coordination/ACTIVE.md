# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_WITH_HUMAN_GATE`  
Task ID: `CNX-20260824-054`  
Updated: 2026-08-24 19:59 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 054 gate.

## Active task

[`tasks/CNX-20260824-054-repeat-install-over-v093-acceptance.md`](tasks/CNX-20260824-054-repeat-install-over-v093-acceptance.md)

## Predecessor disposition

Task 053 is reviewed `ACCEPT` as:

`ACCEPT_RECONCILIATION_CURRENT_TASK050_HEALTHY_TASK052_UNACCEPTED`

Task 052 is superseded and unaccepted. Do not rerun Task 052.

## Human authorization

The operator authorized one new install-over when Task 052 evidence could not be recovered.

## Authorized operation

Run the default installer exactly once from a fresh isolated Task 051 source clone against the healthy current `mode=upgrade` installation, retain the exact child exit code, verify preservation/runtime, and publish/remote-verify the Task 054 report.

Temporary evidence and the isolated clone must remain until remote report verification succeeds.

## Safety

No second installer or retry, clean/fresh reinstall, migration, reset, uninstall, manual repair/restore, force-kill, broad cleanup, excluded-system mutation, merge, tag, or release publication.

