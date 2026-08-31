# Review — CNX-20260827-104 Add Redacted Dashboard Staging Observability

Decision: `REWORK`

Disposition: `REWORK_BEHAVIOR_NEUTRALITY_AND_OBSERVABILITY_COVERAGE`

Reviewed implementation:

`32a6f0a10a98ae52d1a284ee933748f43184b344`

Reviewed report:

`32f1d0424ed0dbebe653a77158a9653d5d07e0c2`

## Publication fence

Independent compare confirms implementation `32a6f0a...` -> report `32f1d042...` is exactly one report-only commit. The implementation commit itself changes only:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`

The publication fence is valid. This review does not accept the implementation for live install yet.

## Finding 1 — blocker: observability changed callback evaluation order

The predecessor implementation guarded first:

`if (info?.kind !== "final" || owned) return payload;`

Only after that guard did it call `ctx.dispatcher.getQueuedCounts()` and inspect payload/media.

Task-104 implementation now computes `finalCount = Number(ctx.dispatcher.getQueuedCounts?.().final ?? 1)` before checking `info.kind` or `owned`.

That is not behavior-neutral. For a non-final callback or an already-owned callback, the old implementation never called `getQueuedCounts`; the new implementation does. A dispatcher getter with side effects or an exception can therefore change execution or throw on a path that previously returned unchanged.

Required repair:

- restore the original semantic evaluation order exactly;
- emit `callback-entry` / `not-final` / `already-owned` diagnostics without calling any downstream capability that the original path would not have called;
- only read queued final count after the original `final && !owned` guard has passed;
- add a RED regression proving a non-final callback with a throwing/counting `getQueuedCounts` still returns the original payload and never calls that method;
- add the equivalent proof for the already-owned second callback.

## Finding 2 — required coverage: `already-owned` branch is not independently proven

The Task-104 report states that focused tests cover all deterministic filter reasons. The added focused reason test explicitly exercises `not-final`, `empty-text`, `media-present`, and `final-count-not-one`, but the reviewed patch does not independently exercise/assert `already-owned` through the callback path.

Required repair:

- add a focused test that stages/owns the first final callback, invokes the callback again, observes exactly one `already-owned` diagnostic, preserves the second payload unchanged, creates no duplicate durable row, and does not evaluate later filters/counters.

## Finding 3 — privacy hardening: callback `kind` is not bounded

The approved contract allows `kind` only as a bounded enum/string category. The implementation currently logs any string from `info.kind` verbatim. The exact OpenClaw build normally supplies a small runtime enum, but production observability must remain bounded if malformed/unexpected input arrives.

Required repair:

- map `info.kind` to a small safe category/allowlist (for example `final`, `non-final`, `unknown`) or another demonstrably bounded representation;
- add a test with a long/synthetic unexpected kind and prove raw content is absent from diagnostics.

## Finding 4 — transaction outcome remains weaker than the Task-104 target

The approved Task/ACTIVE goal includes transaction outcome where practical. Current telemetry distinguishes `stage-attempt`, `stage-not-staged`, `stage-staged`, and `stage-exception`, but it does not distinguish whether a thrown stage entered the write transaction or whether commit completed before a later failure.

This is not the primary blocker, but because Task 103 specifically left H6 open, the rework should add the narrowest behavior-neutral internal observation that is practical for:

- transaction begun;
- transaction committed;
- exception after transaction begin / before commit.

Do not add SQLite diagnostic rows and do not log identifiers/text. If implementation can prove that adding this would materially alter transaction behavior, document that limitation explicitly instead of forcing it.

## Rework verification

Use the existing Task-104 TDD contract. Required evidence before resubmission:

1. RED for the non-final evaluation-order regression.
2. RED for the already-owned evaluation-order/diagnostic regression.
3. RED for bounded-kind redaction.
4. GREEN focused suite.
5. Full plugin suite and `plugin:validate` fresh.
6. Production-shaped release-entry harness fresh.
7. Behavior-equivalence assertions showing non-final and already-owned callbacks perform no additional semantic calls compared with the predecessor.
8. Recompute payload-v2 fingerprint/file count after the final source/build state.

No live install, restart, Dashboard Send, provider call, or live state mutation is authorized during this rework.

## Success gate

Only after these findings are closed may Task 104 return:

`PASS_REDACTED_DASHBOARD_STAGING_OBSERVABILITY_READY_FOR_LIVE_INSTALL`

Until then, do not create the live install/retest successor.
