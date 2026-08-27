# Review — CNX-20260827-103 Diagnose Live Dashboard Durable-Staging Boundary

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`

Reviewed report:

`docs/operations/coordination/reports/CNX-20260827-103-diagnose-live-dashboard-staging-boundary.md`

Execution HEAD:

`7c1a1aa722a22a726cd67f7dafc3a4c5b55b7c61`

Report HEAD:

`6e271242318db90b6ad1d27cca35971e40a065e4`

## Publication fence

Independent compare confirms execution HEAD -> report HEAD is exactly one commit, ahead by one and behind by zero, and the only changed path is the Task-103 report. No maintained product source, test, runtime, config, SQLite, or other coordination artifact was changed by the executor report commit.

## Contract review

Task 103 explicitly allowed `BLOCKED_ROOT_CAUSE_NOT_YET_ISOLATED` when safe evidence could not select one first failing H1-H6 boundary. The report used that blocker rather than claiming an unsupported root cause.

The report eliminated H1 and H2 with source/dist/installed parity and production-shaped release-registration evidence. It also established that OpenClaw 2026.7.1-2 statically provides the modeled `reply_dispatch`/dispatcher contract and that the real release registration path can produce durable staging in a disposable harness.

The preserved Task-102 live evidence still cannot distinguish H3/H4/H5/H6 because no guaranteed live telemetry recorded handler entry, append-before-deliver execution, final filter inputs/reason, stage return reason, or pre-commit exception. Zero `cnx_assistant_delivery` rows proves the durable write was absent, but does not prove which earlier boundary failed.

Therefore the report correctly refuses to infer handler non-execution from missing non-guaranteed logs and does not prescribe a product behavior fix yet.

## Accepted successor boundary

The next change is bounded observability, not a delivery-logic repair. It must add non-secret diagnostics narrowly around the verified Dashboard delivery path so one operator-assisted live semantic attempt can isolate the first failing boundary.

Required telemetry design:

- handler registration/entry marker;
- run/session correlation only as stable hashes or booleans, never raw prompt/credential/token values;
- dispatcher and `appendBeforeDeliver` availability;
- append-before-deliver callback entry;
- `info.kind`, final queued count, text-present boolean, media-present boolean;
- explicit enumerated filter result;
- stage function entry and enumerated non-staged reason;
- transaction begin/commit outcome and exception class/name without payload text;
- one correlation ID sufficient to join these observations to the single authorized semantic run.

This observability must be source-tested before installation. It must not change routing, staging eligibility, delivery settlement, retry policy, model/provider behavior, or fail-closed semantics.

A later live retest remains separately gated and should reuse the Task-102 proven operator-assisted composer focus procedure. No Task-102 nonce/Ticket/run is reusable.

## Review result

`ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`
