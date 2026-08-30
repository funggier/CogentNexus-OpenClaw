# CNX-20260830-154 — Dashboard Durable Capture Public-Hook Repair

## Classification

`OFFLINE_REPOSITORY_TDD_REPAIR`

## Owner / executor

- Owner: ChatGPT
- Executor: ChatGPT
- Live Windows executor: not authorized by this task

## Authority

Task 153 is independently `ACCEPT`ed as authoritative read-only root-cause evidence.

Observed production boundary from Task 152/153:

- `reply_dispatch` handler entered;
- event run correlation present;
- dispatcher present;
- `appendBeforeDeliver` absent;
- handler skipped `missing-append-before-deliver`;
- no callback/staging event followed.

Exact OpenClaw runtime/source under acceptance:

- version: `v2026.7.1-2`
- source commit: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

Exact upstream inspection proves:

1. `ReplyDispatcher.appendBeforeDeliver` is optional.
2. `dispatch-from-config.ts` gives `reply_dispatch` hooks an abort-aware dispatcher wrapper that forwards send methods, idle/counter methods, and completion behavior but does not forward `appendBeforeDeliver`.
3. `dispatch.ts` installs the public `reply_payload_sending` hook on the original dispatcher through a core-owned before-delivery function.
4. that public hook receives the final payload, delivery kind, session key, and turn `runId`, and its returned payload is the payload passed onward to native delivery.

Therefore CogentNexus currently binds durable capture to an optional capability at the wrong layer.

## Objective

Repair Dashboard direct-result durable capture without requiring `reply_dispatch` to expose `appendBeforeDeliver`.

The repair must use the OpenClaw public pre-delivery hook contract for the production-shaped fallback while preserving the existing append-before-deliver path when that capability genuinely exists.

## Required TDD sequence

### RED

Add a focused regression that reproduces the production shape:

- active Dashboard direct Ticket with exact run correlation;
- `reply_dispatch` handler receives a dispatcher with **no** `appendBeforeDeliver`;
- the dispatcher still exposes idle and outcome counters;
- the same run later reaches `reply_payload_sending` with one text-only `kind=final` payload;
- expected behavior: exact direct result is durably staged before native delivery and the returned payload contains the durable marker;
- duplicate staging is forbidden.

The test must fail on the current implementation for the intended reason before production source changes.

### GREEN

Implement the smallest repair that satisfies the regression while preserving:

- current behavior when `appendBeforeDeliver` exists;
- one durable row per Ticket generation;
- changed-text fail-closed behavior;
- no duplicate model inference;
- marker-based replay/dedup semantics;
- dispatcher outcome settlement after native delivery;
- telemetry privacy.

Do not weaken duplicate-safety or convert durable capture into post-delivery observation.

### Verification

Run targeted tests first, then the full plugin validation/build/test/package/security gates required by the repository. Exact-SHA GitHub Actions must be green before any repaired live candidate is authorized.

## Upstream compatibility proof required in report

Record exact OpenClaw `0790d9f` evidence for:

- optional `appendBeforeDeliver`;
- abort-aware `reply_dispatch` wrapper omission;
- core-owned `reply_payload_sending` before-delivery installation;
- run-id binding;
- hook-returned payload being used for delivery.

## Required output

Publish:

`docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`

Then stop for independent review before any Windows install-over or Dashboard semantic retry.

## Hard fence

No Dashboard interaction or semantic Send; no live Windows runtime mutation; no install/reset/uninstall/reinstall; no manual Ticket/outbox/delivery/database mutation; no OpenClaw source patch; no dependency upgrade; no merge/tag/release; no force push.
