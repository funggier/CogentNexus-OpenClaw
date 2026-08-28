# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `MANUAL`
Current authorization: `CNX-20260828-105_EXACT_SNAPSHOT_REAL_WINDOWS_LIFECYCLE_ACCEPTANCE`
Task ID: `CNX-20260828-105`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-105-v093-real-windows-lifecycle-acceptance.md`](tasks/CNX-20260828-105-v093-real-windows-lifecycle-acceptance.md)

Task 105 supersedes the stale Task-104 source-only coordination fence. The operator has explicitly accepted the known OpenClaw `2026.7.1-2` upstream dependency risk for this acceptance line and authorized bounded real-Windows lifecycle acceptance.

## Pinned acceptance snapshot

Do not use moving branch HEAD as the runtime candidate.

- exact source: `c4d37b0005afeffcd183848dfce5476cbe2b85cd`
- version: `0.9.3`
- OpenClaw baseline: `2026.7.1-2`
- managed provider: `Ollama only`
- payload-v2 file count: `178`
- payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- accepted inner ZIP SHA256: `c6151fac1cc3b5cd37a2d82aa366bb547adff1f885b9d2b33209c83601606133`
- package-proof Actions artifact ID: `9669312785`
- Validate run `33128487849`: SUCCESS, package + 6/6 matrix
- PS5.1 Acceptance Smoke `33128487814`: SUCCESS
- Windows Installer Pack Smoke `33128487825`: SUCCESS

Coordination commits after `c4d37b0...` intentionally advance the branch but do not change the acceptance artifact. Development may continue later; Task 105 evidence applies only to the exact snapshot above.

## Authorized live scope

Task 105 may execute, in order and with stop-on-failure semantics:

1. exact provenance/read-only preflight;
2. install-over of the existing coherent CogentNexus-OpenClaw deployment using the exact CI artifact;
3. one confirmed `cnxclaw.cmd reset` proof;
4. one confirmed `cnxclaw.cmd uninstall` proof;
5. fresh reinstall of the same exact CI artifact;
6. normal stop/start/restart lifecycle proof;
7. one full disruptive v3 recovery-harness run with exact-PID safety gates;
8. report and stop for ChatGPT review.

The executor must not repeat a failed/completed destructive phase merely to obtain a cleaner result.

## Hard fence

Task 105 does **not** authorize:

- a new Dashboard semantic nonce/Send or semantic artifact reuse;
- source/product behavior fixes;
- direct live SQLite edits or arbitrary config/runtime mutations;
- session cleanup/normalization;
- credentials/token/password access or re-entry;
- model/provider/timeout changes;
- OpenClaw or Ollama update/reinstall/uninstall/rebaseline;
- LM Studio management;
- process-tree kills;
- reboot;
- merge, tag, GitHub Release publication, or force push.

If exact provenance, ownership, safety, or required baseline cannot be proven, publish a `BLOCKED`/`FAIL` Task-105 report and stop rather than improvising.

## Completion signal

Hermes/Codex owns only the matching report:

`docs/operations/coordination/reports/CNX-20260828-105-v093-real-windows-lifecycle-acceptance.md`

After that report is pushed, stop for independent ChatGPT review. Do not invent the next task.
