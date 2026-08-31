# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `REPOSITORY_INTERACTIVE_LIFECYCLE_DELEGATION_DEADLOCK_REPAIR_HERMES`
Current authorization: `CNX-20260831-179_HERMES_INTERACTIVE_LIFECYCLE_DELEGATION_DEADLOCK_REPAIR`
Task ID: `CNX-20260831-179`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-179-hermes-interactive-lifecycle-delegation-deadlock-repair.md`](tasks/CNX-20260831-179-hermes-interactive-lifecycle-delegation-deadlock-repair.md)

Task 179 repairs the production nested-capture deadlock exposed by Task 178 and first retires the exact Task-178 hung process tree if it remains alive.

## Accepted baseline

- Previous accepted product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Task 171–173: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`
- Task 177: `ACCEPTED_DIAGNOSTIC_PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`
- Task 178: `ACCEPTED_FAILURE_BOUNDARY — RESET_INTERACTIVE_PROMPT_BLOCKED_BY_NESTED_DELEGATION_CAPTURE`

Task-171 semantic Send count remains permanently frozen at exactly `1`.

## Root cause

`cnxclaw.py` delegates unhandled commands through `host_control_v092.py` using `capture_output=True` and forwards stdout/stderr only after child completion. `host_control_v092.py` routes reset/uninstall into the lifecycle wrapper, which waits for explicit interactive confirmation. Therefore the real prompt is trapped behind the intermediate captured child while the child waits for input.

This is a production delegation defect, not a Task-177 outer-harness defect.

## Task-179 authorization

1. Re-verify the exact Task-178 ledger/process identities. If the same hung Task-178 process tree still exists with zero prompt/input events and unchanged pre-confirmation state, terminate only that exact process tree and verify cleanup.
2. Use TDD to reproduce the nested interactive delegation failure harmlessly in repository tests.
3. Apply the smallest source repair that gives `reset`/`uninstall` a true interactive stdin/stdout/stderr delegation path while preserving normal noninteractive delegation behavior.
4. Run focused/full validation and exact-SHA CI.
5. Publish the Task-179 report and stop.

## Hard fence

Task 179 semantic action budget: `0`.

No new reset, uninstall, install/install-over/reinstall, runtime lifecycle helper, Gateway/Ollama restart, Dashboard Send, model/recovery action, manual durable/config/transcript/route/DB repair, upgrade, release, merge, or force push.

Repository source/test changes required by TDD are authorized. Live mutation is limited to cleanup of the exact already-hung Task-178 process tree after re-verification.

After Task-179 report publication, stop for ChatGPT review. A repaired candidate must be reviewed and then installed-over in a later successor before reset is attempted again.