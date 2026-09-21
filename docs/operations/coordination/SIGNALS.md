# Coordination Signals

GitHub carries durable task authority. Signals are shorthand only; they never override safety or the current remote task.

Repository: `funggier/CogentNexus-OpenClaw`
Current branch/task: read from `ACTIVE.md` / `STATUS.md`.

## `ต่อ`

Synchronize current remote authority and continue the exact currently assigned task with the executor named there.

Do not assume a historical `READY_FOR_HERMES` token or old branch name.

## `สถานะ`

Read and report current coordination state only. Do not perform disruptive work.

## `หยุด`

Do not begin new coordination work. This is not a substitute for runtime lifecycle commands.

## Historical `เฝ้าต่อเนื่อง` / `หยุดเฝ้า`

The old one-minute Codex `CogentNexus coordination watch` automation was retired and removed on 2026-09-21.

These signals remain documented only so historical conversations are interpretable. They do not authorize recreating that watcher. A future watcher requires a new explicit task/authorization and a current supported design.

## Safety and authority

The human operator remains final authority. GitHub coordination state outranks stale conversation memory. A signal never authorizes force push, destructive cleanup, repeated external effects, or a successor task not represented in current durable authority.
