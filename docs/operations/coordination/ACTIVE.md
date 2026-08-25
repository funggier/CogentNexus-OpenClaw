# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL_WITH_HUMAN_GATE`
Current authorization: `POST_POWER_LOSS_DIAGNOSIS_AUTHORIZED`
Task ID: `CNX-20260825-062`
Updated: 2026-08-25 10:07 ICT
Owner: ChatGPT
Executor: Hermes after the operator's manual continuation signal

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains project narrative and is not a Task 062 execution gate.

## Active task

[`tasks/CNX-20260825-062-post-power-loss-managed-diagnosis.md`](tasks/CNX-20260825-062-post-power-loss-managed-diagnosis.md)

## Trigger and fresh evidence boundary

The operator explicitly asked ChatGPT to continue after Task 061 and reported that the machine unexpectedly lost power after the Task 061 MANAGED re-entry report.

The power loss invalidates use of Task 061 runtime observations as current-state authority. Task 062 must establish the current post-boot state from fresh evidence before drawing any repair conclusion.

A manual continuation signal to Hermes authorizes execution of exactly Task 062 only.

## Accepted predecessor

Task 061 report result:

`BLOCKED_POST_ENABLE_VERIFICATION`

Task 061 report commit:

`3029ca88d4814f7da2c6e6a088a85692452dc453`

Task 061 review disposition:

`ACCEPT_BLOCKER_MANAGED_REENTRY_ACCEPTANCE_MODEL_MISMATCH`

Task 061 review commit:

`7bdd47b9dc0003fbee1c3a7bbdc8b229740c68a5`

## Review finding carried forward

Task 061 correctly recorded an exit-0 MANAGED re-entry and stopped on its mandatory postconditions, but several of those postconditions were specified against the wrong execution layer.

The current v0.9.3 operator lifecycle is layered through the v0.9.3 Ollama facade, accepted v0.9.2 provider/route facade, v0.9.2 Host-control/Host overlays, and v0.9.1 transactional compatibility layer. Therefore:

- exact final generation `8` is not an authoritative invariant;
- the current startup adapter is expected to target `host_control_v092.py`, not base `host_control.py`;
- managed interval values must be derived from the active overlay, where the v0.9.1 transactional layer uses `60000` ms compatibility values rather than Task 061's base-Host `5000` ms assertions.

Two questions remain unresolved and require diagnosis:

1. why applying/removing the managed AGENTS block did not recreate the accepted pre-enable baseline bytes;
2. why most bounded managed plugin config keys appeared empty after the successful Task 061 enable despite the active transactional layer staging those settings.

## Authorized operation

Task 062 is diagnosis-only. It may:

- create its bounded evidence directory;
- prove the Windows reboot boundary from LastBootUpTime/current timestamps;
- inspect current controller/startup/Gateway/Ollama/plugin/ownership/SQLite state read-only;
- observe existing Scheduled Task state and autonomous post-boot supervisor execution without running or changing the task;
- compare installed lifecycle files against a fresh isolated clone;
- reconstruct the exact v0.9.3 operator call graph and generation accounting;
- diagnose AGENTS byte drift in memory/read-only using bounded backups/evidence;
- diagnose managed config persistence with bounded individual reads/static source tracing;
- publish only the matching Task 062 report.

## Required stop state

Task 062 must stop after diagnosis and report publication. Preferred completed diagnostic result:

`DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND`

This token means evidence is sufficient to design a separate successor; it does not accept the product for release and does not authorize repair.

## Safety

No lifecycle mutation, installer/reset/uninstall, rollover, plugin mutation, OpenClaw config mutation, AGENTS write/restore, startup task mutation/run/end, Gateway/Ollama/provider mutation, ownership rewrite, SQLite/Ticket/session/recovery write, process termination, primary Git mutation, Procmon Task 027/038 action, HermesAgent mutation, Ecosystem work, merge, tag, release, or archive publication.

If the post-power-loss machine is unhealthy, do not start or repair it in Task 062. The unhealthy state is evidence and must be reported as observed.
