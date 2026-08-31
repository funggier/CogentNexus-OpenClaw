# CNX-20260830-163 — Hermes Dashboard Final-Delivery Authority Repair Review

Review disposition: `NOT_ACCEPTED_CONTINUE_TASK_162`

Reviewer: ChatGPT

Review type: coordinator / final review of delegated Hermes Task 163

Reviewed branch: `agent/v0.9.3-full-stabilization`

Hermes report commit / reviewed HEAD: `105db4367f259fcf7de5f2ec5b01c86af1bd6dfd`

Exact upstream OpenClaw target: `v2026.7.1-2`, commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

## Decision

The Hermes `BLOCKED` disposition is **not accepted** as the authority-boundary conclusion.

Hermes was correct to stop before creating a RED regression or modifying production code when it believed the required boundary had not been proven. Its hard-fence behavior was therefore conservative and valid.

However, the source investigation omitted a plugin-accessible post-persistence primitive that exists in the exact installed OpenClaw target:

`api.runtime.events.onSessionTranscriptUpdate(...)`

That omission invalidates the report's central claim that the exact OpenClaw version exposes no public/plugin-accessible post-native-transcript persistence boundary.

Task 163 therefore ends as a useful but incomplete delegated investigation. Parent Task 162 must resume under ChatGPT authority and prove the newly identified boundary with the mandatory test-only RED before any production repair.

## Critical review finding

Hermes states:

> "The source does not expose a plugin callback/API that returns the exact native persisted assistant row, its message ID, or an atomic commit token after the normal agent-run append."

That statement is contradicted by the exact upstream source.

### 1. `before_message_write` is installed on the runtime SessionManager persistence path

Exact upstream:

`src/agents/session-tool-result-guard-wrapper.ts`

`guardSessionManager(...)` obtains the global plugin hook runner, invokes `before_message_write`, accepts a replacement `message`, and passes that function as `beforeMessageWriteHook` to `installSessionToolResultGuard(...)`.

This is not merely a declared hook type. It is wired into the SessionManager write guard used by embedded-agent transcript persistence.

### 2. Assistant messages pass through that hook before the native append

Exact upstream:

`src/agents/session-tool-result-guard.ts`

For a non-tool-result assistant message, the guarded append path performs:

1. persistence transforms;
2. `applyBeforeWriteHook(...)`;
3. obtains `finalMessage`;
4. calls `appendMessageAndCacheTranscriptSeq(finalMessage, ...)`.

Therefore a plugin can bind durable marker metadata/text to the exact assistant message **before** the native SessionManager append without owning the Dashboard transport dispatcher.

### 3. The native append occurs before the transcript-update event

The same exact file defines `appendMessageAndCacheTranscriptSeq(...)` such that `originalAppend(...)` executes first.

After the guarded append returns `entryId`, `sessionFile`, and `messageSeq`, OpenClaw calls:

`emitSessionTranscriptUpdate(...)`

with the persisted `finalMessage`, `messageId`, `messageSeq`, `sessionFile`, `sessionKey`, and `agentId`.

The order is therefore source-evidenced as:

`before_message_write -> originalAppend(native transcript persistence) -> emitSessionTranscriptUpdate`

This is materially different from `reply_dispatch`, `reply_payload_sending`, and `before_agent_finalize`: it provides an observation boundary after the SessionManager append has completed.

### 4. The transcript update is explicitly exposed through `PluginRuntime.events`

Exact upstream:

`src/plugins/runtime/runtime-events.ts`

`createRuntimeEvents()` returns:

- `onAgentEvent`
- `onSessionTranscriptUpdate`

Exact upstream:

`src/plugins/runtime/types-core.ts`

`PluginRuntimeCore.events` explicitly includes:

`onSessionTranscriptUpdate: typeof import("../../sessions/transcript-events.js").onSessionTranscriptUpdate`

CogentNexus-OpenClaw already uses `api.runtime` elsewhere in its plugin, so this is a plugin-accessible runtime surface in the exact installed source target rather than a private core-only helper.

