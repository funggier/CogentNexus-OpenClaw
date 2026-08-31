# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK203_ORPHANED_HOST_CLEANUP_MANAGED_RECOVERY_AND_DISCORD_CLOSURE`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + one bounded Windows cleanup/recovery + at most one human Discord Send through Hermes  
**Active task:** `CNX-20260901-203`  
**Parent:** `CNX-20260901-202`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK202_ROOT_IDLE_NO_EXEC_DESCENDANT__BOUNDED_RECOVERY_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Frozen repaired candidate remains:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 202 result

Task 202 is accepted as:

`EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT`

The exact stale PowerShell PID remained alive but idle with unchanged CPU/threads/handles and unchanged installer streams across bounded samples. Its only descendant was `conhost.exe`; no Python, cnxclaw, Host, Node, OpenClaw, Gateway, installer or other execution descendant remained.

Current runtime remained coherent but incomplete:

- exact repaired installed fingerprint: PASS;
- ownership verify: PASS;
- Host: passthrough;
- startup/plugin: disabled;
- Gateway/Ollama: healthy;
- delivery/recovery: READY, no pending outbox/recovery attempt;
- SQLite integrity: ok;
- Discord Send: `0 / 1` consumed.

No production `install.ps1` deadlock is accepted from this evidence. A bounded live recovery is authorized instead of a source change.

## Active Task 203

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-203-task202-orphaned-host-cleanup-managed-recovery-and-discord-closure.md`

Required sequence:

1. final read-only identity/idle fence on PID `11704`;
2. terminate only that exact orphaned root process;
3. no installer replay;
4. verify installed exact-candidate passthrough health;
5. run installed `cnxclaw.cmd enable` exactly once with root-only process observation;
6. require full managed convergence;
7. only after convergence, use exactly one human Discord Send in the known healthy room;
8. prove one Ticket / one model call / one visible reply / delivery_confirmed / completed with no retry/recovery/duplicate/outbox residue.

If cleanup or enable fails or becomes ambiguous, stop before Discord Send.

## Discord budget

`0 / 1 consumed; 1 / 1 available`

No bot/API/injected message, retry, regenerate, second message, or second room is authorized.

## Hard fence

No installer rerun, reset/uninstall/reinstall/install-over, broad process kill, second enable, disable/start/stop/restart, provider/model/config/SQLite manual mutation, Release/tag mutation, source/test/workflow edit, force push, or second Discord Send.
