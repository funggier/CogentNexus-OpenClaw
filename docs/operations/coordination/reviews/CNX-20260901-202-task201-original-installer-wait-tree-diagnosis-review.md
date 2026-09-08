# CNX-20260901-202 — ChatGPT Review

Disposition: `ACCEPT_EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT__BOUNDED_RECOVERY_REQUIRED`

## Reviewed authority

- Task report: `docs/operations/coordination/reports/CNX-20260901-202-task201-original-installer-wait-tree-diagnosis.md`
- Fresh report commit: `1062ba22901fd125154f0a13f10e768abd4bae5e`
- Frozen repaired product candidate: `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- Expected installed plugin fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Accepted findings

Task 202 is accepted as a valid read-only diagnosis.

1. PID `11704` is still the same original PowerShell process by executable path and creation-time identity.
2. Across two samples separated by about 36.5 seconds, root CPU time, thread count, handle count, descendant membership, stdout/stderr sizes, hashes, and mtimes were unchanged.
3. The only surviving descendant was `conhost.exe`; no Python, `cnxclaw`, Host, Node, OpenClaw, Gateway, command-shell, or Scheduled Task execution descendant remained.
4. The correct evidence classification is therefore `EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT`.
5. This does not prove an internal PowerShell deadlock/wait primitive and no such product root cause is accepted.
6. Installed repaired bytes and ownership remain coherent; Host remains `passthrough`, startup/plugin disabled, while Gateway/Ollama/delivery/recovery/SQLite remain healthy.
7. Discord Send remains unused (`0 / 1`).

## Pattern comparison

A known-good Task-159 install-over used a dedicated standalone child process with command line `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...\install.ps1`, polled that exact process until termination, and completed successfully.

The Task-200/201/202 retained root process instead reports an OS command line containing only `powershell.exe`. Combined with the absence of any executable descendant, this is materially different from the known-good standalone installer-process pattern and is consistent with an executor/PowerShell host boundary rather than a proven `install.ps1` source hang.

This comparison is evidence for recovery-path selection, not a claim about the exact internal PowerShell wait primitive.

## Recovery decision

No production/source repair is authorized from Task 202.

The safe successor is a bounded live recovery task that:

1. revalidates the exact stale PowerShell identity and idle/no-exec-descendant shape;
2. terminates only that exact stale root process and its console infrastructure;
3. does not rerun the installer;
4. independently verifies installed candidate fingerprint/ownership and passthrough safety state;
5. invokes the supported installed `cnxclaw.cmd enable` exactly once;
6. requires managed/plugin/startup/Gateway/Ollama/delivery/recovery/SQLite convergence before any Discord traffic;
7. if convergence passes, consumes the still-unused one-human-Discord-Send budget and completes the Task-198 Discord requalification;
8. stops immediately on cleanup or enable failure without retry or Discord Send.

## Publication fence

The already-published `v0.9.3` Release remains immutable and is not modified by this recovery path.
