# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK201_TASK200_ORIGINAL_INSTALLER_TERMINAL_ADJUDICATION_AND_DISCORD_CLOSURE`
Current disposition: `TASK200_BLOCKED_EVIDENCE_ACCEPTED__ADJUDICATE_ORIGINAL_INSTALLER_BEFORE_ANY_MUTATION`
Task ID: `CNX-20260901-201`
Parent task: `CNX-20260831-200`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published v0.9.3 authority

Publication is already complete and must remain untouched.

Public tag `v0.9.3` target:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Do not republish, retarget, recreate, or modify the v0.9.3 Release/assets.

## Frozen repaired product candidate

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Do not substitute later coordination HEADs for product identity.

Repository RED -> GREEN gates remain accepted:

- Validate `33413832703`: `completed/success`
- Windows Installer Pack Smoke `33413832709`: `completed/success`
- PS5.1 Acceptance Smoke `33413832777`: `completed/success`

## Task 200 review

Task-200 report disposition:

`BLOCKED_EVIDENCE`

Review:

[`reviews/CNX-20260831-200-task198-repaired-discord-windows-requalification-review.md`](reviews/CNX-20260831-200-task198-repaired-discord-windows-requalification-review.md)

Accepted facts:

- one supported install-over invocation was consumed;
- exact repaired plugin bytes were installed and fingerprint-matched;
- original installer process was still running at Task-200 stop boundary;
- final installer completion/exit and managed convergence were not proven;
- last observed host mode was `passthrough`, startup disabled;
- Gateway/Ollama/SQLite remained healthy;
- Discord Send was correctly not started;
- human Discord Send budget remains `0 / 1` consumed.

No new product defect is accepted from Task 200 merely because the observation window ended while the installer was alive.

## Active Task 201

[`tasks/CNX-20260901-201-task200-original-installer-terminal-adjudication-and-discord-closure.md`](tasks/CNX-20260901-201-task200-original-installer-terminal-adjudication-and-discord-closure.md)

Task 201 must first be read-only:

1. identify whether the exact original Task-200 installer process terminated, remains genuinely running, or the PID was reused;
2. inspect/hash retained `b01-install.stdout` / `b01-install.stderr` and any late-created exit artifact;
3. determine whether the installer completion line appeared;
4. capture current plugin/ownership/host/startup/Gateway/Ollama/delivery/recovery/SQLite state;
5. perform no command to force convergence.

Only if the original installer is proven successfully completed **and** current runtime is already independently healthy in managed mode may Hermes proceed to the still-unused single Discord Send.

If the original installer is still the same running process after the extended interval, or if it terminated without successful completion/managed convergence, Task 201 must stop without Discord Send and report exact evidence.

## Discord acceptance semantics if Phase B gate passes

- Known owner session: `agent:main:discord:channel:1531199905673252946`
- Human Discord Send budget: exactly `1 / 1`
- Hermes/bot/API/injected send: `0`
- retry/regenerate/second message: `0`

Expected durable shape:

`1 human Discord Send -> 1 Ticket -> 1 Direct model call -> response_ready -> 1 native visible Discord result -> delivery_confirmed -> completed`

`before_agent_run hook failed` for the tested Send is a failure.

A `cnx_assistant_delivery` row is not required for native Discord Direct delivery. Dashboard-observer `missing-run-correlation` / `missing-append-before-deliver` diagnostics are not failures by themselves.

## Hard fence

Before the Task-201 Phase-B decision gate: no install rerun, no `enable`/`disable`, no start/stop/restart, no process kill, no reset/uninstall/reinstall/install-over, no state/config/SQLite mutation, no provider/model change, no Discord Send, no source/test/workflow edit, no Release/tag mutation, and no force push.
