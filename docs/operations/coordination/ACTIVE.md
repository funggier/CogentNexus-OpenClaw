# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_HERMES`
Current authorization: `CNX-20260830-163_HERMES_REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR`
Task ID: `CNX-20260830-163`
Updated: 2026-08-30 ICT
Executor: Hermes
Coordinator / final reviewer: ChatGPT
Review type at completion: ChatGPT review required

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair.md`](tasks/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair.md)

## Parent task

Task 162 remains the parent repository repair objective:

`tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`

Task 163 delegates the unresolved source-trace / authority-boundary / TDD repair attempt to Hermes. ChatGPT remains coordinator and must review Hermes' report before any successor authorization.

## Task-163 execution contract

Hermes must:

1. re-read fresh GitHub branch state before work and before every write;
2. read Task 162 and its session handoff checkpoint;
3. trace exact installed OpenClaw Dashboard/webchat final-delivery behavior at upstream commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`;
4. prove a plugin-accessible authoritative persistence/verification boundary that prevents native-send + recovery-inject duplication, or report `BLOCKED` with exact evidence;
5. commit a production-faithful test-only RED regression before any production source change;
6. only after verified RED, implement the smallest safe CogentNexus-OpenClaw repair;
7. preserve Task-155 duplicate-safe authority and no-regeneration safeguards;
8. run the required repository/plugin/Windows hosted validation on the exact repair SHA;
9. publish the Task-163 report for ChatGPT review.

## Hard fence

Repository-only. No Dashboard semantic Send or semantic UI interaction; no real Windows install/uninstall/reinstall/reset; no Gateway/Ollama/Supervisor live restart; no manual durable-state mutation; no OpenClaw source patch; no dependency upgrade; no unrelated product change; no release/promotion; no merge to default/release branch; no force push.

Even Task-163 PASS does not authorize another Dashboard Send or live Windows mutation. ChatGPT must review and explicitly accept the evidence first.
