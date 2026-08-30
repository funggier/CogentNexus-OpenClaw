# Coordination Channel Status

**State:** `IN_PROGRESS_CHATGPT`  
**Execution mode:** `OFFLINE_REPOSITORY_TDD_DASHBOARD_DURABLE_CAPTURE_PUBLIC_HOOK_REPAIR`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continued stabilization; Task 153 is independently ACCEPTed and authorizes ChatGPT-owned offline diagnosis/TDD repair before any new live acceptance  
**Execution trigger:** direct ChatGPT repository work; no Hermes/live execution authorized by Task 154

## Active work

Task:

[`tasks/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`](tasks/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md)

Task ID:

`CNX-20260830-154`

## Accepted root-cause evidence

Task 153 report:

`docs/operations/coordination/reports/CNX-20260830-153-task152-redacted-delivery-hook-evidence-collection.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-153-task152-redacted-delivery-hook-evidence-collection-review.md`

Disposition: **ACCEPT**.

Task 152/153 proves the production `reply_dispatch` handler sees a dispatcher but no `appendBeforeDeliver`, so CogentNexus skips before durable staging.

Exact OpenClaw `v2026.7.1-2` source commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` explains why:

- `appendBeforeDeliver` is optional on `ReplyDispatcher`;
- `dispatch-from-config.ts` exposes an abort-aware dispatcher wrapper to `reply_dispatch` and does not forward that optional method;
- `dispatch.ts` separately owns a before-delivery chain on the original dispatcher and invokes public `reply_payload_sending` with the actual payload, delivery kind, session correlation, and turn `runId`;
- the returned hooked payload is then used for native delivery.

## Task-154 TDD gate

No production source change before a genuine RED regression.

Required RED shape:

1. accept/route a direct Dashboard Ticket with active session authority;
2. invoke the registered `reply_dispatch` handler with event run correlation and a dispatcher lacking `appendBeforeDeliver` but retaining idle/outcome counters;
3. invoke the same run's registered `reply_payload_sending` hook with one text-only `kind=final` payload;
4. require durable `direct_result` staging and a marker-bearing returned payload with no duplicate row.

After RED, implement the minimum fallback while preserving the existing append-capable path, duplicate safety, changed-text fail-closed behavior, native-delivery settlement, recovery semantics, and privacy-bounded telemetry.

## Verification gate

Targeted tests must pass first, then full plugin tests/build/validation/package/security gates and exact-SHA GitHub Actions. No live repaired-candidate install-over is authorized until independent review accepts Task 154.

## Required output

ChatGPT must publish:

`docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`

Then stop for independent review.

## Release / live fence

Phase P remains FAIL. No Dashboard semantic Send, Windows install-over, lifecycle mutation, Phase Q, merge, tag, GitHub Release, or promotion is authorized by Task 154. No force push.
