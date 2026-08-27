# Coordination Channel Status

**State:** `AWAITING_OPERATOR_DESIGN_APPROVAL`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and requires fresh-session behavior in final acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted baseline

Accepted source/live lineage through Tasks 078/079/080, 082, 084/085/086, 089, 090 and 091 remains in force.

Task 090 live recovery remains accepted: MANAGED, single canonical loaded plugin, source/live parity at that accepted source, Gateway/Ollama/SQLite healthy and `NO_FLASH_MULTI_TICK_PROVEN`.

Task 091 authenticated Dashboard/WebChat owner surface remains accepted without secret disclosure.

## Task 092 accepted blocker

Task 092 proved the first fresh-session path, Ticket-before-provider ordering, one correlated Ollama inference and one visible exact nonce, but durable delivery did not converge because no `cnx_assistant_delivery` row was staged. Independent disposition remains:

`ACCEPT_BLOCKER_DASHBOARD_DURABLE_PAYLOAD_STAGING`

Task-092 semantic artifacts are retired evidence and are not to be repaired or reused.

## Task 093 result and independent review

Implementation:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

Report:

`62fdd69d2a4a27566c0e986171b949347cf0df68`

Reported result:

`PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`

Independent decision:

`REWORK`

Disposition:

`REWORK_PLUGIN_FINGERPRINT_DOES_NOT_ATTEST_RUNTIME_PAYLOAD`

Review:

`docs/operations/coordination/reviews/CNX-20260827-093-repair-dashboard-durable-payload-staging-boundary.md`

Publication fence is valid: execution -> implementation is one source/test commit and implementation -> report is one report-only commit.

## Preserved Task-093 source repair

The root cause is credible: one process-global prototype marker previously suppressed a legitimate later runtime `reply_dispatch` registration. Exact upstream OpenClaw `0790d9f` creates a fresh plugin API and a fresh guarded registration proxy per registration callback, so separating prototype lifetime from per-runtime hook lifetime is consistent with the real host lifecycle.

The Task-093 Dashboard staging source/test commit remains the candidate repair.

## New blocking attestation finding

Production plugin fingerprinting is too narrow.

`namespace_ownership.py::_plugin_payload()` hashes only four files:

- `openclaw.plugin.json`;
- `package.json`;
- `scripts/bootstrap-ticket-db.mjs`;
- `dist/ticket-store.js`.

It does not bind the rest of the installed runtime package. Task 093 changed code that compiles into `dist/v091-dashboard-verified-delivery.js`, yet its recorded fingerprint remained identical to the currently installed pre-fix plugin.

Because `classify-install` uses this fingerprint for `pluginAlreadyExact`, a live successor could incorrectly skip installing the Task-093 repair.

No live install successor is authorized until this fingerprint authority is repaired.

## Pending bounded repair design

The proposed next task is source-only TDD and will make plugin fingerprinting deterministic over the complete installable payload rather than a four-file sample.

The intended fingerprint domain is package-owned runtime content: sorted normalized relative path + file bytes for `package.json`, package manifest/metadata, shipped bootstrap/README files and all `dist/**` runtime files. Development-only `src/**`, tests, `node_modules/**` and transient npm artifacts remain excluded. Unsafe symlinks/path escapes must fail closed.

Required proof includes:

- changing Task-093 runtime JS changes the fingerprint;
- exact copied/installed payload hashes identically;
- changed-payload classification becomes `pluginAlreadyExact=false` and actions become install+rollover;
- exact payload remains no-install/no-rollover;
- all same-version rollover plan/apply and npm compatibility gates remain green.

## Hard fence while awaiting approval

No Task-094 implementation, live install/reset/repair, generation mutation, semantic message, direct provider probe, model/config/runtime change or Task-092 state rewrite is authorized.

## Successor logic

After explicit operator approval of the bounded design, Task 094 may be published for source-only TDD fingerprint repair. Only independent acceptance of that repair may authorize installing the Task-093 staging fix live and then rerunning final fresh-session semantic acceptance.
