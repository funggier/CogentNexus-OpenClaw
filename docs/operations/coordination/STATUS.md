# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK208_TASK207_WINDOWS_DISCORD_VISIBLE_FINAL_REQUALIFICATION`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + authenticated Windows/OpenClaw/Discord live acceptance through Hermes  
**Active task:** `CNX-20260901-208`  
**Parent:** `CNX-20260901-207`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK207_REPOSITORY_PASS__TASK208_READY`

## Publication and product authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Current repaired candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-207 exact-head CI is GREEN:

```text
Validate 33483589170: success
Windows Installer Pack Smoke 33483589124: success
PS5.1 Acceptance Smoke 33483589138: success
```

Package proof artifact:

`9790881384` / `sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34`

## Task 207 review

Accepted as:

`PASS_REPOSITORY__WINDOWS_REQUALIFICATION_REQUIRED`

The production repair is limited to the direct Discord bare-`NO_REPLY` visible-final guard. It does not change delivery correlation or lifecycle behavior.

A process note remains: the test-only RED commit has no remote Actions run; local RED plus source/commit ordering establish the intended pre-fix failure, while exact implementation GREEN is fully authoritative.

## Active Task 208

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-208-task207-windows-discord-visible-final-requalification.md`

Before install-over or Discord traffic, Task 208 must adjudicate the historical Task-205 recovery row. If it remains capable of delayed output, stop without mutation.

If that gate passes:

- install-over exact `27fe0181...` once from validated package proof;
- verify exact installed provenance and managed health;
- verify numeric Discord channel `1531199905673252946`;
- consume exactly one fresh human Send;
- allow at most one same-run Task-207 finalization revision if first final is bare `NO_REPLY`;
- require one visible native Discord reply;
- then require durable `delivery_confirmed -> completed`.

If visible reply succeeds but settlement fails, stop and preserve the run-bound hook evidence for a separate correlation repair.

## Human Send budget

`0 / 1 consumed; 1 / 1 available`

## Hard fence

No second/probe/API/bot Send, no reset/uninstall/fresh reinstall, no installer retry, no provider/model/config/schema/manual-SQLite mutation, no source/test/workflow mutation, no Release/tag mutation, no force push, and no delivery-correlation repair during Task 208.
