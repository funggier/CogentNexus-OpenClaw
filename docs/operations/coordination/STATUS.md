# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 107 authorizes the bounded real-Windows lifecycle acceptance retry against one exact post-fix candidate  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`](tasks/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md)

Task ID:

`CNX-20260828-107`

## Why Task 107 exists

Task 105 remains a valid failed real-Windows acceptance attempt against its immutable pre-fix candidate. It stopped after the single install-over attempt failed in the OpenClaw `npm-pack:` metadata path on npm `12.0.2`, leaving a preserved PASSTHROUGH boundary and not executing reset, uninstall, fresh reinstall, normal lifecycle, disruptive recovery, or Dashboard semantic delivery.

Task 106 then completed the source/test closure around the accepted minimal installer repair. Because Task 105's artifact predates that production fix, Task 107 uses a new immutable package-proof artifact generated from the exact post-fix source instead of replaying the old candidate.

## Exact Task-107 candidate

Pinned source:

`b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

Exact CI gates on that source are all `SUCCESS`:

- Validate `33149370021`
- Windows Installer Pack Smoke `33149369983`
- PS5.1 Acceptance Smoke `33149369996`

Exact package proof:

- Actions artifact ID: `9677072214`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- outer SHA256: `b02dc802e2ea71ed18a12071ab570236864cea5c72416b8fae6ac9607f710b76`
- inner `cogentnexus-openclaw-v0.9.3.zip` SHA256: `3079ea8289d3ed465337b4621cb771eb1971d4ba7d86eb09d94d81875c049e1b`
- package tar.gz SHA256: `5a010879d6effd3ee0ecbc449a6cffb30ecd26e91b90fb08765636c31d6a3b05`
- version: `0.9.3`
- payload-v2 file count: `178`
- payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

The accepted repair ancestry is:

- `e0b6173d2ed888303bae3e31fd023b24e201c167` — RED installer-path contract;
- `c676c50cb19378541a8223263a609fb7d18ed5a8` — minimal Windows installer local-archive fix;
- `5e41c0c3a8b9da920571b828c9a863f5591af86b` — npm12 production-shaped regression;
- `80a48f73d3c525565a15e07ed1ed37a7c4fc4ad3` — Task-106 test-only stale-assertion repair;
- `b14a711f24b3fd1cd0aaa51ce636c8502ba42404` — Task-106 report and pinned Task-107 package source.

## Live boundary: verify before mutation

Task 105 recorded the post-failure machine as:

- CogentNexus-OpenClaw `PASSTHROUGH`, generation `25`;
- Gateway healthy;
- Ollama healthy;
- SQLite integrity healthy;
- ownership manifest coherent;
- Supervisor task absent after the supported native handoff;
- installer staging/backup residue preserved;
- no later destructive phases executed;
- no Dashboard semantic Send executed.

This is historical evidence, not permission to assume the machine still has that state. Task 107 begins with exact provenance plus a fresh read-only live preflight. If the current machine cannot be reconciled with that boundary, the executor must report `BLOCKED` and stop without manual cleanup or normalization.

## Authorized sequence

Only after provenance and read-only re-entry pass:

`install-over -> reset -> uninstall -> fresh reinstall -> stop/start/restart -> disruptive recovery -> report`

Every destructive or externally visible phase is single-attempt. Stop at the first non-zero or ambiguous result. Product/source repair is outside this acceptance task.

## Hard fence

Task 107 does **not** authorize:

- use of Task 105's old package artifact;
- moving-HEAD installation instead of the pinned Task-107 package;
- Dashboard semantic nonce/Send, semantic artifact reuse, or provider inference;
- source/product fixes;
- direct live SQLite/config/session mutation;
- manual residue cleanup or normalization;
- OpenClaw or Ollama update/reinstall/uninstall;
- model/provider/timeout changes;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- replaying a failed destructive phase.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

The report must give a phase-by-phase evidence-backed verdict and stop after publication for independent ChatGPT review. The final Dashboard durable-delivery semantic test remains a separate follow-up and must not be started inside Task 107.
