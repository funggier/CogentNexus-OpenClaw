# Active Coordination Task

Status: `IN_PROGRESS`
State: `CNX427_OPENCLAW95_TICKET_FIRST_GREEN_FINAL_DISCORD_ACCEPTANCE_READY`
Execution mode: `CONTROLLED_LIVE_ACCEPTANCE_AND_MAINTENANCE`
Task ID: `CNX-20260919-427`
Parent: `CNX-20260919-426`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Task: `docs/operations/coordination/tasks/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair.md`
Report: `docs/operations/coordination/reports/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair-report.md`
Handoff: `docs/operations/coordination/reports/CNX-20260919-427-full-session-handoff-openclaw-9.5-and-storage-relocation.md`

## Primary runtime state

OpenClaw live is now `2026.9.5 (ec9c1a1)` and settled GREEN:

- Gateway health ok;
- event loop not degraded;
- Discord connected/ready;
- plugin errors 0;
- Tailscale Serve active;
- remote HTTPS 200;
- CNX runner ready;
- supervisor Enabled / Last Result 0.

OpenClaw 9.5 was selected because upstream commit `983782594807a23c006b49bd16172b1ba6980924` preserves admitted runtime generation for channel turns, directly matching the Discord/Codex Ticket-first continuity defect reproduced twice on 9.4.

## CNX-428 OpenClaw 9.5 startup-grace repair

The OpenClaw 9.5 cold-start interaction discovered during CNX-427 is repaired and live-qualified.

- repair implementation: `13dfba9a55f4d64ceb9aa8440670c9ee9792354a`;
- actual OpenClaw 9.5 cold start measured about 90.7 s to `gateway ready`;
- the previous two-probe/1-second rule falsely restarted valid cold starts;
- the supervisor now uses a bounded 180-second grace grounded in `gateway_boot_lifecycle`;
- live boot id `2457011a-c738-4e74-912d-3f309236455d` classified `gateway-starting` without calling restart;
- stale `healthy-runtime` maintenance converged through the supported lifecycle path;
- recurring supervisor is Enabled with `LastTaskResult=0` and no new restart request.

Task/report:

- `docs/operations/coordination/tasks/CNX-20260919-428-openclaw-9.5-supervisor-cold-start-grace-repair.md`
- `docs/operations/coordination/reports/CNX-20260919-428-openclaw-9.5-supervisor-cold-start-grace-repair-report.md`

A PID-bound isolated Gateway probe also proved the OpenClaw 9.5 execution generation carries CNX Ticket-first admission correctly: one process -> one user turn -> one host run -> one Ticket -> one model call, with Ticket persistence before model-call authority. The small probe model timed out at 90 s and terminated without duplicate/recovery inference, so it does not replace the final Discord delivery acceptance.

## Remaining primary acceptance

CNX-427 is NOT final PASS yet.

One new Discord turn on live 9.5 must prove:

- one authoritative host run;
- exactly one CNX Ticket;
- Ticket-first before inference authority;
- one model execution;
- one Discord delivery;
- correct terminal Ticket state;
- no duplicate Ticket or stale lane.

Storage/runtime maintenance and pre-inference Ticket-first qualification are now stable. The next operator action is exactly one genuine new Discord acceptance turn; do not substitute another CLI/synthetic turn for that final ingress proof.

## Secondary operator-requested maintenance

The operator-requested C: -> T: backup relocation is complete and verified.

Current state:

- canonical destination: `T:\CogentNexus\CogentNexus-OpenClaw`;
- C: `backups` is an NTFS junction to the T: backup tree;
- C: `plugin-generation-rollover-backups` is an NTFS junction to the T: rollover tree;
- main backup dry mirror: 509,383 files / 9.479 GiB, copied 0, mismatch 0, failed 0, extras 0;
- rollover dry mirror: 159,271 files / 1.408 GiB, copied 0, mismatch 0, failed 0, extras 0;
- authoritative CNX-427 manifest and critical hashes match source/target;
- authoritative reparse count matches 10 -> 10;
- old C: rollback/report paths resolve through the junction;
- reparse-safe source cleanup completed with no failed deletions;
- C: free space increased from ~13.43 GiB to ~25.48 GiB.

Checkpoint:

`docs/operations/coordination/reports/CNX-20260919-427-storage-relocation-and-pre-acceptance-runtime-checkpoint.md`

The only remaining CNX-427 gate is one new live Discord acceptance turn on OpenClaw 2026.9.5.
