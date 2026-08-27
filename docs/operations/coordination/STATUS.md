# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator approved the bounded Task-104 redacted observability implementation and directed full execution within scope
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Currently installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Currently installed plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Expected live state remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health.

## Task 103 accepted result

Report:

`6e271242318db90b6ad1d27cca35971e40a065e4`

Independent disposition:

`ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`

Task 103 proved source/dist/package/installed runtime parity, active release registration, and exact OpenClaw 2026.7.1-2 static hook compatibility. A production-shaped disposable harness stages successfully with the modeled callback shape.

The preserved live run lacks guaranteed telemetry to distinguish handler non-entry, context/capability mismatch, filter rejection, stage non-staged result or pre-commit exception. A behavior-neutral observability implementation is therefore the next bounded step.

## Active Task 104

[`tasks/CNX-20260827-104-add-redacted-dashboard-staging-observability.md`](tasks/CNX-20260827-104-add-redacted-dashboard-staging-observability.md)

Execution mode:

`SOURCE_TDD_REDACTED_DASHBOARD_STAGING_OBSERVABILITY`

Authorization:

`OPERATOR_APPROVED_BOUNDED_OBSERVABILITY_IMPLEMENTATION_NO_LIVE_INSTALL`

Task 104 must add narrowly scoped diagnostics covering:

- verified API hook registration;
- `reply_dispatch` handler entry;
- run-correlation presence;
- dispatcher / `appendBeforeDeliver` availability;
- before-deliver callback registration and invocation;
- final kind, final count, text/media booleans;
- deterministic early-return/filter reason;
- stage attempt;
- staged/non-staged reason;
- safe staging exception category;
- transaction outcome where practical without behavioral change.

Production logs must not contain prompt/response text, nonce content, raw run/session IDs, credentials, tokens, passwords, provider payloads, idempotency keys or delivery markers.

## Mandatory verification

Task 104 uses strict TDD RED -> GREEN and must provide:

- focused RED evidence on the current implementation;
- minimal GREEN implementation;
- focused and full plugin regression results;
- build/typecheck/lint results;
- behavior-equivalence tests;
- explicit secret-leak tests;
- production-shaped real release-registration harness evidence;
- complete installable-payload v2 fingerprint and file count with path/reparse safety verification.

Preferred result token:

`PASS_REDACTED_DASHBOARD_STAGING_OBSERVABILITY_READY_FOR_LIVE_INSTALL`

## Operator assistance

No manual operator action is expected during Task 104.

If source work unexpectedly reaches a point requiring live install, restart, authentication, Dashboard focus/click or semantic Send, Hermes/Codex must stop before that action and report exactly what the operator needs to do.

A later live semantic diagnostic retest, after independent review and install acceptance, will likely use the proven operator-assisted procedure: open/keep the authenticated Firefox Dashboard, allow Codex to identify the exact composer, manually click `Message Assistant` once when explicitly instructed, then avoid changing focus until Codex re-verifies the input target. A semantic Send remains single-attempt and separately gated.

## Hard fence

Task 104 does not authorize:

- live install/install-over/uninstall/reset/cleanup;
- new semantic nonce/Send or sent sentinel;
- provider probe;
- live SQLite/config/runtime mutation;
- session cleanup;
- Gateway/Supervisor restart or reboot;
- model/provider/timeout change;
- credential access/re-entry;
- behavioral delivery fix outside observability;
- merge/tag/release/force push.

Report path:

`docs/operations/coordination/reports/CNX-20260827-104-add-redacted-dashboard-staging-observability.md`

After report publication, independent ChatGPT review is required before any live deployment.
