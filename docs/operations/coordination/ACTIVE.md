# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_HISTORICAL_TASK178_OUTER_OBSERVER_CLEANUP_HERMES`
Current authorization: `CNX-20260831-181_HERMES_HISTORICAL_TASK178_OUTER_OBSERVER_CLEANUP`
Task ID: `CNX-20260831-181`
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

[`tasks/CNX-20260831-181-hermes-historical-task178-outer-observer-cleanup.md`](tasks/CNX-20260831-181-hermes-historical-task178-outer-observer-cleanup.md)

## Accepted repository repair

Task 179:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Accepted repair candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Task 180:

`ACCEPTED_BLOCKED — PREINSTALL_TASK178_OUTER_OBSERVER_CLEANUP_REQUIRED`

Task 180 performed zero installer invocations and zero product lifecycle mutations. The repaired facade remains not yet installed.

## Task-181 authorization

Task 181 is cleanup-only. After fresh identity and zero-input verification, Hermes/Codex may terminate only the historical Task-178 outer evidence-observer chain associated with `run_reset178.py` and its verified wrapper descendants.

Known historical identities from Task-180 are hints only:

```text
bash 14196 -> bash 22832 -> Python 17052 -> Python 17444 (run_reset178.py)
```

Do not kill by PID alone. Fresh command-line/parent/evidence-root identity must match and no actual reset/uninstall child may be present.

## Required clean boundary

PASS requires the observer chain and all its observer descendants to be gone while controller/Gateway/Ollama/ownership/delivery/recovery/SQLite and Task-171 historical durable state remain unchanged and healthy.

## Hard fence

Task 181 semantic action budget: `0`.

No installer/install-over/reinstall, reset, uninstall, start/stop/restart/enable/disable, Gateway/Ollama lifecycle action, Dashboard Send, model/recovery action, manual state repair, product/source/test/workflow changes, release/tag/merge, or force push.

After Task-181 report publication, stop for ChatGPT review. Install-over and another reset remain unauthorized.