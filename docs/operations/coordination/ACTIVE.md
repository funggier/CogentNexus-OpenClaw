# Active Coordination Task

Status: `WAITING_FOR_OPERATOR_SEMANTIC_SEND`
State: `CNX425_WAITING_FOR_OPERATOR_SEMANTIC_SEND`
Execution mode: `CONTROLLED_LIVE_OPENCLAW_2026_9_4_POST_UPGRADE_ACCEPTANCE`
Task ID: `CNX-20260919-425`
Parent: `CNX-20260919-424`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Task: `docs/operations/coordination/tasks/CNX-20260919-425-controlled-live-openclaw-2026-9-4-upgrade-and-post-upgrade-acceptance.md`
Report: `docs/operations/coordination/reports/CNX-20260919-425-controlled-live-openclaw-2026-9-4-upgrade-and-post-upgrade-acceptance-report.md`

## Current position

The live OpenClaw host is now running exact `2026.9.4`.

Non-semantic acceptance is GREEN:

- Gateway health `ok=true`;
- live listener `127.0.0.1:18789`;
- sessions `19`;
- plugin errors `0`;
- qualified CNX plugin hash matches;
- reply_dispatch registration observed;
- Discord connected/ready;
- DB quick_check PASS;
- CNX runtime counters preserved;
- CNX supervisor restored and one tick returned result `0`.

Managed Tailscale exposure is temporarily `off` because the external Tailscale daemon remains `NoState`. The local Gateway is healthy and the rollback snapshot is retained.

## Required operator action

Open/refresh:

`http://127.0.0.1:18789/`

Create a new Dashboard session, explicitly select:

- provider: `OpenAI`
- model: `gpt-5.6-luna`

Send exactly one message:

`CNX-425 semantic acceptance — reply exactly CNX425_OK`

Do not resend.

After the operator reports that the message was sent, ChatGPT must inspect the live Ticket/run/route/inference/delivery evidence and complete CNX-425.
