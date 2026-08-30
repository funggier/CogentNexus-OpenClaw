# Active Coordination Task

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `OFFLINE_REPOSITORY_TDD_DASHBOARD_DURABLE_CAPTURE_PUBLIC_HOOK_REPAIR`
Current authorization: `CNX-20260830-154_DASHBOARD_DURABLE_CAPTURE_PUBLIC_HOOK_REPAIR`
Task ID: `CNX-20260830-154`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: ChatGPT; no live Windows execution authorized

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`](tasks/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md)

Task 154 repairs the Phase-P durable-capture defect offline using TDD. No new Dashboard semantic attempt is authorized.

## Task-153 disposition

Report:

`docs/operations/coordination/reports/CNX-20260830-153-task152-redacted-delivery-hook-evidence-collection.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-153-task152-redacted-delivery-hook-evidence-collection-review.md`

Disposition: **ACCEPT**.

The first proven failure boundary is `HANDLER_SKIPPED_MISSING_APPEND_BEFORE_DELIVER`.

Exact OpenClaw `v2026.7.1-2` / `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` source inspection shows `appendBeforeDeliver` is optional and the `reply_dispatch` hook receives an abort-aware dispatcher wrapper that does not forward that optional method. The same OpenClaw source installs `reply_payload_sending` through a core-owned before-delivery hook on the original dispatcher with turn run correlation and payload rewrite support.

## Task-154 execution contract

ChatGPT must use RED → minimal GREEN → full verification.

RED must reproduce the production-shaped dispatcher where `reply_dispatch` has no `appendBeforeDeliver`, then require the same run's `reply_payload_sending` final payload to be durably staged and marker-bearing before native delivery.

Production repair must preserve the existing append path when available, exactly-once durable staging, changed-text fail-closed behavior, marker replay/dedup semantics, delivery outcome settlement, and telemetry privacy.

## Required completion signal

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`

Then stop for independent review before any Windows install-over or new Dashboard acceptance.

## Hard fence

No Dashboard click/focus/type/paste/Send; no semantic transport; no live Windows/runtime mutation; no lifecycle/reset/install/uninstall/reinstall; no manual semantic/database mutation; no OpenClaw source patch; no dependency upgrade; no merge/tag/release; no force push.
