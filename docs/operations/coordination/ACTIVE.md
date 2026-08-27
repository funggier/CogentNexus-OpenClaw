# Active Coordination Task

Status: `AWAITING_OPERATOR_DESIGN_APPROVAL`
Execution mode: `SOURCE_TDD_FULL_PLUGIN_PAYLOAD_FINGERPRINT_REPAIR_PENDING_APPROVAL`
Current authorization: `NO_LIVE_OR_SEMANTIC_SUCCESSOR_AUTHORIZED`
Task ID: `PENDING_CNX-20260827-094`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator approval and task publication

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 093 review

Task 093 reported:

`PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`

Implementation:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

Report:

`62fdd69d2a4a27566c0e986171b949347cf0df68`

Independent decision:

`REWORK`

Disposition:

`REWORK_PLUGIN_FINGERPRINT_DOES_NOT_ATTEST_RUNTIME_PAYLOAD`

Review:

[`reviews/CNX-20260827-093-repair-dashboard-durable-payload-staging-boundary.md`](reviews/CNX-20260827-093-repair-dashboard-durable-payload-staging-boundary.md)

## What remains valid from Task 093

The Dashboard durable-staging root cause and minimal source fix are preserved.

Exact OpenClaw `2026.7.1-2` loader review supports the registration-lifetime fix: each plugin registration callback receives a fresh guarded API proxy, while `TicketStore.prototype` remains process-global. Separating prototype patch idempotence from per-runtime `reply_dispatch` hook registration is therefore consistent with the real host lifecycle.

The Task-093 implementation/test commit remains the candidate staging repair and should not be reverted or broadened without a focused RED.

## Blocking deployment-attestation defect

Production `namespace_ownership.py::_plugin_payload()` fingerprints only:

- `openclaw.plugin.json`;
- `package.json`;
- `scripts/bootstrap-ticket-db.mjs`;
- `dist/ticket-store.js`.

It does not fingerprint the rest of the shipped runtime, including `dist/v091-dashboard-verified-delivery.js` changed by Task 093.

Task 093 therefore reported the same fingerprint as the old live plugin even though runtime behavior changed.

This can cause `classify-install` to return `pluginAlreadyExact=true` for the old live runtime and skip package installation, leaving the Task-093 fix unapplied.

## Pending bounded design

Before any live install-over, the next source-only TDD task must replace the four-file sample fingerprint with a deterministic fingerprint over the complete installable plugin payload.

Proposed scope:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` fingerprint helper;
- focused ownership/classification tests only as needed;
- no Dashboard staging behavior change;
- no live installation or semantic send.

Required invariants:

1. hash package-owned runtime files, including all `dist/**`, package/manifest/bootstrap metadata and other files actually shipped;
2. include normalized relative paths + bytes in sorted order;
3. exclude `src/**`, tests, `node_modules/**` and transient npm artifacts that are not installed;
4. reject symlinks/path escape/unsafe payload entries;
5. changing `dist/v091-dashboard-verified-delivery.js` changes fingerprint;
6. exact copied/installed package payload produces the same fingerprint;
7. Task-093 candidate differs from current pre-fix live payload;
8. changed-payload single-generation classification yields `pluginAlreadyExact=false`, then lifecycle actions `installPlugin=true`, `rolloverPlugin=true`;
9. already-exact payload remains `false/false` actions;
10. preserve Task-084/085/086 rollover attestation, plan/apply tree fences, Task-089 installer boundary and npm 11/npm 12 package behavior.

## Hard fence

Until the operator approves this bounded design:

- do not create/run Task 094 implementation;
- no install/install-over/uninstall/reset/cleanup;
- no plugin-generation mutation;
- no semantic message/provider probe;
- no Task-092 record repair;
- no live controller/startup/Supervisor/AGENTS/config/runtime mutation.

## Successor logic

After explicit operator approval, publish the source-only Task 094 contract for full installable-payload fingerprint attestation. Only independent acceptance of that repair can release a live install-over of the Task-093 staging fix.
