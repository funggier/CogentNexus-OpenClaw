# CNX-20260827-104 — Add Redacted Dashboard Staging Observability

## Result

`PASS_REDACTED_DASHBOARD_STAGING_OBSERVABILITY_READY_FOR_LIVE_INSTALL`

Task 104 rework completed within the approved source/test/build/package observability scope. The callback evaluation order was restored to the predecessor's short-circuit behavior, unexpected callback kinds are reduced to safe categories, and redacted diagnostics remain covered by focused tests. No live install, semantic Send, provider call, live SQLite/config/runtime mutation, restart, credential access, or delivery-logic repair was performed.

Stop now for independent review. A separately gated install-over task is required before any live diagnostic retest.

## Authorization and preflight

- Coordination branch: `agent/v0.9.3-recovery-reality-tests`.
- Fresh synchronization from `origin/agent/v0.9.3-recovery-reality-tests` reached coordination HEAD `524e171` before source work.
- Active gate: `READY_FOR_HERMES`; Task ID `CNX-20260827-104`.
- Review disposition: `REWORK_BEHAVIOR_NEUTRALITY_AND_OBSERVABILITY_COVERAGE`.
- Accepted live baseline was not touched: installed source `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`, fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`, expected MANAGED generation 24.
- Work was performed in the isolated coordination clone under `%LOCALAPPDATA%\\Temp`; no live OpenClaw state was used.

## TDD evidence

### RED

After adding the two rework-focused tests, before changing production code:

```text
npm test -- --run src/v091-dashboard-verified-delivery.test.ts
```

Observed RED:

- 10 tests collected;
- 8 passed, 2 failed;
- both failures were the intended rework assertions: `getQueuedCounts` was evaluated for a non-final/owned-sensitive path, and an unexpected long `info.kind` was not safely bounded before logging.

No syntax or setup failure caused the RED result.

### GREEN

After the minimum source correction:

```text
npm test -- --run src/v091-dashboard-verified-delivery.test.ts
```

Observed GREEN:

- 1 test file passed;
- 10 tests passed;
- exit code 0.

The focused suite covers registration/capability diagnostics, deterministic filter reasons, successful and non-staged staging, exception telemetry, duplicate registration, secret-leak assertions, predecessor guard order, already-owned behavior, and bounded unexpected callback kinds.

## Implementation

Implementation commit:

`fca61704174a7b7bb46598a86992900fb3c83cce`

Parent implementation/rework base:

`524e171`

Changed files:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`

The source change is limited to the approved verified-delivery observability boundary:

1. `info.kind !== "final"` is checked before `getQueuedCounts()` and downstream work.
2. `owned` is checked before `getQueuedCounts()` and downstream work.
3. Non-final kinds are logged as the bounded categories `final`, `delta`, `other`, or `unknown`; unexpected long/synthetic strings are never logged raw.
4. Exception telemetry is categorical (`sqlite`, `error`, or `unknown`) and never forwards error codes/messages.
5. The already-owned second callback returns its payload unchanged, emits `already-owned`, and does not create a duplicate durable row.

No transaction behavior was altered. Transaction begin/commit phase telemetry was not added because the staging function is a synchronous transaction boundary with several existing early commits and adding callbacks around individual transaction statements would require changing that behavior or introducing a new diagnostics interface. Existing `stage-attempt`, `stage-staged`, `stage-not-staged`, and `stage-exception` observations distinguish the externally relevant stage outcome without modifying transaction semantics.

## Diagnostic taxonomy

Stable prefix:

`CogentNexus-OpenClaw delivery-observe`

Events and safe fields:

| Boundary | Event/reason | Safe fields |
| --- | --- | --- |
| runtime hook registration | `hook-registered` | registration count, capability boolean |
| handler entry | `handler-entry` | run-ID presence booleans, capability booleans, truncated SHA-256 digest |
| handler capability skip | `handler-skip` | `missing-run-correlation`, `missing-dispatcher`, `missing-append-before-deliver` |
| callback registration | `callback-registered` | callback capability boolean |
| callback entry | `callback-entry` | bounded kind, final count only after predecessor guards, text/media/owned booleans, truncated digest |
| filter decision | `filter-skip` | `not-final`, `already-owned`, `empty-text`, `media-present`, `final-count-not-one` |
| stage start | `stage-attempt` | truncated digest and text-present boolean |
| non-staged return | `stage-not-staged` | existing stage reason enum |
| staged return | `stage-staged` | truncated digest and owner generation |
| staging exception | `stage-exception` | categorical exception class and normalized category |

