# Active Coordination Task

Status: `IN_PROGRESS`
State: `CNX427_LIVE_9_5_GREEN_FINAL_DISCORD_ACCEPTANCE_PENDING_WITH_STORAGE_RELOCATION`
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

Do not ask for the next Discord acceptance until current storage relocation maintenance is stable.

## Secondary operator-requested maintenance

The operator asked to reclaim C: space by moving CNX backups to T:.

Current state is incomplete:

- C: backup source is still a normal directory and must be preserved;
- C: free ~13.45 GB;
- T: free ~641.19 GB;
- observed T: destination tree is `T:\CogentNexus\CogentNexus-OpenClaw`;
- T: backups currently showed only CNX-425;
- CNX-427 rollback backups are not yet verified on T:;
- no C: junction has been created.

Next session must finish and verify the C: -> T: backup relocation before deleting anything from C:.

Read the full handoff before continuing.
