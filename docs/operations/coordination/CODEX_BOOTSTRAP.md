# Codex Coordination Bootstrap

This is the one-time standing instruction for a Codex session that will execute CogentNexus work through the GitHub coordination layer.

## Standing instruction

Use `funggier/cogentnexus` branch `agent/v0.9.3-recovery-reality-tests` as the durable coordination channel with ChatGPT.

For coordination work:

1. GitHub coordination records outrank stale conversational memory.
2. Read `docs/operations/coordination/README.md` and `SIGNALS.md`.
3. On every operator signal `ต่อ`, fetch/synchronize safely and read `ACTIVE.md` again from the current branch state.
4. Execute work only when `ACTIVE.md` says `READY_FOR_CODEX`.
5. Read the exact active task and its report contract before execution.
6. Obey task-specific safety/precondition gates. If they are not satisfied, report `BLOCKED`; do not improvise dangerous fixes.
7. Write execution results only to the matching Codex-owned report under `docs/operations/coordination/reports/`, plus any source/evidence changes explicitly authorized by the task.
8. Commit and push results normally. Never force-push coordination history.
9. After the report is pushed, stop. Do not invent or execute the next task.
10. If `ต่อ` is received again while the current task is awaiting ChatGPT review, do not repeat completed side effects. Report that review is pending and stop.
11. `สถานะ` means synchronize/read/report status only. Do not execute disruptive work.
12. `หยุด` means do not begin a new coordination task.

The operator should not need to relay the task body between ChatGPT and Codex. ChatGPT publishes task specifications/reviews in GitHub; Codex publishes local execution reports/evidence references in GitHub.

## Initial synchronization

After accepting this bootstrap, synchronize the coordination branch and read `docs/operations/coordination/ACTIVE.md`.

Do not execute the active task until the operator sends the signal:

```text
ต่อ
```
