# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK213_TASK212_INSTALLER_SOURCE_AND_DETACHED_LAUNCH_ROOT_CAUSE_ADJUDICATION`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + authenticated Windows read-only/harness evidence through Hermes  
**Active task:** `CNX-20260901-213`  
**Parent:** `CNX-20260901-212`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK212_TERMINAL_BLOCK_ACCEPTED__TASK213_ROOT_CAUSE_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Current repository-GREEN repaired candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-207 candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

## Task 212 reviewed boundary

Task 212 is accepted only as an evidence-safe stop:

`ACCEPT_BLOCKED_INSTALLER_TERMINAL__LAUNCH_SOURCE_AND_HARNESS_ROOT_CAUSE_REQUIRED`

Observed Task-212 shape:

```text
preflight mode: passthrough ordinary upgrade
old live fingerprint: f82674172...
recorded installer PID: 21836
first bounded observation ~27s later: PID absent
stdout bytes: 0
stderr bytes: 0
stage markers: 0
terminal line: none
exit code: unavailable
post live fingerprint: f82674172...
startup adapter: absent
Gateway: healthy
SQLite: ok
Discord sends: 0
```

No product failure is accepted from this shape.

The executed command also referenced:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1`

Task 212 did not bind that exact source tree to Task-207 candidate `27fe0181...`; it proved the Task-207 package separately. Since the installer packages the repository-relative plugin tree, this source boundary must be adjudicated before another install authorization.

## Active Task 213

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication.md`

Required diagnostic work:

- read-only live preservation;
- exact identity/fingerprint/hash binding of the source root containing the actually executed Task-212 `install.ps1`;
- exact inspection of retained `launch-installer.py` / `monitor-installer.py` Popen and Windows creation flags;
- harmless synthetic PowerShell child using the same launch options, with deterministic stdout/stderr, >=60s lifetime, known exit code, and immediate OS identity sampling;
- comparison with known-good Task-170 launch/observation evidence where directly provable;
- explicit root-cause classification.

Task 213 may create only external evidence files and a harmless temporary process. It may not run any product installer/lifecycle action.

## Discord budget

`0 Discord Sends`.

## Hard fence

No install-over/installer, no lifecycle enable/disable/start/stop/restart/reset/uninstall, no OpenClaw plugin mutation, no ownership/staging/transaction/backup edits, no SQLite writes, no Gateway restart, no provider/model/config mutation, no source/test/workflow mutation, no Release/tag mutation, no force push, and no Discord traffic.
