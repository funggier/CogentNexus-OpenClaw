# Task Resumption

Use before risky or long-running work and whenever an interrupted task exists.

## Checkpoint

Write an atomic entry to `memory/interrupted-tasks.json` containing task ID, objective, state, completed steps, current/next action, timestamp, retry limit, and retry count. Prefer:

```powershell
python skills/cogentnexus/scripts/task_state.py checkpoint --task-id <id> --task "<objective>" --next-action "<next>"
```

Checkpoint after every material verified step, not after every trivial action.

## Resume

On session startup or task continuation:

1. Inspect in-progress entries older than five minutes.
2. Confirm the task was not explicitly abandoned and does not conflict with the current user request.
3. Re-read affected state and verify completed work.
4. Resume the smallest executable next action.
5. Retry transient failures within the stored limit; diagnose before changing strategy.
6. Remove the entry after verified completion.

Do not silently resume an unrelated stale task during an active user request. Surface a conflict when resumption could materially interfere.

## Failure-specific checks

- File edit: re-read and compare expected state.
- Command: confirm whether the process still exists before rerunning.
- Multi-file change: inventory completed files, then continue in dependency order.
- External operation: verify remote state before retrying to avoid duplication.