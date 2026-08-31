# CNX-20260830-154 — Dashboard Durable Capture Public-Hook Repair

## Verdict

`PASS`

Task 154 completed the authorized offline RED → minimal GREEN → full verification repair. No live Windows/runtime mutation and no Dashboard semantic Send occurred.

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260830-154`
- Execution mode: `OFFLINE_REPOSITORY_TDD_DASHBOARD_DURABLE_CAPTURE_PUBLIC_HOOK_REPAIR`
- Accepted predecessor evidence: Task 153, independent disposition `ACCEPT`
- Exact OpenClaw runtime/source under compatibility inspection: `v2026.7.1-2` / `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

The task fence prohibited Dashboard interaction, semantic transport, live Windows/runtime mutation, lifecycle/install/reset/uninstall/reinstall actions, manual durable-state mutation, OpenClaw source patching, dependency upgrades, merge/tag/release, and force push. Those fences were preserved.

## Accepted root cause carried from Task 153

Task 153 established the first production failure boundary from Task 152:

1. the CogentNexus `reply_dispatch` handler entered;
2. event run correlation was present;
3. a dispatcher was present;
4. `appendBeforeDeliver` was absent;
5. the handler skipped with `missing-append-before-deliver`;
6. no callback registration/invocation or durable staging followed in the bounded observation window.

Therefore the Task-152 failure was before durable staging, not a SQLite staging failure, final-payload filter failure, or Task-138 final-count regression.

## Exact upstream compatibility proof

