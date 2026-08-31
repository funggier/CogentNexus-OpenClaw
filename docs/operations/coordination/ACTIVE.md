# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK203_ORPHANED_HOST_CLEANUP_MANAGED_RECOVERY_AND_DISCORD_CLOSURE`
Current disposition: `TASK202_ROOT_IDLE_NO_EXEC_DESCENDANT_ACCEPTED__BOUNDED_RECOVERY_AUTHORIZED`
Task ID: `CNX-20260901-203`
Parent task: `CNX-20260901-202`
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

Do not substitute coordination HEAD for product identity.

Repository RED -> GREEN gates remain accepted:

- Validate `33413832703`: `completed/success`
- Windows Installer Pack Smoke `33413832709`: `completed/success`
- PS5.1 Acceptance Smoke `33413832777`: `completed/success`

## Task 202 accepted result

Task-202 report outcome:

`EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT`

Review:

[`reviews/CNX-20260901-202-task201-original-installer-wait-tree-diagnosis-review.md`](reviews/CNX-20260901-202-task201-original-installer-wait-tree-diagnosis-review.md)

Accepted facts:

- stale root PowerShell PID `11704` remained exact by creation-time identity;
- across bounded samples its CPU/threads/handles and stdout/stderr did not advance;
- its only descendant was `conhost.exe` console infrastructure;
- no Python, cnxclaw, Host, Node, OpenClaw, Gateway, installer, or other executable work descendant survived;
- exact repaired plugin fingerprint and ownership remained valid;
- Host remained passthrough/startup disabled/plugin disabled;
- Gateway/Ollama/delivery/recovery/SQLite remained healthy;
- Discord Send remains unused: `0 / 1` consumed.

No `install.ps1` product deadlock is accepted from this evidence. The observed root shape materially differs from the known-good Task-159 standalone `powershell.exe ... -File install.ps1` process pattern and is treated as an orphaned executor/PowerShell-host boundary for recovery purposes.

## Active Task 203

Hermes must execute:

[`tasks/CNX-20260901-203-task202-orphaned-host-cleanup-managed-recovery-and-discord-closure.md`](tasks/CNX-20260901-203-task202-orphaned-host-cleanup-managed-recovery-and-discord-closure.md)

Execution order:

1. revalidate exact PID `11704` identity and idle/no-executable-descendant shape;
2. terminate only that exact stale root process;
3. do **not** rerun installer;
4. verify coherent installed exact-candidate passthrough state;
5. invoke installed `cnxclaw.cmd enable` exactly once using root-only process observation semantics;
6. prove full managed/plugin/startup/Gateway/Ollama/delivery/recovery/SQLite convergence;
7. only then use the still-unused human Discord Send budget `1 / 1` and prove one Ticket -> one model call -> one visible Discord result -> delivery_confirmed -> completed;
8. stop immediately on cleanup/enable/health failure without retry or Discord Send.

## Hard fence

No installer replay, reset/uninstall/reinstall/install-over, second enable, disable/start/stop/restart, provider/model/config/SQLite manual mutation, broad process kill, Release/tag mutation, product/source/test/workflow edit, second Discord Send, injection, or force push.
