# CNX-20260830-163 — Hermes Dashboard Final-Delivery Authority Repair Attempt

## Disposition

`BLOCKED`

Task 163 is blocked at the mandatory source-trace / authority-boundary gate. Exact upstream OpenClaw source proves the model-result and native Dashboard transcript-delivery paths, but no plugin-accessible public boundary was found that can atomically establish native transcript persistence, settle the CogentNexus durable delivery row, and prevent native-send plus recovery-inject duplication without patching OpenClaw.

Because the required safe authority boundary was not proven, the TDD contract does not authorize a RED test or a production source change. No RED commit, production repair, or live acceptance was performed.

## Authority and fresh state

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Active task: `CNX-20260830-163`
- Fresh authoritative starting HEAD: `3f29fe7d77d89c4184fa02450ecec025417edcb5`
- Fresh isolated checkout: `C:\Users\CDQ-P\AppData\Local\Temp\cnx163-20260830T20260830T144101Z\source`
- Checkout state before report: clean and equal to remote HEAD
- Coordination files re-read from GitHub immediately before report write; local and remote `ACTIVE.md` / `STATUS.md` matched
- Required report was absent before the report write
- Exact upstream read-only target: OpenClaw `v2026.7.1-2`, commit `0790d9f593ad30c940ed93b5872a8cf8c`
- Exact upstream checkout: `C:\Users\CDQ-P\AppData\Local\Temp\cnx163-20260830T20260830T144101Z\upstream-openclaw`

## Exact upstream source trace

### Dashboard dispatcher creation and native delivery

At upstream `src/gateway/server-methods/chat.ts:4724-4751`, `chat.send` creates `createReplyDispatcher(...)`. Its `deliver` callback records `block`/`final` payloads in the local `deliveredReplies` array and runs the media-transcript helper; it does not itself persist the normal agent-run assistant transcript row.

The normal final content is processed only after dispatch completes. At `chat.ts:4920-4959`, post-dispatch code separates agent-run and non-agent ownership. The source explicitly states that agent runs persist model-visible turns through the OpenClaw runtime SessionManager and that this dispatcher owns live delivery payloads only; blindly mirroring agent-run finals would duplicate normal embedded-agent assistant turns.

For non-agent replies, `chat.ts:5353-5386` calls `appendAssistantTranscriptMessage(...)` and uses the returned persisted message to build the final broadcast. If append fails, `chat.ts:5387-5414` constructs an in-memory fallback message instead of proving persistence. The final UI event is broadcast at `chat.ts:5425-5434`. Agent-run source-reply handling rewrites/persists eligible transcript mirrors at `chat.ts:5622-5647`, then broadcasts at `chat.ts:5682-5692`.

This establishes that the final broadcast and the transcript persistence paths are distinct, and that the normal agent-run transcript owner is the runtime SessionManager rather than the plugin-facing dispatcher callback.

### Pre-model `reply_dispatch` capability

At upstream `src/auto-reply/reply/dispatch-from-config.ts:1086-1110`, `createAbortAwareDispatcher(...)` forwards send, idle, queue-count, failed-count, cancellation-count, and completion methods. It does not forward `appendBeforeDeliver`.

At `dispatch-from-config.ts:1873-1876`, this wrapper is supplied as the dispatch-hook dispatcher. Therefore a plugin `reply_dispatch` handler cannot assume an append-capable dispatcher or intercept the later normal final through that wrapper.

### Public pre-delivery hook ordering

At upstream `src/auto-reply/dispatch.ts:424-438`, `installReplyPayloadSendingBeforeDeliver(...)` installs the public payload hook only when the original dispatcher exposes its internal `appendBeforeDeliver` capability. The hook is installed before `dispatchReplyFromConfig(...)` at `dispatch.ts:561-575`.

At upstream `src/auto-reply/reply/reply-dispatcher.ts:280-296`, the composed before-delivery hook runs in the serialized send chain; its returned payload becomes `deliverPayload`, and only then is `options.deliver(deliverPayload, dispatchInfo)` called. Thus `reply_payload_sending` is a pre-native-delivery rewrite point, not a post-native-persistence receipt.

### Native transcript identity and available primitives

The gateway transcript append helpers return `ok`, `messageId`, `message`, or an error. The injected assistant helper at upstream `src/gateway/server-methods/chat-transcript-inject.ts:86-117` can search an existing assistant row by caller-supplied `idempotencyKey`; its append operation at `:120-230` is a gateway-owned injection path, not a receipt for the normal model-run native append.