Independent inspection of exact OpenClaw commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` confirmed the repair contract before production changes were accepted.

### 1. `appendBeforeDeliver` is optional

`src/auto-reply/reply/reply-dispatcher.types.ts` declares:

- `appendBeforeDeliver?: (hook: ReplyDispatchBeforeDeliver) => void`

CogentNexus therefore cannot require this optional capability to be present on every dispatcher-shaped object exposed to plugins.

### 2. `reply_dispatch` receives a wrapper that omits the optional append capability

Exact `src/auto-reply/reply/dispatch-from-config.ts` constructs the dispatcher exposed through the dispatch hook by forwarding:

- `sendToolResult`
- `sendBlockReply`
- `sendFinalReply`
- `waitForIdle`
- `getQueuedCounts`
- failed/outcome count access
- `markComplete`

but does not forward `appendBeforeDeliver`.

This exactly explains the Task-153 runtime observation without requiring a plugin-registration or SQLite hypothesis.

### 3. OpenClaw owns a public pre-delivery hook on the original dispatcher

Exact `src/auto-reply/dispatch.ts` installs `reply_payload_sending` on the original dispatcher through `installReplyPayloadSendingBeforeDeliver(...)` before `dispatchReplyFromConfig(...)` runs.

Its before-delivery function calls `runReplyPayloadSendingHook(...)` with:

- the actual outbound payload;
- delivery `kind`;
- channel/session correlation;
- the turn `runId` captured from `onAgentRunStart`.

### 4. Hook-returned payload is the payload delivered natively

Exact `src/auto-reply/reply/reply-dispatcher.ts` executes the composed `beforeDeliver` function inside the serialized send chain. The returned payload becomes `deliverPayload`, preserves reply metadata, and is then passed to `options.deliver(deliverPayload, dispatchInfo)`.

Therefore `reply_payload_sending` is a genuine pre-native-delivery rewrite boundary, not a post-delivery observation hook.

## TDD — genuine RED

### Test-only RED commits

- `129b8d20dc97d4182689a1fc968bb86149202617` — `test: reproduce Dashboard capture without appendBeforeDeliver`
- `a9c7b069e03498abf71a1ae9253c79e59da10939` — `test: satisfy namespace gate for Task 154 RED`

The focused regression created a production-shaped Dashboard Direct turn where:

- session authority was active;
- the Ticket was accepted/routed with exact run correlation;
- `reply_dispatch` received a dispatcher with no `appendBeforeDeliver` but with send/idle/outcome methods;
- the same run later invoked `reply_payload_sending` with one text-only `kind=final` payload;
- expected behavior required a durable direct-result row and marker-bearing returned payload before native delivery.

### RED evidence

Exact RED SHA: `a9c7b069e03498abf71a1ae9253c79e59da10939`

- GitHub Actions Validate: `33290691842`
- Ubuntu/Python 3.11 job: `99201678165`

The repository's existing `v091-dashboard-verified-delivery.test.ts` suite passed `11/11` while the new Task-154 regression failed exactly once:

`src/v154-dashboard-public-hook-fallback.test.ts`

Failure:

`expected undefined to be type of 'function'`

at the assertion requiring the registered `reply_payload_sending` handler.

This is the intended RED: the predecessor implementation registered only the append-dependent `reply_dispatch` path and had no public-hook fallback.

## Minimal GREEN production repair

### Production implementation commit

`e0182d89c91647e7070c2b95fc0b9b0fffc0378a` — `fix: capture Dashboard final via public pre-delivery hook`

Production file changed:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

The repair is intentionally narrow:

1. The existing `reply_dispatch` + `appendBeforeDeliver` path remains unchanged when that capability exists.
2. When `reply_dispatch` lacks `appendBeforeDeliver`, the handler still records the existing skip diagnostic, then arms a run-scoped fallback only if the correlated Ticket is a Dashboard Direct Ticket.
3. The plugin registers `reply_payload_sending` and accepts only a matching armed run.
4. The fallback accepts only one text-only `kind=final` payload and preserves the Task-138 `finalCount > 1` rejection rule.
5. `stageDashboardDirectResult(...)` remains the durable authority for generation-bound idempotency, one-row ownership, changed-text fail-closed behavior, response-ready state, payload hashing, and marker generation.
6. On successful staging, the hook returns the original payload with only `text` rewritten to the exact durable marker-bearing `nativeText`; OpenClaw then sends that returned payload through native delivery.
7. The fallback uses the same dispatcher idle/failed/cancelled outcome counters to settle the durable row after native delivery. Successful native settlement calls `settleDashboardNativeDelivery(...)`; failure/cancellation preserves the durable row and kicks the existing host-delivery recovery path instead of regenerating model output.
8. Run correlation remains privacy-bounded through the existing digest telemetry; raw prompt/response/run/session identifiers are not added to logs.

No model inference, resend, alternate semantic transport, or post-delivery reconstruction was introduced.

### Correlation-digest preservation follow-up

`4c5d2d3d0b5d49f47a31cbf49ee45d2b9e1a7c77` — `fix: preserve delivery correlation digest separator`

The first production edit unintentionally changed the predecessor digest separator representation while editing the same function. This follow-up restored the original separator representation and changed no delivery semantics.

For Task-154 production provenance, the accepted production implementation state is therefore the source tree at `4c5d2d3d0b5d49f47a31cbf49ee45d2b9e1a7c77`.

## Verification stabilization after production GREEN

The first full Validate run on `4c5d2d3d0b5d49f47a31cbf49ee45d2b9e1a7c77` exposed test-harness issues caused by registering a second hook:

- legacy test mocks stored every `api.on(...)` handler without checking the hook name, so the newly registered `reply_payload_sending` handler overwrote their intended `reply_dispatch` handler;
- the new focused regression allowed the asynchronous native-settlement waiter to survive teardown, so the temporary SQLite database could be removed before the waiter settled.

These failures did not establish a new production defect. The Task-154 regression itself already passed on the production repair, while the affected legacy mocks no longer modeled named hook registration accurately.

A test-only verification descendant fixed those harness/synchronization defects:

`74732d847add15295265afc472ef3455ce89f3f3` — `test: stabilize Task 154 public-hook coverage`

Changes were limited to tests:

- legacy mocks now retain handlers only for `name === "reply_dispatch"` where the test is specifically exercising that hook;
- the Task-154 regression now holds `waitForIdle()` on a controlled promise, verifies exactly one pending durable row, invokes the same final a second time and proves no duplicate row is staged, releases native idle deterministically, waits one event-loop turn, and verifies the durable row becomes `delivered` and the Ticket becomes `completed` before teardown.

No production code changed in `74732d847add15295265afc472ef3455ce89f3f3`.

## Final exact-SHA verification

Verification SHA:

`74732d847add15295265afc472ef3455ce89f3f3`

Exact GitHub Actions:

| Workflow | Run | Result |
|---|---:|---|
| Validate | `33291503163` | `success` |
| PS5.1 Acceptance Smoke | `33291503150` | `success` |
| Windows Installer Pack Smoke | `33291503165` | `success` |

The Validate matrix completed successfully across:

- Ubuntu Python 3.11 and 3.14;
- macOS Python 3.11 and 3.14;
- Windows Python 3.11 and 3.14;
- package dry-run.

Relevant gates included repository/namespace validation, Python tests/self-tests, `npm ci`, full plugin `npm test`, evaluation, `npm audit --omit=dev`, plugin validation, Windows PowerShell checks, and package provenance/dry-run validation as applicable to each matrix job.

## Acceptance-contract review

Task-154 requirements are satisfied offline:

- production-shaped no-append RED reproduced: **PASS**
- genuine RED before production repair: **PASS**
- public pre-delivery fallback bound to exact run: **PASS**
- existing append-capable path preserved: **PASS**
- one durable row per Ticket generation: **PASS**
- duplicate same-final staging forbidden: **PASS**
- changed-text fail-closed authority preserved in `stageDashboardDirectResult`: **PASS**
- marker-bearing native payload returned before delivery: **PASS**
- no duplicate model inference/regeneration: **PASS**
- dispatcher native outcome settlement preserved: **PASS**
- recovery path retains durable payload on delivery failure/cancellation: **PASS**
- privacy-bounded telemetry preserved: **PASS**
- exact-SHA full CI/smoke verification: **PASS**

## Files / commits

Production:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `e0182d89c91647e7070c2b95fc0b9b0fffc0378a`
- `4c5d2d3d0b5d49f47a31cbf49ee45d2b9e1a7c77`

Regression/verification:

- `plugins/cogentnexus-openclaw/src/v154-dashboard-public-hook-fallback.test.ts`
- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`
- RED: `129b8d20dc97d4182689a1fc968bb86149202617`, `a9c7b069e03498abf71a1ae9253c79e59da10939`
- final test-only verification descendant: `74732d847add15295265afc472ef3455ce89f3f3`

## Safety / side effects

During Task 154:

- Dashboard semantic Sends: `0`
- live Windows runtime mutations: `0`
- install/reset/uninstall/reinstall invocations: `0`
- manual Ticket/outbox/delivery/database mutations: `0`
- OpenClaw source patches: `0`
- dependency upgrades: `0`
- merge/tag/release operations: `0`
- force pushes: `0`

## Conclusion

`PASS`

The Task-153 production boundary now has a tested offline repair using OpenClaw's exact public pre-delivery hook contract. The repair durably captures and marks the final Dashboard payload before OpenClaw native delivery even when the `reply_dispatch` wrapper lacks `appendBeforeDeliver`, while preserving the predecessor append path and duplicate/recovery safety.

Phase P is **not** declared accepted by this offline task. Publish this report and stop for independent review. A repaired Windows install-over/health proof and any later single-Send Dashboard reacceptance require separate coordination authority after review.
