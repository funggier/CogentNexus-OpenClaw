# Codex Continuous Coordination Watch Mode

This file defines the standing unattended polling mode for CogentNexus GitHub coordination.

## Purpose

After one explicit operator setup/enable action, Codex checks the coordination branch repeatedly and executes newly authorized tasks without requiring the operator to send `ต่อ` for every handoff.

This mode removes repeated human relay work. It does not remove task-specific safety gates or allow Codex to invent project work.

## Supported execution model

Use a Codex Scheduled task in the ChatGPT desktop app when local Windows access is required.

- Run inside the CogentNexus local project or a dedicated Git worktree.
- Use a one-minute recurrence when near-immediate pickup is desired.
- Keep the Windows machine powered on and the ChatGPT desktop app running.
- Prefer a dedicated worktree so unfinished local changes are isolated.
- Use the narrowest sandbox/permissions that satisfy the active task.
- Do not claim the watch is active until the Scheduled task is confirmed enabled.

A normal interactive chat does not remain a permanent background watcher merely because it was told to wait.

## Poll cycle

On every scheduled run:

1. fetch `origin/agent/v0.9.3-recovery-reality-tests` safely;
2. read this file, `CODEX_BOOTSTRAP.md`, `SIGNALS.md`, and the current remote `ACTIVE.md`;
3. if `ACTIVE.md` is not `READY_FOR_CODEX`, exit without changes;
4. if `Execution mode` is not `AUTO`, exit without executing the task;
5. read the exact active task, matching report state, and task-specific safety gates;
6. if a matching completed report already exists, do not repeat any side effect; exit awaiting ChatGPT review;
7. execute only the exact active task;
8. publish the matching Codex-owned report/evidence references;
9. stop the current run after the report is pushed.

A later scheduled run begins a fresh synchronization cycle. Codex must never carry a stale task pointer across cycles.

## Automatic execution authority

`Execution mode: AUTO` in `ACTIVE.md` means the operator authorizes Codex to begin that exact task automatically when the watcher detects it.

It does not authorize:

- bypassing a precondition;
- widening task scope;
- force-pushing;
- discarding unrelated local work;
- repeating completed external side effects;
- inventing a successor task;
- overriding a task's explicit confirmation or safety requirements.

If a task cannot complete safely without new human authority, publish `BLOCKED` and stop that run.

## Stop and pause

The operator can pause the Scheduled task from the Scheduled view.

The coordination signal `หยุดเฝ้า` means disable or pause the continuous Scheduled task. It does not issue `cnx stop` and does not alter CogentNexus runtime state.

## Reporting

No-op polling cycles should not create commits or reports.

A run creates/updates the matching report only when it actually begins an authorized task or must record a meaningful `BLOCKED` result.
