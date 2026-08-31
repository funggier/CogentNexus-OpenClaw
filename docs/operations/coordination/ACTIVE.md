# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK188_SUBTASK191_SUBTASK192_NO_REPLY_REPAIR_WINDOWS_REQUALIFICATION`
Current disposition: `AWAITING_HERMES_WINDOWS_EXECUTION`
Task ID: `CNX-20260831-188`
Parent repair: `CNX-20260831-191`
Execution subtask: `CNX-20260831-192`
Triggered by: `CNX-20260831-190`
Updated: 2026-08-31 ICT
Executor: Hermes on accepted Windows host + exactly one genuine human Dashboard Send by user
Coordinator / final reviewer: ChatGPT
Human release authority: User

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative for coordination history.

## Current task

[`tasks/CNX-20260831-192-no-reply-repair-windows-requalification.md`](tasks/CNX-20260831-192-no-reply-repair-windows-requalification.md)

Task 192 is the bounded real-Windows verification boundary for Task 191.

## Frozen repaired product candidate

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

This exact SHA is immutable for Task 192.

Later coordination/report commits do not redefine the product candidate and must not be installed as a replacement candidate.

Historical pre-repair candidate `604569c286e930f1a596362ab926b065b56d486e` is no longer release-eligible.

## Repository repair evidence

Task-191 repository report:

[`reports/CNX-20260831-191-no-reply-direct-dashboard-semantic-repair.md`](reports/CNX-20260831-191-no-reply-direct-dashboard-semantic-repair.md)

Repository disposition:

`READY_FOR_WINDOWS_REQUALIFICATION`

TDD evidence:

- RED test-only SHA `94872464781e19d934877ac3346714e3061bd140`;
- RED Validate `33390068431` failed exactly the two intended Task-191 assertions;
- repaired candidate `050ab53f4b593ab538143084d6bbdbf7e1672e34`;
- Validate `33390552591` `completed/success`;
- PS5.1 Acceptance Smoke `33390552613` `completed/success`;
- Windows Installer Pack Smoke `33390552545` `completed/success`;
- Task-191 regression `2/2` PASS;
- plugin suite `54` files / `275` tests PASS on inspected exact-candidate job.

## Candidate identities

- plugin tree: `eeab5fb8c67e5c16284d5df49ec413a53c251a13`
- fixed source blob: `aa97d7a5411f799c612cd0aeece050085298a8bb`
- skill tree: `a1e873ba404205507a1623961b49f1b1a0689f9f`
- skill scripts-tree: `3d9d323ba19443d46e970b87cef52ce878da274f`
- `cnxclaw.py` blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- expected live facade SHA-256 to re-prove: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- package payload-v2: `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93`
- package file count: `186`

## Current objective

Hermes must execute Task 192 continuously through its stop boundary:

1. read-only accepted-host baseline;
2. acquire exact candidate `050ab53f...` in isolation;
3. exactly one supported install-over;
4. prove installed plugin/package/facade identity and runtime health;
5. generate a fresh Task-192 nonce and tell the user exactly what one-line prompt to send in normal OpenClaw Dashboard;
6. user sends exactly once and tells Hermes `ส่งแล้ว`;
7. Hermes immediately continues read-only post-send observation in the same execution context;
8. prove either direct visible completion or at most one same-run sentinel-triggered OpenClaw finalization revision;
9. publish Task-192 report and stop for ChatGPT review.

Hermes must never perform or simulate the human Dashboard Send.

## Hard fence

No reset, uninstall, fresh reinstall, state deletion, provider replacement, OpenClaw version change, source/test/dependency/workflow/schema edit, second human Send, retry/regenerate/injection, release PR merge, Release workflow dispatch, tag/release publication, or force push.

## Publication fence

Task 188 release publication remains blocked until Task-192 real-Windows evidence is committed and accepted by ChatGPT.
