# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `V0.9.5_FINAL_ACCEPTANCE_RETRY`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260913-317`
Parent: `CNX-20260913-316`
Executor: `Hermes`
Reviewer: `ChatGPT`
Release candidate: `434b27185f7afd17d8cffeede9c016378df0a6aa`
Candidate branch: `fix/v0.9.5-final-acceptance-installer-cli`
Authority branch: `coord/v0.9.5-final-acceptance`

## Current position

The original v0.9.5 candidate `a986f3261b1570d1bcb1574d2458fe7068207a9c` exposed a real installer CLI defect during authorized live acceptance. The defect was repaired with a test-first sequence and the repaired acceptance target is now `434b27185f7afd17d8cffeede9c016378df0a6aa`.

The repaired candidate independently requalified repository tests, but the live install attempt reached a Gateway restart/probe timeout. The acceptance machine was left in native passthrough with CNX disabled. Provider Switch, Idle Quiescence, and Controlled Wake therefore remain unproven.

This successor task supplies the durable authority required for a bounded retry.

## Authorized next work

Hermes may:

1. diagnose the prior Gateway restart/probe timeout using bounded diagnostics first;
2. use the minimum supported recovery path needed to restore a healthy acceptance runtime;
3. install-over and verify the exact repaired candidate;
4. enable the plugin through the supported path;
5. execute Provider Switch Acceptance;
6. execute Idle Quiescence Acceptance for at least two supervisor cadences;
7. execute Controlled Actionable Wake with exactly one durable work item;
8. collect and publish evidence.

## Release gate state at retry start

```text
Original Candidate            RETIRED / historical
Repaired Candidate            434b27185f7afd17d8cffeede9c016378df0a6aa
Automated Validation          PASS
Repaired Install              BLOCKED by Gateway restart/probe timeout
Provider Switch               INDETERMINATE
Idle Quiescence               INDETERMINATE
Controlled Wake               INDETERMINATE
Finalization                  BLOCKED
PR #38                        OPEN / UNMODIFIED
Merge                         None
Tag                           None
Release                       Not published
```

## Hard fences

- Do not modify or merge PR #38 in this task.
- Do not create, move, or delete `v0.9.5` tag.
- Do not publish GitHub Release.
- Do not force-push.
- Do not expose, record, or mutate secrets or credentials.
- Do not perform unrelated system/service/Scheduled Task/provider/configuration changes.
- Do not manually mutate Ticket/SQLite/session/transcript/delivery state outside normal documented acceptance operations.
- Missing evidence remains `INDETERMINATE`.
- Stop and report `BLOCKED` when the required action exceeds this authority.
