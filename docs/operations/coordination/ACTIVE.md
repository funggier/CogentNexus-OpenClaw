# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK213_TASK212_INSTALLER_SOURCE_AND_DETACHED_LAUNCH_ROOT_CAUSE_ADJUDICATION`
Current disposition: `TASK212_TERMINAL_BLOCK_ACCEPTED__SOURCE_AND_HARNESS_ROOT_CAUSE_REQUIRED`
Task ID: `CNX-20260901-213`
Parent task: `CNX-20260901-212`
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

Known old live generation remains:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 212 reviewed result

Task-212 report:

`reports/CNX-20260901-212-task211-normal-upgrade-recovery-install-over.md`

Task-212 review:

`reviews/CNX-20260901-212-task211-normal-upgrade-recovery-install-over-review.md`

Accepted review disposition:

`ACCEPT_BLOCKED_INSTALLER_TERMINAL__LAUNCH_SOURCE_AND_HARNESS_ROOT_CAUSE_REQUIRED`

Accepted Task-212 facts:

- preflight remained the ordinary upgrade boundary;
- one recorded PowerShell PID `21836` was launched;
- PID disappeared before the first ~30-second sample;
- installer stdout/stderr remained 0 bytes;
- no stage marker, success line, failure line, or exit code was retained;
- live fingerprint remained old `f826...`;
- controller remained PASSTHROUGH, startup absent, Gateway healthy, SQLite integrity `ok`;
- Task-205 cancellation remained inert;
- no installer retry/lifecycle workaround/Discord Send occurred.

Independent review identified an additional source-authority gap: the command recorded by Task 212 executed

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1`

rather than a path visibly rooted in the Task-212 verified Task-207 extraction. The report proved Task-207 package identity separately but did not bind the source tree containing the executed installer to `27fe0181...`.

The detached launcher itself is also unproven because Task-212 did not retain an immediate OS identity tuple proving PID/executable/command-line and its 0-byte/rapid-exit shape differs materially from known-good Task-170 behavior.

## Active Task 213

Hermes must execute:

`tasks/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication.md`

Task 213 is diagnostic/read-only with one harmless synthetic process-launch test.

It must:

1. preserve current product/runtime state read-only;
2. identify the exact source tree behind the Task-212 executed installer path by hashes, metadata/Git identity where available, exact candidate-tool plugin fingerprint, and Task-207 repair-file byte comparison;
3. inspect/hash the retained Task-212 `launch-installer.py` and `monitor-installer.py` and report exact Popen/creationflags/std-handle/cwd/env behavior;
4. reproduce the same launcher mechanics with a harmless PowerShell child that writes deterministic stdout/stderr, sleeps >=60s, and exits with known code — no product script or product path access;
5. capture OS PID + creation time + executable + full argv immediately and during the harmless run;
6. compare material launch mechanics with known-good Task-170 evidence where provable;
7. classify source-boundary and/or launcher-harness root cause and publish report.

No CogentNexus installer or lifecycle command is authorized.

## Discord budget

Task 213 authorizes `0 Discord Sends`.

Task-207 semantic acceptance remains closed until installation/provenance/managed convergence is proven.

## Hard fence

No installer, no install-over, no enable/disable/start/stop/restart/reset/uninstall, no OpenClaw plugin mutation, no ownership/transaction/backup normalization, no manual SQLite mutation, no Gateway restart, no provider/model/config mutation, no product source/test/workflow edit, no Release/tag mutation, no force push, and no Discord traffic.
