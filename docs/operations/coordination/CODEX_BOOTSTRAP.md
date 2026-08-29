# Hermes/Codex Coordination Bootstrap

Updated: 2026-08-30 ICT

This is the standing instruction for an authorized Hermes or Codex session/Scheduled task that executes CogentNexus-OpenClaw work through the GitHub coordination layer.

## Standing instruction

Use repository `funggier/CogentNexus-OpenClaw` and current stabilization branch `agent/v0.9.3-full-stabilization` as the durable coordination channel with ChatGPT.

Canonical READY state: `READY_FOR_HERMES`.  
Executor role: `Hermes/Codex`.

Read [`EXECUTION_OWNERSHIP.md`](EXECUTION_OWNERSHIP.md). Hermes/Codex is the local/live executor lane; repository/source/test/CI work stays with ChatGPT by default unless the active task explicitly delegates it.

For coordination work:

1. The current **remote working branch** outranks stale conversational memory and any stale local checkout.
2. Read `README.md`, `EXECUTION_OWNERSHIP.md`, `SIGNALS.md`, and `WATCH_MODE.md`.
3. On every manual signal or scheduled poll, fetch/synchronize the named remote branch and verify the remote branch HEAD first.
4. Read remote `ACTIVE.md` and `STATUS.md` from that revision before treating local coordination files as current.
5. Compare the local checkout/worktree to remote HEAD. If local state is stale or uncertain, do not claim the remote gate is stale.
6. If a local checkout contains uncommitted/uncertain work, do not reset or overwrite it merely to synchronize. Prefer a fresh clone/worktree from verified remote HEAD.
7. Execute only when remote `ACTIVE.md` says `READY_FOR_HERMES` and the exact task authorizes the requested work.
8. Manual `ต่อ` may execute any READY delegated task. Continuous watch mode may execute only when `ACTIVE.md` also says `Execution mode: AUTO`.
9. Read the exact active task and report contract before execution.
10. Obey every task-specific safety/precondition gate. If a gate is not satisfied, follow `PROBLEM_LOOP.md`; do not improvise dangerous fixes.
11. Do not duplicate repository/source/test/CI work already being performed by ChatGPT unless the active task explicitly assigns that implementation to Hermes/Codex.
12. Write execution results only to the matching executor-owned report under `docs/operations/coordination/reports/`, plus changes explicitly authorized by the task.
13. Commit and push normally. Never force-push coordination history.
14. Before pushing, re-fetch/race-check the remote branch. Do not overwrite concurrent ChatGPT or executor work.
15. After the report is pushed, stop that run. Do not invent or execute the next task. ChatGPT independently reviews actionable reports and publishes the next disposition/task if needed.
16. Never repeat completed side effects when a matching report already exists.
17. `สถานะ` means synchronize/read/report status only.
18. `หยุด` means do not begin a new coordination task.
19. `หยุดเฝ้า` means pause/disable continuous Scheduled execution without altering CogentNexus-OpenClaw runtime state.

The operator does not relay task bodies. ChatGPT performs repository-capable work and publishes tasks/reviews in GitHub; Hermes/Codex is invoked for the narrow local/live remainder and publishes matching machine execution reports/evidence references.

## Local/live escalation scope

Typical Hermes/Codex work includes real Windows runtime state, OpenClaw/Ollama/Gateway processes, supported install/uninstall/reset/restart operations, real filesystem topology, real Dashboard/browser semantic interaction, hardware/device integration, local permissions, and other machine-specific acceptance evidence.

If GitHub Actions can prove the required behavior adequately, a local executor run is not required merely for duplication.

## Manual initial synchronization

After accepting this bootstrap, fetch the current authorized remote branch, verify its remote HEAD, and read remote `ACTIVE.md`/`STATUS.md`.

For manual mode, do not execute until the operator sends:

```text
ต่อ
```

## Continuous watch setup

For unattended pickup, follow `WATCH_MODE.md` and create/enable an authorized Scheduled task in the local ChatGPT desktop app.

Do not claim continuous monitoring is active merely because the bootstrap was read. It is active only after the Scheduled task is confirmed enabled for the local CogentNexus-OpenClaw project/worktree.
