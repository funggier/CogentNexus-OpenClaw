# CNX-20260830-154 — Independent Review

## Disposition

`REWORK`

## Scope reviewed

- Task: `CNX-20260830-154`
- Report: `docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`
- Report publication commit: `45828a8be8cb9e93710bf1004f2a53a3405687f8`
- Production repair commits: `e0182d89c91647e7070c2b95fc0b9b0fffc0378a`, `4c5d2d3d0b5d49f47a31cbf49ee45d2b9e1a7c77`
- Verification descendant: `74732d847add15295265afc472ef3455ce89f3f3`
- Exact OpenClaw compatibility source: `v2026.7.1-2` / `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

The report publication commit adds only the matching Task-154 report. The genuine RED evidence and final exact-SHA CI evidence are valid. The public-hook fallback direction is also correct. However one duplicate/changed-text safety condition remains unsatisfied in the fallback implementation and is blocking acceptance.

## Findings accepted

The following Task-154 conclusions are supported:

1. Task 153 correctly identified the pre-staging production boundary: `reply_dispatch` receives a dispatcher without `appendBeforeDeliver` and skips.
2. Exact OpenClaw source proves `appendBeforeDeliver` is optional.
3. Exact `dispatch-from-config.ts` exposes an abort-aware dispatcher wrapper to `reply_dispatch` that forwards send/idle/outcome behavior but does not forward `appendBeforeDeliver`.
4. Exact `dispatch.ts` installs `reply_payload_sending` on the original core dispatcher before native delivery and binds it to the turn `runId`.
5. Exact `reply-dispatcher.ts` uses the hook-returned payload as the payload passed to native delivery.
6. RED SHA `a9c7b069e03498abf71a1ae9253c79e59da10939` is genuine: the focused Task-154 regression alone failed because `reply_payload_sending` was not registered while the predecessor delivery suite remained green.
7. The production repair preserves the existing append-capable path and correctly stages/marks the first qualifying public-hook final.
8. Final verification SHA `74732d847add15295265afc472ef3455ce89f3f3` has green Validate, PS5.1 Acceptance Smoke, and Windows Installer Pack Smoke workflows.

## Blocking finding — already-owned public-hook callback bypasses durable authority

Current fallback code in `v091-dashboard-verified-delivery.ts` performs this guard before inspecting/staging the repeated final:

```ts
if (kind !== "final") return;
if (fallback.owned) return;
```

The exact OpenClaw `reply-payload-sending-hook.ts` contract is important here. If a plugin hook returns no result payload, OpenClaw resolves:

```ts
const payload = (result?.payload as ReplyPayload | undefined) ?? params.payload;
```

and therefore continues native delivery with the original payload.

Consequences after the first final has been durably staged and `fallback.owned` becomes true:

1. A repeated same-text callback returns `undefined` from CogentNexus, so OpenClaw continues with the unmodified original payload instead of the durable marker-bearing payload.
2. A repeated changed-text callback also returns before `stageDashboardDirectResult(...)`, so the existing generation-bound changed-text mismatch check is never reached and cannot fail closed.
3. The final Task-154 regression currently encodes this unsafe behavior by expecting the duplicate public-hook invocation to return `undefined`; it proves only that a second database row is not inserted, not that durable marker ownership or changed-text fail-closed behavior survives hook re-entry.

This conflicts with Task-154's explicit requirements to preserve:

- changed-text fail-closed behavior;
- marker-based replay/dedup semantics;
- duplicate safety, not merely duplicate-row suppression.

The problem is offline and deterministic. It does not require another Windows or Dashboard attempt to prove.

## Required rework

The public-hook fallback must keep one durable row while routing any qualifying re-observation through the existing durable authority rather than bypassing it.

Minimum acceptable behavior:

- first qualifying final: stage once and return marker-bearing `nativeText` as now;
- repeated same-text final for the same armed run/generation: do not insert another row, but return the same durable marker-bearing payload;
- repeated changed-text final for the same armed run/generation: reach the existing durable text-mismatch check and fail closed;
- do not start a second native-settlement waiter;
- preserve the append-capable path unchanged;
- preserve current delivery failure/recovery and privacy behavior.

A narrow implementation can reuse the idempotent `stageDashboardDirectResult(...)` authority on repeated qualifying public-hook callbacks while guarding the worker pulse/waiter so they are started only for first ownership.

## Required RED for successor/rework

Before production adjustment, add regression assertions on the current implementation proving:

1. same-text second `reply_payload_sending` call must return marker-bearing text while durable row count remains exactly one;
2. changed-text second call must throw/fail closed via durable text mismatch;
3. only one settlement waiter is armed;
4. existing append-capable behavior remains unchanged.

The current implementation should fail the first two assertions for the intended reason.

## Safety review

No live Windows or Dashboard work is required for this rework. Do not install the candidate and do not authorize another semantic Send yet.

## Conclusion

`REWORK`

Task 154 established the correct upstream boundary and substantially correct fallback architecture, but it cannot be accepted while an already-owned public-hook callback bypasses the durable marker/text authority. Repair this offline with a focused RED → minimal fix → full exact-SHA verification before repaired-candidate install-over is authorized.