Raw prompt, response, run/session identifiers, nonce content, idempotency keys, markers, credentials, tokens, passwords, provider payloads, paths, and raw exception messages are not emitted by the new diagnostics.

## Regression and package evidence

Focused:

```text
npm test -- --run src/v091-dashboard-verified-delivery.test.ts
```

Result: `10 passed (10)`, exit code 0.

Full plugin suite:

```text
npm test -- --run
```

Result: `49 passed (49) test files`, `265 passed (265) tests`, exit code 0.

Build/package validation:

```text
npm run plugin:validate
```

Result:

- TypeScript build passed;
- mixed-plugin artifact verification passed (`45` config properties, `5` tools);
- ticket DB bootstrap passed (`9` required tables plus v0.9.5 registration fence);
- package contents verification passed;
- packed file count: `176`.

The repository Python regression attempt was not runnable because the Hermes Python environment has no `pytest` module. No installer or Python implementation files were changed; package validation and the complete plugin test suite passed.

## Production-shaped release-path harness

A disposable external Node harness loaded the rebuilt `dist/v091-release-entry.js`, created a temporary MANAGED Host controller at generation 24, initialized temporary SQLite state, registered the real release entry, captured registered hooks, invoked the real release-registered `reply_dispatch` hooks, and drove a modeled successful final text-only Dashboard callback.

Harness result:

```json
{
  "replyHookCount": 3,
  "beforeDeliverCount": 2,
  "deliveryCount": 1,
  "hasStageAttempt": true,
  "hasStageStaged": true,
  "leaks": [],
  "returnedMarkerPayload": true
}
```

Exit code was 0. The harness used only temporary state and did not access or mutate live SQLite/runtime state.

## Fingerprint and package safety

The accepted Task-094/095 payload-v2 helper was run directly:

```text
python skills/cogentnexus-openclaw/scripts/namespace_ownership.py plugin-fingerprint --plugin-root plugins/cogentnexus-openclaw --version 0.9.3
```

Final rebuilt payload:

- version: `0.9.3`;
- installable file count: `176`;
- payload-v2 fingerprint: `92175edc4d5b52782bfaf40ec8ee6180293342e6c651657dece2a9598e92f2cb`;
- `package.json.files` and package contents: PASS;
- reparse/path safety through the accepted fingerprint helper: PASS.

This fingerprint is not the currently installed live fingerprint. It was not installed.

## Secret-safety and semantic-equivalence evidence

Focused tests and the release-path harness supplied synthetic response text, prompt text, run IDs, session values, media values, and exception conditions. Captured diagnostics contained none of the raw synthetic secrets. The bounded-kind test supplied a 5,000-character synthetic kind and verified the logged value was `other`, not the input string.

The predecessor-sensitive test verified:

- non-final callback: `getQueuedCounts` call count remains zero and payload is returned unchanged;
- first final callback: queued count is evaluated once and staging proceeds;
- already-owned second final callback: queued count is not re-evaluated, `already-owned` is emitted, and the payload is returned unchanged;
- existing staging semantics remain one durable row.

## Zero-live-mutation proof

Task-104 rework mutation counts:

- Dashboard semantic Send: `0`;
- provider/model call: `0`;
- live SQLite/config/runtime mutation: `0`;
- live plugin install/install-over/uninstall/reset/cleanup: `0`;
- Gateway/Supervisor restart or reboot: `0`;
- credential/token/password access or re-entry: `0`;
- session cleanup/normalization: `0`;
- source changes outside the isolated coordination clone: `0`;
- semantic delivery repair outside observability: `0`.

## Exact successor recommendation

1. Independent ChatGPT review of implementation commit `fca61704174a7b7bb46598a86992900fb3c83cce` and this report.
2. If independently accepted, create one separately gated bounded install-over task using fingerprint `92175edc4d5b52782bfaf40ec8ee6180293342e6c651657dece2a9598e92f2cb`.
3. After install acceptance and fresh live-state verification, perform one operator-assisted single semantic Dashboard diagnostic retest only when explicitly authorized by the successor task.

## Publication fence

This report is to be the only file added after implementation commit `fca61704174a7b7bb46598a86992900fb3c83cce`. The final implementation-to-report delta must be report-only. Verify repository status and ancestry, push the report to `agent/v0.9.3-recovery-reality-tests`, then stop for independent review.
