# Active Coordination Task

Status: `READY_FOR_EXECUTION`
State: `CNX425_READY_FOR_EXECUTION`
Execution mode: `CONTROLLED_LIVE_OPENCLAW_2026_9_4_UPGRADE_AND_ACCEPTANCE`
Task ID: `CNX-20260919-425`
Parent: `CNX-20260919-424`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Review: `docs/operations/coordination/reviews/CNX-20260919-424-chatgpt-review.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260919-425-controlled-live-openclaw-2026-9-4-upgrade-and-post-upgrade-acceptance.md`
Expected report: `docs/operations/coordination/reports/CNX-20260919-425-controlled-live-openclaw-2026-9-4-upgrade-and-post-upgrade-acceptance-report.md`

## Current position

CNX-424 review result:

`ACCEPTED_PASS__CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_AUTHORIZED`

The live host may now be upgraded from `2026.7.1-2` to exact `2026.9.4` under rollback-first controls.

## Mandatory first actions

1. record live version/health/session/plugin/state preflight;
2. identify the normal Gateway ownership/start mechanism;
3. gracefully stop live Gateway;
4. create and verify a complete rollback snapshot outside `~/.openclaw`;
5. preserve old OpenClaw global package/wrappers and state/config/workspace/CNX DB;
6. only then install/migrate exact 2026.9.4.

No semantic provider traffic before non-semantic post-upgrade gates pass.