## Why the original BLOCKED argument no longer holds

Hermes correctly rejected pre-persistence candidates such as:

- pre-model `reply_dispatch`;
- `reply_payload_sending`;
- `before_agent_finalize` by itself;
- `chat.history` read-then-inject;
- `chat.inject` as a receipt for an unrelated native append.

Those rejections remain useful.

The missing primitive changes the state space because OpenClaw itself provides an in-process event emitted after the runtime transcript append and includes the persisted assistant message identity (`messageId`) plus transcript/session correlation fields.

The repair therefore no longer needs to infer successful native persistence from transport success or perform a race-prone external history read merely to learn whether the SessionManager append happened.

## Candidate authority boundary for Task 162

The following composite boundary is now source-supported and must be tested before production use:

1. `before_agent_run` / existing run-session ownership binds `runId` to the Dashboard session and Ticket generation.
2. `before_agent_finalize` provides the exact terminal assistant candidate and run/session correlation without triggering a second inference.
3. `before_message_write` on the matching native assistant write stages/binds the durable CogentNexus direct-result identity and adds the stable CogentNexus delivery marker to the message that OpenClaw is about to persist.
4. OpenClaw performs `originalAppend(...)` through its native SessionManager.
5. `api.runtime.events.onSessionTranscriptUpdate(...)` observes the marker-bearing assistant row **after** that append and supplies its native `messageId` / session/transcript identity.
6. Only that post-append observation may settle the CogentNexus direct-delivery row as natively persisted.
7. Recovery must use the same marker/idempotency identity. If the native marker exists, it settles/consumes the durable row and must not `chat.inject`; if the native marker does not exist after ownership has safely transferred to recovery, exactly one recovery injection is permitted.

This candidate does **not** yet authorize production source changes. The exact crash/race handoff between native-write ownership and external recovery still requires a production-faithful RED regression and explicit proof that recovery cannot inject while a native append remains an active owner.

## Mandatory RED scope on resumed Task 162

Before any production change, the regression must reproduce the exact installed-version contract and fail on current CogentNexus code.

At minimum it must prove:

1. pre-model `reply_dispatch` has no append-capable dispatcher;
2. no second `reply_payload_sending` callback is needed;
3. exact post-model assistant result/run/session correlation exists;
4. `before_message_write` acts on the native assistant message that is actually persisted;
5. transcript-update observation occurs only after the simulated native append and carries the same marker-bearing assistant plus native message identity;
6. CogentNexus success is withheld until that post-persistence observation;
7. once native persistence is observed, recovery injection is suppressed;
8. if a durable result exists but native persistence is not observed, recovery cannot race an active native-write owner;
9. no second inference occurs after the assistant result already exists;
10. Task-155 duplicate/public-hook behavior remains protected.

Only after that test-only RED is committed and its expected failure is recorded may the production repair proceed.

## Hermes report quality notes

Positive findings retained:

- correct trace that `reply_dispatch` receives the abort-aware wrapper without `appendBeforeDeliver`;
- correct rejection of `reply_payload_sending` as a native persistence receipt;
- correct separation of Gateway live payload delivery from embedded runtime transcript ownership;
- correct refusal to make speculative production changes;
- no prohibited live semantic or Windows/runtime action was reported.

Required correction:

- the report's `Authority and fresh state` section contains a malformed/truncated rendering of the exact upstream OpenClaw commit. The canonical exact target remains `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`.

## Review result

Task 163 report: `NOT_ACCEPTED`

Hermes production changes: none — correct under its investigated premise.

Hermes hard-fence compliance: accepted based on reported/repository evidence.

Hermes `BLOCKED` authority conclusion: rejected as incomplete.

Parent Task 162: `CONTINUE`

Next action: return execution authority to ChatGPT on Task 162 and create the mandatory production-faithful test-only RED around `before_message_write -> native append -> runtime.events.onSessionTranscriptUpdate`, including native/recovery ownership race protection.

No Dashboard Send, live Windows lifecycle mutation, OpenClaw patch, dependency upgrade, release, or promotion is authorized by this review.
