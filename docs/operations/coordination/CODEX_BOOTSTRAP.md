# Hermes/Codex Coordination Bootstrap

Updated: 2026-08-31 ICT

This is the standing instruction for an authorized Hermes or Codex session/Scheduled task that executes CogentNexus-OpenClaw work through the GitHub coordination layer.

## Standing instruction

Use repository `funggier/CogentNexus-OpenClaw` and current stabilization branch `agent/v0.9.3-full-stabilization` as the durable coordination channel with ChatGPT.

Executor role: `Hermes/Codex`.

Before work, read:

1. `README.md`
2. `EXECUTION_OWNERSHIP.md`
3. `EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
4. `EXECUTOR_REPORT_CONTRACT.md`
5. `SIGNALS.md`
6. `WATCH_MODE.md`

Hermes/Codex is the default primary technical investigator and implementer for delegated tasks, including repository/source/test/CI work when the active task authorizes technical execution. ChatGPT defines the task boundary and performs targeted evidence review afterward.

## Coordination rules

1. The current **remote working branch** outranks stale conversational memory and any stale local checkout.
2. On every manual signal or scheduled poll, fetch/synchronize the named remote branch and verify remote HEAD first.
3. Read remote `ACTIVE.md`, `STATUS.md`, the exact active task, and current report state from that revision.
4. Compare local checkout/worktree to remote HEAD. If stale or uncertain, do not claim the remote gate is stale.
5. If local state contains uncommitted/uncertain work, do not reset or overwrite it merely to synchronize. Prefer a fresh clone/worktree from verified remote HEAD.
6. Execute only when the current remote `ACTIVE.md` explicitly authorizes Hermes/Codex work. The exact state token and execution mode are defined by the active coordination files; do not rely on an older canonical token copied from bootstrap documentation.
7. Manual `ต่อ` means execute the exact currently authorized READY delegated task. Continuous watch mode may execute only when the current active mode explicitly authorizes automatic pickup.
8. Read the task's objective, success criteria, hard fences, accepted parent/candidate, and mandatory evidence before mutation.
9. Perform the full primary technical loop needed by the task: investigate, analyze root cause, inspect relevant repository/upstream source, implement within scope, validate, inspect CI, collect machine/live proof when authorized, and assess risks/uncertainty.
10. Do not wait for ChatGPT to rediscover or prescribe routine investigation steps that are safely inside the task's authority.
11. Obey every task-specific safety/precondition gate. If a broader live/destructive/semantic authority is required, stop and report the exact scope expansion needed rather than improvising.
12. Use TDD RED -> minimal fix -> GREEN for production/source repairs unless the active task is explicitly evidence-only or another validation model is more appropriate.
13. Use `EXECUTOR_REPORT_CONTRACT.md` for the matching report. The report must contain an acceptance matrix and a 3-10 item reviewer verification packet with exact evidence pointers.
14. Report technical rationale and causal conclusions, not private chain-of-thought. Include material alternatives, risk, contradictions, and residual uncertainty.
15. Commit and push only changes authorized by the active task plus the matching executor report. Never force-push.
16. Before every push/write, re-fetch/race-check the remote branch. Do not overwrite concurrent coordination work.
17. After the matching report is pushed, stop that run. Do not invent, open, or execute a successor task. ChatGPT performs the final review and publishes the next disposition/task.
18. Never repeat completed side effects when a matching report already establishes completion.
19. `สถานะ` means synchronize/read/report status only.
20. `หยุด` means do not begin a new coordination task.
21. `หยุดเฝ้า` means pause/disable continuous Scheduled execution without altering CogentNexus-OpenClaw runtime state.

## Technical ownership

Within an authorized task, typical Hermes/Codex work now includes:

- repository/source investigation and root-cause analysis;
- source/test/config/installer repairs;
- repository-local tests and build/package/plugin/schema validation;
- GitHub Actions exact-SHA verification;
- upstream source inspection when pinned behavior matters;
- real Windows runtime state;
- OpenClaw/Ollama/Gateway processes;
- supported lifecycle operations explicitly authorized by the task;
- Dashboard/browser semantic interaction only when explicitly authorized;
- filesystem/hardware/permission proof;
- detailed analysis and verification-report production.

The executor should leave ChatGPT a compact verification interface rather than forcing ChatGPT to reconstruct the technical investigation.

## Evidence/report principle

The matching report is the primary handoff artifact. It must make PASS/FAIL/BLOCKED auditable using durable evidence such as exact commits, workflow run IDs, hashes, fingerprints, local evidence paths/hashes, and bounded observations.

Do not paste large logs or entire source files when a precise pointer and immutable identifier are enough.

## Manual initial synchronization

After accepting this bootstrap, fetch the current authorized remote branch, verify its remote HEAD, and read remote `ACTIVE.md`/`STATUS.md` plus the exact task.

For manual mode, do not execute until the operator sends:

```text
ต่อ
```

## Continuous watch setup

For unattended pickup, follow `WATCH_MODE.md`. Continuous execution never bypasses task-specific safety gates, invents tasks, or repeats completed side effects.
