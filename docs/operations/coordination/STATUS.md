# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK212_TASK211_NORMAL_UPGRADE_RECOVERY_INSTALL_OVER`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + authenticated Windows live install/provenance evidence through Hermes  
**Active task:** `CNX-20260901-212`  
**Parent:** `CNX-20260901-211`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK211_NORMAL_UPGRADE_RECOVERY_BOUNDARY_ACCEPTED__TASK212_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Current repaired candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Exact-head CI/package proof remain accepted.

## Task 211 accepted boundary

Task-211 report disposition was `BLOCKED_PARTIAL_FOREIGN_OR_MISMATCHED_STATE`; independent review accepts its observations but narrows the interpretation.

Fresh evidence proves:

```text
live plugin fingerprint = f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
candidate fingerprint = d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
live registration = canonical cogentnexus-openclaw 0.9.3 root, disabled
controller = passthrough
startup adapter = absent
classifier mode = upgrade
pendingRollover = false
pluginAlreadyExact = false
replacementPluginPath = null
legacy = []
Task-210 candidate-bound transaction = absent
```

No foreign plugin/package/version or unrelated replacement was proven. The mismatch is the expected old accepted generation versus the new Task-207 candidate. Because no candidate rollover transaction was persisted and no candidate plugin replacement occurred, the live state is accepted as a recoverable ordinary same-version upgrade boundary.

Historical accepted Windows evidence also establishes that `plugin-rollover-prepare` can take ~430–434 seconds and full install-over ~819 seconds. Task-210's blocking outer observer was too short to safely host the complete installer.

## Active Task 212

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-212-task211-normal-upgrade-recovery-install-over.md`

Required model:

- fresh read-only preflight must reproduce the Task-211 normal-upgrade shape;
- exactly one newly authorized Task-207 installer launch;
- root installer process launched independently from observation and identified by PID + creation time + executable path;
- stdout/stderr persisted to evidence files;
- separate 30–60 second bounded observations of the same PID;
- no observer timeout may kill or cause a second installer launch;
- allow at least 20 minutes from installer start before runtime alone is considered anomalous;
- require natural termination, all seven installer stage pairs with exit 0, and final installer success line;
- then prove installed fingerprint `d0677581...`, plugin enabled/loaded, ownership exact, OpenClaw pinned, controller managed, startup ready, Gateway/Ollama/delivery/recovery healthy, Task-205 recovery inert, and SQLite integrity `ok`.

Task 212 stops for review after install/provenance/health. It does not perform Discord acceptance.

## Discord budget

Task 212 authorizes `0 Discord Sends`.

## Hard fence

One installer launch maximum. No lifecycle workaround, no manual plugin/ownership/transaction/SQLite mutation, no provider/model substitution, no OpenClaw upgrade, no source/test/workflow edit, no Release/tag mutation, no force push, and no Discord traffic.
