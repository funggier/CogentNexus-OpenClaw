# Coordination Signals

The operator does not need to copy task instructions between ChatGPT and Hermes/Codex. GitHub carries the durable task specification and report handoff.

Current coordination repository: `funggier/CogentNexus-OpenClaw`.  
Current stabilization branch: `agent/v0.9.3-full-stabilization`.  
Current READY gate: `READY_FOR_HERMES`.

## `ต่อ`

Synchronize the current authorized coordination branch, read `ACTIVE.md`, execute the exact currently authorized READY task, publish its matching report, and stop.

Before execution, Hermes/Codex must read the coordination README, active task, matching report state, and every safety/precondition gate.

If the active state is not `READY_FOR_HERMES`, or a completed matching report already exists, do not execute or repeat side effects.

## `เฝ้าต่อเนื่อง`

Set up or enable the continuous coordination mode defined in `WATCH_MODE.md`.

The intended configuration is an authorized Hermes/Codex Scheduled task in the ChatGPT desktop app using the local CogentNexus-OpenClaw project or a dedicated Git worktree.

Continuous mode may execute only tasks whose `ACTIVE.md` contains both:

```text
Status: READY_FOR_HERMES
Execution mode: AUTO
```

Reading this signal alone is not proof that monitoring is active. The executor must confirm that the Scheduled task is enabled.

## `สถานะ`

Synchronize and report coordination status only. Read `ACTIVE.md` and any matching report. Do not execute disruptive work.

## `หยุด`

Do not begin a new coordination task. This does not replace runtime lifecycle commands.

## `หยุดเฝ้า`

Pause or disable the continuous Scheduled task. Do not alter CogentNexus-OpenClaw runtime state.

## Safety and authority

The human operator remains final authority. Manual signals and `Execution mode: AUTO` authorize evaluation/execution of the exact durable task only; they never bypass safety gates.

GitHub coordination state outranks stale conversation memory. Hermes/Codex must stop as `BLOCKED` rather than broaden authority, discard unrelated work, repeat completed effects, or improvise an unsafe workaround.
