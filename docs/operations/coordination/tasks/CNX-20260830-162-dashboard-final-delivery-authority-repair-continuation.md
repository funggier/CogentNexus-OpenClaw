# CNX-20260830-162 — Dashboard Final-Delivery Authority Repair Continuation

Status: `IN_PROGRESS_CHATGPT`

Execution mode: `REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_CONTINUATION`

Current authorization: `CNX-20260830-162_REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_CONTINUATION`

Task ID: `CNX-20260830-162`

Updated: 2026-08-30 ICT

Owner / coordinator / executor / reviewer: ChatGPT

Review type at completion: self-review / non-independent

## Trigger

Task 161 remains unresolved and the active ChatGPT context reached its practical continuation boundary before a valid RED regression had been committed.

This task exists to preserve the proven Task-160/161 causal investigation and continue the same repository repair without losing evidence, repeating unsafe semantic actions, or weakening TDD.

Predecessor task:

`docs/operations/coordination/tasks/CNX-20260830-161-dashboard-live-durable-delivery-path-repair.md`

Task-160 live failure report:

`docs/operations/coordination/reports/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`

Task-160 review:

`docs/operations/coordination/reviews/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance-review.md`

## Repository checkpoint at rollover

Authoritative branch at task creation:

`agent/v0.9.3-full-stabilization`

Exact predecessor HEAD inspected immediately before this task was opened:

`d917ffd90e7a796f36b935ea15afdcfe99e71ad6`

No Task-161 RED test commit and no Task-161 production repair commit had been made at that checkpoint.

GitHub must still be re-read before every write; this SHA is a handoff checkpoint, not permission to assume future state.

## Proven causal findings carried forward

### 1. Task-160 production failure is after inference, before durable authority

The single authorized Dashboard semantic Send established that:

- the model call completed;
- assistant reply text existed (`Probe reply via fallback bridge`);
- `response_ready` was committed;
- `reply_dispatch` was observed;
- the dispatch surface exposed `hasAppendBeforeDeliver=false`;
- CogentNexus armed the fallback;
- no terminal persistence callback followed;
- `missing-append-before-deliver` was recorded;
- no authoritative assistant durable-delivery row was committed;
- `/send` failed closed with HTTP 500;
- no semantic retry occurred because duplicate/no-regeneration safety took precedence.

Therefore this is not an inference failure. The unresolved boundary is exact assistant result -> authoritative durable persistence -> verified delivery success.

### 2. The accepted Task-154 fallback depended on a callback that is not a production contract

Current CogentNexus code in:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

handles `reply_dispatch` by using `appendBeforeDeliver` when available. When it is absent, it arms a fallback and waits for a later public payload callback such as `reply_payload_sending`.

Task 160 demonstrated that the real Dashboard/webchat path did not provide the assumed second terminal callback.

The repair must not merely wait for another optional callback or treat transport text as a durable receipt.

### 3. Exact installed OpenClaw control flow explains why `reply_dispatch` cannot own final persistence

The installed OpenClaw provenance used by the live acceptance was `v2026.7.1-2`, commit:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

Source inspection of that exact upstream commit established:

- `dispatchReplyFromConfig()` invokes the `reply_dispatch` plugin hook **before normal model dispatch**;
- the hook receives `dispatchHookDispatcher`, produced by `createAbortAwareDispatcher()`;
- `createAbortAwareDispatcher()` exposes send/wait/count/markComplete operations but intentionally does **not** expose `appendBeforeDeliver`;
- when the hook does not handle the turn, OpenClaw continues into normal model dispatch;
- the eventual final reply is queued through the original dispatcher, not the pre-dispatch wrapper received by the plugin hook.

Consequences:

- `hasAppendBeforeDeliver=false` on the live `reply_dispatch` path is consistent with upstream source, not an incidental runtime anomaly;
- mutating or retaining the dispatcher passed to `reply_dispatch` cannot intercept the normal final answer;
- Task-154 synthetic behavior that later supplied an append-capable callback represented a possible test sequence, not a reliable OpenClaw Dashboard/webchat contract.

### 4. `before_agent_finalize` is a real awaited post-model/pre-terminal boundary, but is not yet proven sufficient

Exact upstream source shows the embedded agent runner calls the awaited `before_agent_finalize` hook from `onBeforeTerminalDelivery` only after a visible terminal assistant candidate exists.

Its event includes at least:

- `runId`;
- `sessionId`;
- `sessionKey` when available;
- `provider` / `model`;
- `transcriptPath` when available;
- `lastAssistantMessage` containing the resolved terminal assistant text;
- projected messages.

This makes it materially stronger than pre-model `reply_dispatch` for capturing the exact model result.

However, **do not implement persistence from this hook alone yet**. Existing CogentNexus delivery recovery in `skills/cogentnexus-openclaw/scripts/host_delivery.py` uses a marker/idempotency observation before `chat.inject`. If native Dashboard delivery persists the same assistant text without that marker while a separately queued CogentNexus recovery row remains pending, recovery could inject a duplicate assistant message.

