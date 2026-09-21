# Coordination Watch Mode — Historical / Optional Design

Updated: 2026-09-21 ICT

## Current status

The former Codex `CogentNexus coordination watch` one-minute automation is **retired and removed**. It is not part of the current operating model.

This file is retained to explain the intended safety properties of any future bounded watcher and to interpret historical reports. It is not an instruction to recreate the old automation.

## Requirements for any future watcher

A future watcher may exist only when explicitly authorized by a current task and must:

1. read the branch/task from current remote `ACTIVE.md` / `STATUS.md`;
2. never hard-code a historical branch;
3. fetch remote authority before every mutation/recheck;
4. deduplicate scheduled wakes;
5. perform no heartbeat commits;
6. never infer successor/live/destructive authority;
7. stop when the task is complete, stale, paused, or assigned to another authority;
8. preserve no side-effect authority merely because a timer fired.

## CI/external waits

If an active task needs repeated rechecks, prefer a bounded delayed recheck appropriate to the current toolchain. A wait is permission to re-check the same dependency, not permission to repeat the action that created it.

## Historical note

Older documents may describe approximately five-minute polling or a persistent Codex watcher. Those descriptions remain factual history for their time but are not standing current instructions.
