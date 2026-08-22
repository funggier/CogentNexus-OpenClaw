# Codex Coordination Bootstrap

This is the one-time standing instruction for a Codex session or Scheduled task that executes CogentNexus work through the GitHub coordination layer.

## Standing instruction

Use `funggier/cogentnexus` branch `agent/v0.9.3-recovery-reality-tests` as the durable coordination channel with ChatGPT.

For coordination work:

1. GitHub coordination records outrank stale conversational memory.
2. Read `docs/operations/coordination/README.md`, `SIGNALS.md`, and `WATCH_MODE.md`.
3. On every manual signal or scheduled poll, synchronize safely and read the current remote `ACTIVE.md` again.
4. Execute only when `ACTIVE.md` says `READY_FOR_CODEX`.
5. Manual `ต่อ` may execute any READY task. Continuous watch mode may execute only when `ACTIVE.md` also says `Execution mode: AUTO`.
6. Read the exact active task and report contract before execution.
7. Obey every task-specific safety/precondition gate. If a gate is not satisfied, report `BLOCKED`; do not improvise dangerous fixes.
8. Write execution results only to the matching Codex-owned report under `docs/operations/coordination/reports/`, plus changes explicitly authorized by the task.
9. Commit and push normally. Never force-push coordination history.
10. After the report is pushed, stop that run. Do not invent or execute the next task.
11. Never repeat completed side effects when a matching report already exists.
12. `สถานะ` means synchronize/read/report status only.
13. `หยุด` means do not begin a new coordination task.
14. `หยุดเฝ้า` means pause/disable the continuous Scheduled task without altering CogentNexus runtime state.

The operator does not relay task bodies. ChatGPT publishes tasks/reviews in GitHub; Codex publishes local execution reports/evidence references in GitHub.

## Manual initial synchronization

After accepting this bootstrap, synchronize the branch and read `ACTIVE.md`.

For manual mode, do not execute until the operator sends:

```text
ต่อ
```

## Continuous watch setup

For unattended pickup, follow `WATCH_MODE.md` and create/enable a Codex Scheduled task in the local ChatGPT desktop app.

Do not claim continuous monitoring is active merely because the bootstrap was read. It is active only after the Scheduled task is confirmed enabled for the local CogentNexus project/worktree.
