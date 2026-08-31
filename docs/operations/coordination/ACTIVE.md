# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK204_STALE_RESET_LIFECYCLE_ADJUDICATION_CLEANUP_AND_DISCORD_CLOSURE`
Current disposition: `TASK203_FAIL_PRE_ENABLE_HEALTH_ACCEPTED__HISTORICAL_RESET_TREE_BLOCKS_RECOVERY`
Task ID: `CNX-20260901-204`
Parent task: `CNX-20260901-203`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Frozen repaired product candidate

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Repository RED -> GREEN gates remain accepted:

- Validate `33413832703`: `completed/success`
- Windows Installer Pack Smoke `33413832709`: `completed/success`
- PS5.1 Acceptance Smoke `33413832777`: `completed/success`

## Task 203 accepted result

Task-203 report disposition:

`FAIL_PRE_ENABLE_HEALTH`

Review:

[`reviews/CNX-20260901-203-task202-orphaned-host-cleanup-managed-recovery-and-discord-closure-review.md`](reviews/CNX-20260901-203-task202-orphaned-host-cleanup-managed-recovery-and-discord-closure-review.md)

Accepted facts:

- exact stale Task-200/202 PowerShell root PID `11704` was safely identity-fenced and removed once;
- installed repaired fingerprint and ownership remain valid;
- Gateway/Ollama/delivery/recovery/SQLite remain healthy;
- Host remains passthrough, startup/plugin disabled;
- no enable occurred;
- Discord Send remains unused: `0 / 1` consumed;
- an independent historical reset tree remains active:
  - PID `9840` product-owned Python -> `host_control_v092.py ... reset --provider ollama`
  - child PID `17360` underlying Python -> same argv.

The reset tree was created around `2026-08-31T14:36:03Z / 21:36 ICT`, about 1h47m before repaired candidate `9f4eaa...` and about 1h55m before the Task-200 orphan host. It is not a Task-200 install-over child and not the earlier accepted Task-183 reset.

Current best classification is a separate historical/manual reset invocation. Exact origin and internal wait state remain to be adjudicated before cleanup.

## Active Task 204

Hermes must execute:

[`tasks/CNX-20260901-204-task203-stale-reset-lifecycle-adjudication-cleanup-and-discord-closure.md`](tasks/CNX-20260901-204-task203-stale-reset-lifecycle-adjudication-cleanup-and-discord-closure.md)

Required sequence:

1. revalidate exact reset PID/create-time/argv identities and parent/session lineage;
2. sample reset-tree CPU/thread/handle/tree and state-file progress twice without sending any input;
3. classify whether `9840 -> 17360` is one stale logical reset invocation and ensure no lifecycle progress/second lifecycle process exists;
4. only if cleanup gate passes, terminate exact child `17360`, then exact parent `9840` if it remains; never broad-kill Python or parent `10724`;
5. prove no lifecycle residue and coherent exact-candidate passthrough state;
6. invoke installed `cnxclaw.cmd enable` exactly once;
7. require full managed convergence;
8. only then use the still-unused one human Discord Send and prove one Ticket -> one model call -> one visible reply -> delivery_confirmed -> completed.

## Discord budget

`0 / 1 consumed; 1 / 1 available`

## Hard fence

No reset replay, installer/install-over replay, uninstall/reinstall, broad process kill, input injection into stale reset, second enable, disable/start/stop/restart, manual config/SQLite/provider mutation, product/source/test/workflow edit, Release/tag mutation, second Discord Send, or force push.
