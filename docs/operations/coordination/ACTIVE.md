# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_REDACTED_DASHBOARD_STAGING_OBSERVABILITY`
Current authorization: `OPERATOR_APPROVED_BOUNDED_OBSERVABILITY_IMPLEMENTATION_NO_LIVE_INSTALL`
Task ID: `CNX-20260827-104`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Operator approval

The operator explicitly approved the bounded Task-104 observability design and directed the executor to proceed fully within the approved scope.

No operator action is expected during Task 104. If any step unexpectedly requires manual focus/click/authentication/send/restart/install authorization or another live mutation, stop before that step and report the exact operator action required.

## Task 103 accepted blocker

Task 103 report:

`6e271242318db90b6ad1d27cca35971e40a065e4`

Independent disposition:

`ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`

Task 103 eliminated installed/source/dist parity failure and verified-delivery release-registration failure. The remaining live failure is inside an unobserved boundary between verified `reply_dispatch` invocation and durable `cnx_assistant_delivery` staging.

## Active Task 104

[`tasks/CNX-20260827-104-add-redacted-dashboard-staging-observability.md`](tasks/CNX-20260827-104-add-redacted-dashboard-staging-observability.md)

Goal: add behavior-neutral, secret-safe diagnostics around:

`reply_dispatch registration -> handler entry -> run/dispatcher capability -> appendBeforeDeliver registration -> callback entry -> filter decision -> stage attempt -> stage result/exception -> transaction outcome`

Task 104 is implementation work, but only for observability. It must not repair or redesign delivery behavior.

## Mandatory TDD

Use strict RED -> GREEN:

- write focused failing tests before production changes;
- prove RED fails for missing observability rather than setup/syntax;
- add the minimum implementation;
- prove focused GREEN;
- run full plugin regressions/build/typecheck/lint and required package/installer tests;
- prove behavior equivalence and no secret leakage;
- exercise the real release-registration path in a disposable harness.

## Diagnostic privacy contract

Production telemetry may contain only bounded event/reason names, booleans, non-secret counts, safe exception class/category and optionally short one-way correlation digests.

It must never contain prompt text, response text, nonce content, raw run/session IDs, idempotency keys, delivery markers, credentials, tokens, passwords or provider payloads.

## Build/package requirement

Because runtime payload changes, Task 104 must build the plugin and compute the complete installable-payload v2 fingerprint using the accepted Task-094/095 algorithm, including path/reparse safety verification.

Task 104 does **not** install that payload live.

Preferred success token:

`PASS_REDACTED_DASHBOARD_STAGING_OBSERVABILITY_READY_FOR_LIVE_INSTALL`

## Accepted live baseline

Currently installed source remains:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Currently installed plugin fingerprint remains:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Expected live state remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health.

## Hard fence

Task 104 authorizes isolated source/test/build/package changes necessary for the bounded observability implementation.

It does **not** authorize:

- a new Dashboard semantic nonce or Send;
- sent sentinel;
- Task-102 semantic artifact reuse;
- direct provider probe;
- live SQLite/config/runtime mutation;
- install/install-over/uninstall/reset/cleanup;
- session cleanup/normalization;
- model/provider/timeout change;
- Gateway/Supervisor restart or reboot;
- credential/token/password access or re-entry;
- delivery-logic behavioral repair beyond observability;
- merge/tag/release/force push.

## Publication fence

Use an isolated worktree.

Record execution coordination HEAD, implementation HEAD and report HEAD. The final implementation -> report delta must be report-only.

Report path:

`docs/operations/coordination/reports/CNX-20260827-104-add-redacted-dashboard-staging-observability.md`

After the report is published, stop for independent ChatGPT review before any live install or semantic retest.
