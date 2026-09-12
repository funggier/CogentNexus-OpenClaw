# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-316`
Parent: `CNX-20260913-V095-FINALIZATION-BLOCKED`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `a986f3261b1570d1bcb1574d2458fe7068207a9c`
Candidate branch: `feat/v0.9.5-release-readiness-clean`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

v0.9.5 automated validation is green on the frozen candidate, but finalization is blocked because live provider-switch, idle-quiescence, and controlled-wake evidence have not yet been proven on the target runtime.

The previous coordination state was `COMPLETED` and explicitly required future work to use a new task/branch. This successor task now supplies that durable execution authority.

## Authorized next work

Hermes may install-over and enable the exact frozen candidate through supported repository-defined paths, then execute the documented live acceptance sequence:

1. exact-candidate installation/provenance verification;
2. Provider Switch Acceptance;
3. Idle Quiescence Acceptance for at least two supervisor cadences;
4. Controlled Actionable Wake using one durable work item;
5. evidence collection and report update.

This authority does not authorize merge, tag creation, GitHub Release publication, or unrelated system/configuration mutation.

## Hard fences

- Preserve candidate `a986f3261b1570d1bcb1574d2458fe7068207a9c` unless a separately proven defect requires a new candidate and full requalification.
- No credentials, API keys, tokens, cookies, or secrets may be recorded or exposed.
- No manual Ticket/SQLite/session/transcript/delivery mutation outside documented normal acceptance operations.
- No unrelated service, Scheduled Task, Gateway, provider-routing, or configuration mutation.
- Missing evidence remains `INDETERMINATE`; never infer PASS.
- Stop and report `BLOCKED` when an action exceeds the task's explicit scope.

## Release gate state at task start

```text
Automated Validation      PASS
Provider Switch           INDETERMINATE
Idle Quiescence           INDETERMINATE
Controlled Wake           INDETERMINATE
Finalization              BLOCKED
Merge                     None
Tag                       None
Release                   Not published
```
