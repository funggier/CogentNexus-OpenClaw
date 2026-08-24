# Active Coordination Task

Status: `READY_FOR_CODEX`  
Execution mode: `MANUAL_REPOSITORY_ONLY`  
Task ID: `CNX-20260824-051`  
Updated: 2026-08-24 19:18 ICT  
Owner: ChatGPT  
Executor: Codex after operator's manual signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` is project narrative and is not a Task 051 gate.

## Active task

[`tasks/CNX-20260824-051-align-canonical-check-help.md`](tasks/CNX-20260824-051-align-canonical-check-help.md)

## Task 050 report and review

[`reports/CNX-20260824-050-fresh-install-current-v093.md`](reports/CNX-20260824-050-fresh-install-current-v093.md)

[`reviews/CNX-20260824-050-fresh-install-current-v093.md`](reviews/CNX-20260824-050-fresh-install-current-v093.md)

Task 050 is reviewed `ACCEPT_WITH_FOLLOWUP_REQUIRED` as `ACCEPT_INSTALLED_RUNTIME_WITH_HELP_DEFECT`.

## Human authorization

The operator authorized immediate Codex execution:

> `ให้ codex ทำเลยก็ได้ครับ แล้วค่อยรายงานงาน`

Scheduled execution remains disabled. Codex starts from the operator's manual signal.

## Root cause and bounded repair

The check engine correctly accepts canonical component `cogentnexus-openclaw` and rejects generic `cogentnexus`, but base/v0.9.3 CLI help and usage still advertise the invalid generic command.

Task 051 must use TDD to correct only current operator-facing help/usage and add namespace-lint regression coverage.

Do not add a generic compatibility alias.

## Live-machine boundary

The live CogentNexus-OpenClaw v0.9.3 installation is accepted as materialized and healthy under canonical checks.

Task 051 is repository-only. It must not access or mutate the live installation, OpenClaw, Gateway, Ollama, scheduler, controller, plugin registry/config, Task 049 backup, primary repository, or excluded projects/evidence.

After Task 051 is reviewed, updating the installed copy requires a separate explicit human decision.
