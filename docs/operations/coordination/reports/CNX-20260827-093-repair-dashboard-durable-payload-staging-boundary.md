# CNX-20260827-093 — Repair Dashboard Durable Payload Staging Boundary

Result: `PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`

## Scope and fence

This task was executed as source/test-only. No live install-over, runtime restart, plugin-generation mutation, provider/model/timeout change, SQLite rewrite, semantic message, direct Ollama/provider probe, or Task-092 record repair was performed.

Task-092 evidence was preserved as retired evidence. Its exact Ticket/run/session remained unchanged during this task.

## Phase A — publication and evidence re-proof

- Coordination branch was fetched and reset to remote before work.
- Execution HEAD before source edit: `dad3f991f5dd392d8dff602584c13e80c36ddf03`
- Task-092 report commit was present in ancestry: `0939c8b0659f0254c754dd7bbf44dc422648c4da`
- Task-092 accepted independent review remained present in the coordination branch.
- Source implementation commit: `a924157ecdedef1d4f166d5762529b0d59536fc9`
- Live runtime was not mutated.

## Phase B — root cause

H1 was proven against the accepted source and executable reproduction.

`installV091DashboardVerifiedDelivery()` used the same `TicketStore.prototype` symbol as an early-return guard for both:

1. one-time prototype method patching; and
2. runtime `api.on('reply_dispatch', ...)` registration.

The previous source returned immediately when the prototype was already patched. Therefore a legitimate later plugin registration in the same Node process inherited the patched TicketStore methods but received no `reply_dispatch` staging hook. This precisely permits `response_ready` and fail-closed unverifiable-delivery behavior without a `cnx_assistant_delivery` row.

## Gate R — RED

A regression assertion was added to the existing production-shaped v0.9.1 Dashboard delivery test. It performs a second legitimate `installV091DashboardVerifiedDelivery()` call with a distinct runtime API object and requires a second `reply_dispatch` hook.

Before the production edit, the focused test failed as intended:

```text
1 failed, 1 passed
expected undefined to be type of 'function'
```

The failure occurred at the second-registration hook assertion, proving the source boundary rather than a test-only copy of the logic.

## Gate F — minimal fix

The fix separates the two lifetimes:

- `needsPrototypePatch` guards only the one-time `TicketStore.prototype` method patch.
- A module-level `WeakSet<object>` named `REGISTERED_APIS` guards one hook registration per active runtime API object.
- A later legitimate API object receives exactly one `reply_dispatch` hook even when the prototype is already patched.
- Repeated registration with the same API object remains idempotent.
- No owner admission, payload correlation, recovery, settlement, or timeout semantics were changed.

## Gate T and verification

Focused Dashboard verified-delivery suite:

- RED before fix: expected failure on second registration.
- GREEN after fix: `2 tests passed`.
- Existing production-shaped test still proved durable exact text staging, marker binding, idempotent re-observation, changed-text fail-closed behavior, generic receipt non-terminal behavior, recovery non-regeneration, successful settlement, and non-Dashboard rejection.

Node 24.18.0 / npm 11.16.0:

- clean `npm ci --ignore-scripts`: exit `0`
- full plugin suite: `49 passed`, `257 passed`
- `npm run plugin:validate`: exit `0`
- TypeScript build: pass
- schema verification: pass
- ticket DB bootstrap: pass
- package-content verification: pass (`176` packed files)

Node 22.23.2 / npm 12.0.2 isolated execution path:

- clean `npm ci --ignore-scripts`: exit `0`
- full plugin suite: `49 passed`, `257 passed`
- `npm run plugin:validate`: exit `0`
- TypeScript build: pass
- schema verification: pass
- ticket DB bootstrap: pass
- package-content verification: pass (`176` packed files)

Python repository suite in an isolated dev venv outside the clone:

```text
374 passed, 2 skipped, 4 subtests passed
```

The two skips are existing platform-conditional tests. Baseline consistency:

```text
CogentNexus-OpenClaw v0.9.3 baseline consistency: PASS (Bridge v0.9.3)
```

`git diff --check`: pass.

## Source fingerprint

The exact new plugin payload fingerprint for the later authorized install-over task is:

```text
8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360
```

This source fingerprint is recorded only; this task did not install it live.

## Publication fence

Source/tests were committed and pushed first as implementation commit:

```text
a924157ecdedef1d4f166d5762529b0d59536fc9
```

This report is the only file in the following report-only commit, to be verified remotely before stopping:

```text
REPORT_COMMIT_PENDING
```

The successor gate is now the independent acceptance of:

```text
PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED
```

No semantic retest or live install-over is authorized by this report alone.
