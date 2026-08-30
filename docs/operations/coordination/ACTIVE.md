# Active Coordination Task

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_CONTINUATION`
Current authorization: `CNX-20260830-162_REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_CONTINUATION`
Task ID: `CNX-20260830-162`
Updated: 2026-08-30 ICT
Owner / coordinator / executor / reviewer: ChatGPT
Review type at completion: self-review / non-independent

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`](tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md)

## Predecessor

Task 161 remains the repository-repair predecessor whose investigation is continued by Task 162:

`tasks/CNX-20260830-161-dashboard-live-durable-delivery-path-repair.md`

No Task-161 RED regression or production repair had been committed before the rollover checkpoint.

## Trigger

Task 160 is durably reviewed `FAIL`, and Task 161 established additional source-level causal evidence before the ChatGPT context rollover:

- the real OpenClaw `reply_dispatch` hook runs before normal model dispatch;
- that hook receives an abort-aware dispatcher wrapper without `appendBeforeDeliver`;
- the normal final answer is later sent through the original dispatcher;
- therefore the Task-154 fallback cannot rely on pre-model `reply_dispatch` owning final persistence or on a later `reply_payload_sending` callback being guaranteed;
- exact upstream `before_agent_finalize` is an awaited post-model/pre-terminal hook with `lastAssistantMessage`, but it is not yet sufficient by itself because native-send plus recovery-inject duplicate safety must be proven;
- exact upstream Gateway `chat.ts` owns the next authoritative source path to trace: webchat final dispatcher delivery, transcript append, idempotency, and settlement order.

The durable continuation details and exact next investigation are recorded in Task 162.

## Task-162 execution contract

ChatGPT must:

1. re-read fresh branch state before every write;
2. continue exact installed OpenClaw Dashboard/webchat final-delivery tracing at upstream commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`;
3. identify a plugin-accessible authoritative persistence/verification boundary that prevents native-send + recovery-inject duplication;
4. create and commit a production-faithful test-only RED regression before any production source change;
5. implement the smallest safe CogentNexus-OpenClaw repair only after verified RED;
6. preserve Task-155 duplicate-safe authority and no-regeneration safeguards;
7. run full relevant repository/plugin/Windows validation on the exact repair SHA;
8. publish Task-162 report and explicit self-review.

## Hard fence

Repository-only. No Dashboard semantic Send or semantic UI interaction; no live Windows install/uninstall/reinstall/reset; no Gateway/Ollama/Supervisor live restart for this task; no manual durable-state mutation; no OpenClaw source patch; no dependency upgrade; no unrelated behavior change; no release/promotion; no force push.

Even Task-162 ACCEPT does not authorize another Dashboard Send. A separate repaired-candidate Windows install-over acceptance checkpoint is required first.
