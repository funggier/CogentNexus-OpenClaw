# Active Coordination Task

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `REPOSITORY_DASHBOARD_DURABLE_DELIVERY_PATH_REPAIR`
Current authorization: `CNX-20260830-161_REPOSITORY_DASHBOARD_DURABLE_DELIVERY_PATH_REPAIR`
Task ID: `CNX-20260830-161`
Updated: 2026-08-30 ICT
Owner / coordinator / executor / reviewer: ChatGPT
Review type at completion: self-review / non-independent

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-161-dashboard-live-durable-delivery-path-repair.md`](tasks/CNX-20260830-161-dashboard-live-durable-delivery-path-repair.md)

## Trigger

Task 160 is durably reviewed `FAIL`:

`docs/operations/coordination/reviews/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance-review.md`

The one authorized live Dashboard Send had valid candidate provenance and healthy runtime, completed its model call, and reached `response_ready`, but no authoritative durable delivery row was committed. The Ticket terminal-failed through `missing-append-before-deliver` / no-regeneration protection.

## Task-161 execution contract

ChatGPT must:

1. establish exact OpenClaw Dashboard/webchat control flow at the installed upstream version before production change;
2. determine why the accepted CogentNexus durable-delivery fallback did not establish durable authority;
3. create a valid RED regression for the demonstrated mechanism;
4. implement the smallest safe CogentNexus-OpenClaw repair;
5. preserve Task-155 duplicate-safe authority and no-regeneration safeguards;
6. run full relevant repository/plugin/Windows validation on the exact repair SHA;
7. publish Task-161 report and explicit self-review.

## Hard fence

Repository-only. No Dashboard semantic Send or semantic UI interaction; no live Windows install/uninstall/reinstall/reset; no manual durable-state mutation; no OpenClaw source patch; no dependency upgrade; no unrelated behavior change; no release/promotion; no force push.

Even Task-161 ACCEPT does not authorize another Dashboard Send. A separate repaired-candidate Windows install-over acceptance checkpoint is required first.