The ordinary agent-run path supplies runtime-owned transcript data to the gateway after dispatch. The source does not expose a plugin callback/API that returns the exact native persisted assistant row, its message ID, or an atomic commit token after the normal agent-run append. `chat.history`/transcript search can observe history, but a read followed by a separate `chat.inject` is not an atomic exactly-once boundary and cannot close the race between native persistence and recovery injection.

## Candidate boundaries considered and rejected

| Candidate | Why rejected |
|---|---|
| `reply_dispatch` + `appendBeforeDeliver` | Pre-model hook receives an abort-aware wrapper without `appendBeforeDeliver`; where present on another dispatcher, it is still pre-native persistence and does not prove the runtime-owned transcript commit. |
| `reply_payload_sending` | Runs before native delivery. Returning marker-bearing text can bind transport, but cannot prove the subsequent native transcript append committed. A timeout/failure after native append can still leave recovery believing delivery is unconfirmed. |
| `before_agent_finalize` | Upstream `src/plugins/hooks.ts:969-982` documents/runs it as a modifying hook that may request another model pass before a natural final is accepted. It exposes a candidate result before terminal completion, not an authoritative post-persistence receipt. Persisting there could race or duplicate the later native runtime append. |
| `agent_end` / model-output hooks | These expose lifecycle/output observations, not a public atomic native transcript persistence acknowledgement. They also occur at a boundary where native persistence ownership remains separate. |
| `chat.history` then marker/text comparison | Read-only observation is not atomic with native append. If the row is not yet visible, recovery can issue `chat.inject`; if it becomes visible concurrently, the two semantic effects can produce duplicate assistant messages. |
| `chat.inject` with a marker/idempotency key | This is a separate semantic injection and transcript-append side effect. The existing `host_delivery.py` path correctly checks history before injecting and fails closed when observation fails, but the check-and-inject sequence cannot prove mutual exclusion with a concurrent native Dashboard append. |
| Existing CogentNexus `reply_payload_sending` fallback | Task 160 live evidence showed the real operation produced `response_ready` but no CogentNexus durable delivery row; Task 154/155 repairs preserve public pre-delivery capture but do not create the missing post-native transcript authority. |

## Blocking argument

The required authority must establish, for one exact run/generation, all of:

1. exact final assistant-result identity;
2. authoritative native transcript persistence;
3. idempotent duplicate prevention;
4. durable CogentNexus delivery settlement;
5. fail-closed behavior when authority is unavailable; and
6. no second inference or native-send plus recovery-inject duplicate.

The exact source trace proves (1) is available before native delivery and that (2) is owned by the normal OpenClaw runtime transcript path. It does not expose (2) as a plugin-accessible post-commit proof that can be atomically joined to (3) and (4). Every available plugin/public candidate either runs before native persistence, only observes lifecycle state, or uses a separate read-then-inject side effect.

Under the Task-163 candidate rejection rule, any design that allows native persistence while CogentNexus still believes delivery is unconfirmed is unsafe. Therefore no safe CogentNexus-only repair can be claimed without weakening the contract or patching OpenClaw, both prohibited by the task.

## TDD status

- Phase A source investigation: completed; safe authority boundary: **not proven**
- Phase B test-only RED: **not authorized / not performed**
- RED commit SHA: none
- Failing assertion: none
- Phase C production repair: **not authorized / not performed**
- Phase D GREEN validation: not applicable
- OpenClaw source changes: `0`
- CogentNexus production changes: `0`
- Dependency changes: `0`

Creating a RED that assumes an unproven boundary would violate Task 163's ordering contract. The correct disposition is `BLOCKED`, not a speculative repair.

## Files and repository effects

Only the required report file was added:

`docs/operations/coordination/reports/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair.md`

No source, test, dependency, workflow, or OpenClaw files were changed.

## Hard-fence compliance

- Dashboard semantic Sends: `0`
- Dashboard semantic UI interaction: `0`
- Live Windows install/uninstall/reinstall/reset: `0`
- Gateway/Ollama/Supervisor live restart or mutation: `0`
- Manual Ticket/workflow/result/outbox/delivery/database mutation: `0`
- OpenClaw source patches: `0`
- Dependency upgrades: `0`
- Release/promotion/tag/merge to default or release branch: `0`
- Force pushes: `0`

All work was read-only source/history inspection plus the authorized report-only repository publication.

## Recommended next action for ChatGPT review

`BLOCKED` should be reviewed and accepted as the exact source-boundary outcome. Do not authorize a successor Dashboard Send or live Windows mutation. A future repair task must first provide an upstream-supported, plugin-accessible post-persistence/idempotency authority boundary (or explicitly authorize an OpenClaw core change outside this task's fence) before another RED or production repair can be valid.
