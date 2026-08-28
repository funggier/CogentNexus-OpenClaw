# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL_REAL_WINDOWS_ACCEPTANCE`
Current authorization: `CNX-20260828-107_V093_REAL_WINDOWS_LIFECYCLE_ACCEPTANCE_RETRY`
Task ID: `CNX-20260828-107`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`](tasks/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md)

Task 107 is a new pinned real-Windows lifecycle acceptance attempt after Task 105 exposed the npm 12 installer incompatibility and Task 106 closed the source/test regression.

## Accepted source and CI gate

Exact pinned source:

`b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

Accepted repair ancestry:

- RED installer contract: `e0b6173d2ed888303bae3e31fd023b24e201c167`
- minimal production fix: `c676c50cb19378541a8223263a609fb7d18ed5a8`
- npm12 production-shaped regression: `5e41c0c3a8b9da920571b828c9a863f5591af86b`
- Task-106 test-only repair: `80a48f73d3c525565a15e07ed1ed37a7c4fc4ad3`
- Task-106 report / pinned package source: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

Exact CI runs on the pinned source are all SUCCESS:

- Validate `33149370021`
- Windows Installer Pack Smoke `33149369983`
- PS5.1 Acceptance Smoke `33149369996`

Exact package-proof artifact:

- artifact ID `9677072214`
- name `cogentnexus-openclaw-v0.9.3-package-proof-b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- outer SHA256 `b02dc802e2ea71ed18a12071ab570236864cea5c72416b8fae6ac9607f710b76`
- inner v0.9.3 ZIP SHA256 `3079ea8289d3ed465337b4621cb771eb1971d4ba7d86eb09d94d81875c049e1b`
- tar.gz SHA256 `5a010879d6effd3ee0ecbc449a6cffb30ecd26e91b90fb08765636c31d6a3b05`
- payload-v2 file count `178`
- payload-v2 fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Do not use the old Task-105 package artifact. It predates the accepted installer fix.

## Preserved live boundary to verify, not assume

Task 105 recorded the Windows machine after its single failed install-over as:

- CogentNexus-OpenClaw: `PASSTHROUGH`
- generation: `25`
- Gateway: healthy
- Ollama: healthy
- SQLite: healthy
- Supervisor task absent after supported native handoff
- reset/uninstall/fresh reinstall/recovery phases: not executed
- Dashboard semantic Send: not executed

Task 107 must begin with a fresh read-only preflight. If the current machine cannot be reconciled with that recorded boundary, stop `BLOCKED` rather than normalizing it manually.

## Authorized Task-107 sequence

Only after exact provenance and read-only preflight pass:

`install-over -> reset -> uninstall -> fresh reinstall -> stop/start/restart -> disruptive recovery -> report`

Every externally visible/destructive phase is single-attempt. Stop at the first non-zero or ambiguous result. Do not patch product behavior inside the acceptance task.

## Hard fence

Task 107 does **not** authorize:

- Dashboard semantic nonce/Send or semantic artifact reuse;
- use of the old Task-105 package for retry;
- moving-HEAD installation instead of the pinned package;
- source/product fixes;
- direct SQLite/config/session mutation;
- manual residue cleanup/normalization;
- OpenClaw or Ollama update/reinstall/uninstall;
- model/provider/timeout changes;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- replaying any failed destructive phase.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

After the report is pushed, stop for independent ChatGPT review. Do not invent or start the final semantic-delivery task.
