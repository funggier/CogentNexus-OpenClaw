# Coordination Signals

The operator does not need to copy task instructions between ChatGPT and Codex. GitHub carries the durable task specification and report handoff.

## `ต่อ`

Synchronize with `agent/v0.9.3-recovery-reality-tests`, read the current `ACTIVE.md`, execute the exact currently authorized READY task, publish its matching report, and stop.

Before execution, Codex must read the coordination README, active task, report state, and every safety/precondition gate.

If the active state is not `READY_FOR_CODEX`, or a completed matching report already exists, do not execute or repeat side effects.

## `เฝ้าต่อเนื่อง`

Set up or enable the continuous coordination mode defined in `WATCH_MODE.md`.

The intended configuration is a Codex Scheduled task in the ChatGPT desktop app using the local CogentNexus project or a dedicated Git worktree, polling every one minute.

Continuous mode may execute only tasks whose `ACTIVE.md` contains both:

```text
Status: READY_FOR_CODEX
Execution mode: AUTO
```

Reading this signal alone is not proof that monitoring is active. Codex must confirm that the Scheduled task is enabled.

## `สถานะ`

Synchronize and report coordination status only. Read `ACTIVE.md` and any matching report. Do not execute disruptive work.

## `หยุด`

Do not begin a new coordination task. This does not replace runtime commands such as `cnx stop`.

## `หยุดเฝ้า`

Pause or disable the continuous Scheduled task. Do not alter CogentNexus runtime state.

## Safety and authority

The human operator remains final authority. Manual signals and `Execution mode: AUTO` authorize evaluation/execution of the exact durable task only; they never bypass its safety gates.

GitHub coordination state outranks stale conversation memory. Codex must stop as `BLOCKED` rather than broaden authority, discard unrelated work, or improvise an unsafe workaround.
