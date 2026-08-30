# Active Coordination Task

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `OFFLINE_REPOSITORY_TDD_PUBLIC_HOOK_DUPLICATE_DURABLE_AUTHORITY_REWORK`
Current authorization: `CNX-20260830-155_DASHBOARD_PUBLIC_HOOK_DUPLICATE_DURABLE_AUTHORITY_REWORK`
Task ID: `CNX-20260830-155`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: ChatGPT; no live Windows execution authorized

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`](tasks/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md)

Task 155 is the narrow offline RED-first rework required by the independent Task-154 review. No live install/install-over and no Dashboard semantic Send are authorized.

## Task-154 disposition

Report:

`docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-154-dashboard-durable-capture-public-hook-repair-review.md`

Disposition: **REWORK**.

Accepted Task-154 findings remain valid: the production `reply_dispatch` wrapper lacks optional `appendBeforeDeliver`, and `reply_payload_sending` is the correct public before-delivery fallback. The blocking defect is narrower: once fallback ownership is established, repeated qualifying callbacks return early before the durable stage/text authority is re-applied.

## Task-155 execution contract

ChatGPT must use RED -> minimal GREEN -> full verification.

Required RED must show that, on current code:

1. repeated same-text `reply_payload_sending` final returns no marker-bearing replacement instead of reusing durable `nativeText`;
2. repeated changed-text final bypasses durable mismatch failure instead of failing closed;
3. durable row remains singular;
4. only one waiter/pulse ownership sequence is permitted.

Production repair must route repeated qualifying callbacks through the idempotent durable staging authority while guarding first-ownership waiter/pulse side effects. Existing append-capable behavior must remain unchanged.

## Required completion signal

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`

Then stop for independent review before any Windows install-over or Dashboard reacceptance.

## Hard fence

No Dashboard click/focus/type/paste/Send; no semantic transport; no live Windows/runtime mutation; no lifecycle/reset/install/uninstall/reinstall; no manual semantic/database/plugin/controller mutation; no OpenClaw source patch; no dependency upgrade; no merge/tag/release; no force push.
