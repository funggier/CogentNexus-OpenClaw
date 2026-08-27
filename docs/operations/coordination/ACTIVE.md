# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_REWORK_REDACTED_DASHBOARD_STAGING_OBSERVABILITY`
Current authorization: `TASK104_OPERATOR_APPROVAL_CONTINUES_FOR_BOUNDED_REWORK_NO_LIVE_INSTALL`
Task ID: `CNX-20260827-104`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 104 implementation/report

Implementation:

`32a6f0a10a98ae52d1a284ee933748f43184b344`

Report:

`32f1d0424ed0dbebe653a77158a9653d5d07e0c2`

Independent review:

[`reviews/CNX-20260827-104-add-redacted-dashboard-staging-observability.md`](reviews/CNX-20260827-104-add-redacted-dashboard-staging-observability.md)

Decision:

`REWORK`

Disposition:

`REWORK_BEHAVIOR_NEUTRALITY_AND_OBSERVABILITY_COVERAGE`

Publication fence itself is valid: implementation -> report is exactly one report-only commit. The implementation is not authorized for live install yet.

## Primary blocker

Task-104 instrumentation changed semantic evaluation order inside the verified `appendBeforeDeliver` callback.

The predecessor returned immediately for:

`info.kind != final` or `owned == true`

before calling `dispatcher.getQueuedCounts()`.

The reviewed implementation calls `getQueuedCounts()` before those guards. Therefore a non-final/already-owned callback can now execute or throw through a dispatcher method that the predecessor never called. This violates Task-104's behavior-neutral invariant.

## Required rework

Hermes/Codex must keep Task 104 in the same bounded observability scope and use strict RED -> GREEN.

Required fixes/evidence:

1. restore predecessor evaluation order exactly;
2. add RED/GREEN proving a non-final callback never calls `getQueuedCounts`, including when that method would throw;
3. add RED/GREEN proving an already-owned second callback never evaluates downstream final-count/media/stage work, returns the second payload unchanged, and creates no duplicate durable row;
4. explicitly assert the `already-owned` diagnostic branch;
5. bound `info.kind` diagnostics to a safe enum/category and prove an unexpected long/synthetic kind is never logged raw;
6. where practical, add behavior-neutral transaction-phase telemetry sufficient to distinguish transaction begun / committed / pre-commit exception; if not practical without altering behavior, document the exact limitation;
7. rerun focused tests, full plugin tests, `plugin:validate`, production-shaped release-entry harness and secret-leak assertions;
8. recompute final installable payload-v2 fingerprint/file count after rework.

No source behavior fix outside observability is authorized.

## Accepted predecessor context

Task 103 remains accepted as:

`ACCEPT_BLOCKER_LIVE_HOOK_BOUNDARY_REQUIRES_REDACTED_OBSERVABILITY`

The currently installed live source remains:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Current installed plugin fingerprint remains:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Expected live state remains MANAGED generation 24.

## Hard fence

Task-104 rework authorizes isolated source/test/build/package changes only for the approved observability design.

It does **not** authorize:

- live install/install-over/uninstall/reset/cleanup;
- new Dashboard semantic nonce/Send or sent sentinel;
- Task-102 semantic artifact reuse;
- direct provider probe;
- live SQLite/config/runtime mutation;
- session cleanup/normalization;
- model/provider/timeout change;
- Gateway/Supervisor restart or reboot;
- credential/token/password access or re-entry;
- unrelated delivery behavior repair;
- merge/tag/release/force push.

## Re-publication gate

After rework, publish a revised Task-104 report with fresh TDD/regression/harness/fingerprint evidence and an implementation -> report publication fence. Stop again for independent ChatGPT review before any live install.
