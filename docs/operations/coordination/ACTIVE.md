# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK212_TASK211_NORMAL_UPGRADE_RECOVERY_INSTALL_OVER`
Current disposition: `TASK211_ACCEPTED__NORMAL_UPGRADE_RECOVERY_BOUNDARY_PROVEN`
Task ID: `CNX-20260901-212`
Parent task: `CNX-20260901-211`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Current repaired product candidate

Task-207 repository-GREEN candidate remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Validated package proof remains artifact `9790881384`, digest `sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34`.

## Task 211 reviewed result

Report:

`reports/CNX-20260901-211-task210-interrupted-rollover-reentry-adjudication.md`

Review:

`reviews/CNX-20260901-211-task210-interrupted-rollover-reentry-adjudication-review.md`

Accepted review disposition:

`ACCEPT_CLASSIFICATION__NORMAL_UPGRADE_RECOVERY_BOUNDARY_PROVEN__FRESH_INSTALL_OVER_AUTHORIZATION_REQUIRED`

Accepted facts:

- Task-210 did not install the Task-207 candidate plugin generation;
- live plugin fingerprint remains the pre-Task-210 generation `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`;
- candidate fingerprint is `d0677581...`;
- live product registration remains canonical id/version/root but disabled;
- controller remains PASSTHROUGH and startup adapter absent;
- exact candidate classifier returns `mode=upgrade`, `pendingRollover=false`, `pluginAlreadyExact=false`, `replacementPluginPath=null`, `legacy=[]`;
- no Task-210 candidate-bound rollover transaction was persisted;
- Task-205 cancelled recovery remains inert; SQLite is healthy;
- no current installer/lifecycle process remains.

This is not the supported already-exact interrupted-reentry shape. It is accepted as a recoverable ordinary same-version upgrade boundary where the old generation remains intact and the candidate replacement never became active.

## Active Task 212

Hermes must execute:

`tasks/CNX-20260901-212-task211-normal-upgrade-recovery-install-over.md`

Task 212 must:

1. fresh-check authority and exact Task-207 package provenance;
2. re-prove the exact normal-upgrade preflight shape from Task 211;
3. launch exactly one newly authorized candidate installer process;
4. launch it detached from the observer so the executor can return immediately with exact PID/creation identity;
5. poll only that exact PID and retained stdout/stderr in separate bounded probes;
6. never restart or kill the installer merely because an observer call times out;
7. allow at least 20 minutes from start because historical successful install-over took ~819 seconds and rollover-prepare ~430–434 seconds;
8. require natural process termination, all seven stage START/COMPLETE pairs exit 0, and final success line;
9. prove installed fingerprint exactly `d0677581...`, plugin enabled/loaded, ownership coherent, OpenClaw pin preserved, and managed runtime/startup/Gateway/Ollama/delivery/recovery/SQLite health;
10. publish Task-212 report and stop for review.

No Discord Send is authorized in Task 212.

## Discord budget

Task 212 authorizes `0 Discord Sends`.

Task-207 semantic acceptance remains deferred until recovered install convergence is independently reviewed PASS.

## Hard fence

Exactly one Task-212 installer launch maximum. No compensating `enable/disable/start/stop/restart/reset/uninstall`, no manual plugin/ownership/transaction/SQLite mutation, no provider/model substitution, no OpenClaw upgrade, no source/test/workflow mutation, no Release/tag mutation, no force push, and no Discord traffic.