The next repair must therefore prove how native Dashboard transcript persistence and CogentNexus durable-delivery settlement can share one exactly-once authority.

### 5. Upstream Gateway webchat already contains authoritative transcript primitives

Inspection of exact upstream `src/gateway/server-methods/chat.ts` shows the Dashboard/webchat gateway owns transcript helpers including assistant transcript append/search/idempotency logic and creates the reply dispatcher used by `chat.send`.

This file is the next source/control-flow target. Continue tracing:

1. where the webchat `createReplyDispatcher(...)` deliver callback broadcasts the final payload;
2. where/when the assistant transcript row is appended relative to broadcast and `chat.send` completion;
3. what idempotency key or message identity is available;
4. whether any public plugin hook/API/runtime surface exposes that authoritative result without patching OpenClaw;
5. whether CogentNexus can verify native persistence and settle its durable row without issuing a second side effect.

Do not patch OpenClaw source.

## Objective

Continue Task-161 root-cause work from the exact upstream Dashboard/webchat final-delivery path, identify a plugin-accessible authoritative exactly-once persistence/verification boundary, reproduce the real defect with a valid RED regression, then implement the smallest CogentNexus-OpenClaw repair and prove GREEN.

## Required next investigation

Before any production change:

1. re-read current branch HEAD and coordination state;
2. trace exact `chat.send` webchat dispatcher creation/delivery/transcript-settlement flow at OpenClaw commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`;
3. map that flow against CogentNexus `v091-dashboard-verified-delivery.ts` and `host_delivery.py`;
4. determine which event/primitive can establish all of:
   - exact assistant result identity;
   - authoritative transcript persistence;
   - idempotent duplicate prevention;
   - durable CogentNexus settlement;
   - fail-closed behavior when authority cannot be verified;
5. explicitly reject any candidate that would permit native-send + recovery-inject duplication.

## TDD contract

### RED

Only after the real production boundary is demonstrated, add the smallest regression that faithfully reproduces it.

The RED must cover the production-relevant case, including:

- no reliance on a second `reply_payload_sending` callback;
- no append-capable dispatcher being available from pre-model `reply_dispatch`;
- exact assistant result becoming available on the real post-model path;
- no successful HTTP/terminal delivery result until authoritative persistence is verified;
- no duplicate assistant row if native persistence has already occurred.

Commit the test-only RED state first and record exact commit / Actions run / job / expected failing assertion.

### Minimal repair

After RED is observed, change only the CogentNexus-OpenClaw production surface required to make that regression GREEN.

The repair must preserve:

- Task-155 duplicate safety;
- one authoritative assistant result per run/generation;
- no re-inference after an assistant result already exists;
- no duplicate native-send + recovery-inject side effects;
- fail-closed behavior when persistence cannot be proven;
- Ticket/workflow/delivery ownership boundaries;
- upstream OpenClaw as read-only external code.

### GREEN

At the final production repair SHA, run the Task-161 validation contract at minimum:

- repository Validate workflow / relevant full matrix;
- Windows PowerShell 5.1 Acceptance Smoke;
- Windows Installer Pack Smoke;
- full CogentNexus-OpenClaw plugin tests;
- Task-155 duplicate public-hook regression;
- the new Task-162 production-faithful regression;
- dependency audit / existing package validation required by the repository.

Any production/source change requires fresh validation after the final production SHA.

## Repository-only authorization

Authorized:

- GitHub source/history inspection;
- exact installed-version upstream OpenClaw source read-only inspection;
- repository regression tests;
- minimal CogentNexus-OpenClaw production repair;
- coordination/report/review documentation;
- CI/workflow execution and log inspection.

## Hard fence

Task 162 does **not** authorize:

- any Dashboard semantic Send;
- Dashboard click/focus/type/paste for semantic testing;
- any semantic user message through another live surface;
- real Windows install-over/uninstall/reinstall/reset;
- Gateway/Ollama/Supervisor live restart for this repository investigation;
- manual Ticket/workflow/result/outbox/delivery/database mutation;
- arbitrary live-state deletion;
- OpenClaw source patch;
- dependency upgrade;
- unrelated product behavior change;
- release/tag/package publication/promotion;
- merge to default/release branch;
- force push.

## Acceptance criteria

Task 162 may be accepted only when:

1. the exact Dashboard/webchat final-delivery + transcript-persistence order is source-evidenced;
2. the chosen CogentNexus authority boundary is proven to prevent native/recovery duplication;
3. a valid production-faithful RED regression fails before production change;
4. a minimal repair makes the regression GREEN;
5. Task-155 duplicate safety remains GREEN;
6. relevant repository/plugin/Windows validation is GREEN on the exact repair SHA;
7. no prohibited live action occurred;
8. a durable Task-162 report and explicit ChatGPT self-review are published.

## Successor gate

Even Task-162 ACCEPT does **not** authorize another Dashboard semantic Send.

After repository acceptance, the next live step remains a separate repaired-candidate Windows install-over + provenance/health acceptance task. Only after that checkpoint is reviewed ACCEPT may a new exactly-one-Send Dashboard reacceptance task be opened.
