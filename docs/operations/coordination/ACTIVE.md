# Active Coordination Task

Status: `AWAITING_OPERATOR_DESIGN_APPROVAL`
Execution mode: `REDACTED_LIVE_HOOK_OBSERVABILITY_PENDING_APPROVAL`
Current authorization: `NO_NEW_SEMANTIC_SEND_OR_PRODUCT_IMPLEMENTATION_AUTHORIZED`
Task ID: `PENDING_CNX-20260827-104`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator design approval

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 103 independent review

Task 103 report:

`6e271242318db90b6ad1d27cca35971e40a065e4`

Decision:

`ACCEPT`

Disposition:

`ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`

Review:

[`reviews/CNX-20260827-103-diagnose-live-dashboard-staging-boundary.md`](reviews/CNX-20260827-103-diagnose-live-dashboard-staging-boundary.md)

Independent publication-fence verification confirms execution `7c1a1aa722a22a726cd67f7dafc3a4c5b55b7c61` -> report `6e271242318db90b6ad1d27cca35971e40a065e4` is exactly one report-only commit.

## What Task 103 proved

H1 and H2 are eliminated:

- repository source, dist, package manifest and installed live runtime were byte/content consistent at the active plugin boundary;
- the active v0.9.1 release entry registers the verified-delivery installer;
- a disposable production-shaped release-registration harness captures the verified `reply_dispatch` handler and can create one durable `cnx_assistant_delivery` row with the modeled callback shape.

The exact OpenClaw 2026.7.1-2 runtime/type contract statically provides `reply_dispatch`, run correlation, dispatcher access and `appendBeforeDeliver`.

The remaining live Task-102 evidence cannot safely choose among H3/H4/H5/H6 because no guaranteed live telemetry captured:

- verified handler entry;
- append-before-deliver callback entry;
- actual live filter inputs/reason;
- stage return reason;
- staging exception/transaction outcome.

Therefore Task 103 correctly reported:

`BLOCKED_ROOT_CAUSE_NOT_YET_ISOLATED`

No delivery-logic fix is authorized yet.

## Pending Task 104 bounded design

Classification: bounded observability change to the existing verified Dashboard delivery path.

Proposed behavior:

1. add narrowly scoped redacted diagnostics around `installV091DashboardVerifiedDelivery` / `reply_dispatch` / `appendBeforeDeliver` / `stageDashboardDirectResult`;
2. record only booleans, enumerated reasons, counts, exception class/name and stable hashed correlation IDs;
3. never record prompt text, assistant payload text, nonce content, credentials, tokens, provider payloads or secret values;
4. distinguish at minimum:
   - handler registered/entered;
   - run correlation present/missing;
   - dispatcher and `appendBeforeDeliver` availability;
   - before-deliver callback entry;
   - `info.kind`;
   - queued final count;
   - text-present/media-present booleans;
   - explicit filter skip reason;
   - stage entered;
   - stage non-staged reason;
   - transaction begin/commit outcome;
   - exception class/name;
5. observability must not alter routing, eligibility, staging text/marker, settlement, retry/fail-closed behavior, provider/model selection or timing semantics;
6. TDD/source tests must prove redaction and every diagnostic branch through the real release-registration path;
7. build/dist/package fingerprint impact must be reported before any install-over;
8. Task 104 itself should implement and verify source observability only. A live semantic retest remains a successor gate unless the operator separately approves combining installation/retest.

Suggested Task-104 result token:

`PASS_REDACTED_DASHBOARD_DELIVERY_OBSERVABILITY_READY`

## Operator assistance

No operator action is required while the Task-104 source observability change is developed/tested.

A later live semantic retest will likely require the already-proven manual handoff:

- keep/open the authenticated Firefox Dashboard;
- wait until Codex identifies the exact target composer;
- manually click the exact `Message Assistant` composer once when instructed;
- avoid clicking elsewhere until Codex re-verifies foreground/input ownership;
- perform no Send unless explicitly instructed for the one authorized semantic attempt.

Coordination must notify the operator immediately before any such manual step.

## Hard fence pending approval

Until the operator approves the bounded Task-104 design:

- do not create/run Task 104 implementation;
- no product-source/test edits;
- no new semantic nonce or Dashboard Send;
- do not reuse Task-102 semantic artifacts;
- no provider probe;
- no install/install-over/uninstall/reset/cleanup;
- no live SQLite/config/runtime mutation;
- no restart/reboot;
- no credential/token/password access or re-entry;
- no merge/tag/release/force push.
