# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK208_TASK207_WINDOWS_DISCORD_VISIBLE_FINAL_REQUALIFICATION`
Current disposition: `TASK207_REPOSITORY_PASS__TASK208_LIVE_REQUALIFICATION_READY`
Task ID: `CNX-20260901-208`
Parent task: `CNX-20260901-207`
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

Task-207 repository-GREEN candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Validated package proof:

```text
artifact ID: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
payload-v2: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
```

## Task 207 accepted result

Review:

`reviews/CNX-20260901-207-task206-direct-discord-no-reply-visible-final-repair-review.md`

Accepted disposition:

`PASS_REPOSITORY__WINDOWS_REQUALIFICATION_REQUIRED`

Independent review confirmed:

- RED test commit `7b53a0eadfd640c92f77e48d2d02a162362dcf86` is test-only;
- implementation `27fe0181...` follows one commit later and changes only `v091-dashboard-verified-delivery.ts`;
- exact run/session/direct-Ticket/numeric Discord fences are present;
- Task-191 Dashboard semantics are preserved;
- no delivery-correlation/lifecycle/schema/provider/release change occurred;
- Validate `33483589170`, Windows Installer Pack Smoke `33483589124`, and PS5.1 Acceptance Smoke `33483589138` are exact-head `completed/success`;
- package-proof artifact is exact-head and retained.

Evidence note: the test-only RED SHA has no remote Actions run; RED was recorded locally and is independently deterministic from commit/source ordering. This does not alter candidate identity or GREEN acceptance.

## Active Task 208

Hermes must execute:

`tasks/CNX-20260901-208-task207-windows-discord-visible-final-requalification.md`

Execution order:

1. fresh read-only host/runtime/provenance baseline;
2. adjudicate the historical Task-205 pending direct-recovery row before any mutation;
3. if the old recovery can still emit delayed Discord output, STOP without install or Send;
4. otherwise perform exactly one supported install-over of exact `27fe0181...` using the retained validated package proof;
5. prove terminal installer exit using a standalone explicit `powershell.exe ... -File install.ps1` child process and bounded polling;
6. prove installed exact provenance + managed/startup/plugin/Gateway/Ollama/delivery/recovery/SQLite health;
7. prove exact Discord channel ID `1531199905673252946`;
8. issue one fresh `CNX208-*` nonce and consume exactly one human Send;
9. prove visible-final semantics, allowing at most one same-run finalization revision if the first natural final is bare `NO_REPLY`;
10. prove one native visible Discord reply and then durable `delivery_confirmed -> completed`.

If a visible Discord reply occurs but durable settlement does not, stop as `FAIL_VISIBLE_REPLY_UNSETTLED__CORRELATION_DEFECT_CONFIRMED`; do not repair correlation in the live task.

## Discord budget

Task-208 human Send budget:

`0 / 1 consumed; 1 / 1 available`

No probe/API/bot/injected/second Send is authorized.

## Hard fence

No reset/uninstall/fresh reinstall, no installer retry, no provider/model/config/schema/manual-SQLite mutation, no source/test/workflow edit, no Release/tag mutation, no force push, and no reply-dispatch/message-sent repair during Task 208.
