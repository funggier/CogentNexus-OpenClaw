# Coordination Signals

This file defines the minimal human trigger vocabulary for Codex when the repository coordination layer is being used.

The operator does not need to copy task instructions between ChatGPT and Codex. GitHub carries the durable task specification and report handoff.

## `ต่อ`

Meaning: **synchronize with the coordination branch and continue the currently authorized active task.**

When Codex receives only:

```text
ต่อ
```

Codex should:

1. locate the CogentNexus repository;
2. fetch `origin/agent/v0.9.3-recovery-reality-tests` without force-pushing or discarding local work;
3. read `docs/operations/coordination/README.md`;
4. read `docs/operations/coordination/ACTIVE.md` from the current coordination branch state;
5. read the active task and its required report contract;
6. verify all task preconditions before doing anything disruptive;
7. execute only the work authorized by that task;
8. write/update only the matching Codex-owned report under `reports/` plus any task-authorized evidence/changes;
9. commit and push the report/results normally;
10. stop after the report is pushed. Do **not** invent a next task and do not repeat a completed task.

If the active state is not `READY_FOR_CODEX`, Codex must not execute a disruptive task. It should report the observed coordination state and stop.

If the task is already represented by a completed report at the current GitHub head, Codex must not repeat side effects merely because the operator sent `ต่อ` again. It should report that the task is awaiting ChatGPT review or already complete.

## `สถานะ`

Meaning: **synchronize and report coordination status only. Do not execute the task.**

Codex should read `ACTIVE.md`, the matching report if one exists, and summarize the current handoff state without running disruptive commands.

## `หยุด`

Meaning: **do not begin any new coordination task.**

This signal does not replace CogentNexus runtime commands such as `cnx stop`; it controls only whether Codex starts new coordination work.

## Safety and authority

The human operator remains final authority. These signals are convenience triggers, not permission to bypass task-specific safety gates.

The durable task in GitHub always outranks assumptions from prior Codex conversation context. If the active task and remembered instructions differ, Codex follows the current GitHub coordination records or stops as `BLOCKED` when the conflict cannot be resolved safely.
