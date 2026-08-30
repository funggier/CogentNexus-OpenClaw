# CNX-20260831-167 — Hermes Native Delivery Staging Root-Cause Repair Report

## Disposition

**PASS**

This repository-only repair addresses the Task-166 durable-delivery failure. No Dashboard semantic Send, live runtime mutation, install-over, dependency upgrade, upstream OpenClaw patch, recovery, or external ticket mutation was performed.

## Authority and provenance

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Execution base / remote HEAD before repair: `5b481ff1c5d64e40f9a87ff792599c63cfcf84a9`
- Pinned upstream OpenClaw source read-only SHA: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`
- Accepted Task-166 report: `docs/operations/coordination/reports/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`
- Task-166 review: `docs/operations/coordination/reviews/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance-review.md`

The upstream checkout was read-only and was not used as a production patch source.

## Observed failure and root cause

Task 166 produced the exact assistant response in the Dashboard and native transcript, but the Ticket ended with `durableDelivery=false`, no `cnx_assistant_delivery` row, and no delivery marker. The prior implementation collected the candidate only in `before_agent_finalize`, then attempted to inject the marker in `before_message_write`.

The pinned OpenClaw lifecycle shows that this order is inverted for native persistence:

1. Native SessionManager invokes `before_message_write` before appending the message.
2. Native transcript persistence/update occurs.
3. The terminal `agent_end` path invokes the `before_agent_finalize`/terminal-delivery gate.

Therefore the prior implementation could receive the final candidate after the only pre-write marker opportunity had already passed. The Task-164 fixture used the opposite order and did not reproduce the live failure.

Relevant pinned source evidence:

- `src/agents/session-tool-result-guard.ts`: pre-write hook is invoked while preparing the native append.
- `src/sessions/transcript-events.ts` and session accessor: transcript update is emitted from the native persistence boundary.
- `src/agents/embedded-agent-subscribe.handlers.lifecycle.ts:273–297`: terminal delivery gate runs from the agent-end lifecycle path.
- `src/agents/embedded-agent-runner/run/attempt.ts`: the terminal lifecycle is reached after the assistant turn has been assembled/persisted.

## TDD evidence

### Existing RED

New test:

```text
plugins/cogentnexus-openclaw/src/v167-native-delivery-staging-order.test.ts
```

The test models the production-shaped sequence:

```text
before_message_write
native transcript update
before_agent_finalize
```

Before the repair it failed with:

```text
expected persisted native assistant text to contain
'<!-- cogentnexus-openclaw-delivery:'
Received: 'CNX-V167-NATIVE-ORDER-ACK'
```

This is the direct reproduction of the Task-166 failure mode.

### Minimal production repair

Changed:

```text
plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
```

The `before_message_write` handler now:

- Resolves the unique accepted, direct, Dashboard ticket by `owner_session_key` when no earlier candidate exists.
- Refuses to infer ownership when more than one eligible ticket exists.
- Stages the exact assistant text before native persistence.
- Injects the deterministic delivery marker before the native append.
- Retains the existing transcript settlement path and idempotency protections.
- Leaves `before_agent_finalize` available for the terminal lifecycle boundary.

No OpenClaw source was modified.

## GREEN and regression verification

### Targeted Task-167 test

```text
./node_modules/.bin/vitest run src/v167-native-delivery-staging-order.test.ts
```

Result after repair: **PASS**.

The test verifies:

- Native persisted message contains the delivery marker.
- One durable delivery row exists with the exact response text.
- Delivery is `delivered`.
- Idempotency key exists.
- Claim token is cleared after settlement.
- Ticket is `completed`.
- `delivery_confirmed_at` is populated.

### Related regression set

```text
./node_modules/.bin/vitest run \
  src/v167-native-delivery-staging-order.test.ts \
  src/v162-dashboard-transcript-authority.test.ts \
  src/v091-dashboard-verified-delivery.test.ts \
  src/v090-native-restart-boundary.test.ts \
  src/delivery-continuity.test.ts
```

Result: **5 test files passed, 34 tests passed**.

### Full plugin suite

```text
./node_modules/.bin/tsc --noEmit
./node_modules/.bin/vitest run
```

Results:

- TypeScript: exit `0`
- Vitest: **53 test files passed, 273 tests passed**

### Official build and schema verification

```text
npm run plugin:build
```

Result: exit `0`.

```text
CogentNexus-OpenClaw mixed-plugin artifact verification: PASS
(45 config properties, 5 tools)
```

## Scope and hard-fence verification

- Dashboard semantic Send: `0`
- Dashboard click/type/focus interaction: `0`
- Live runtime mutation: `0`
- Windows install-over: `0`
- Dependency manifest/lockfile change: `0`
- OpenClaw upstream patch: `0`
- Manual Ticket/DB/outbox/delivery mutation: `0`
- Recovery/retry/inference: `0`
- Force push/merge/release/tag: `0`

The only intended repository changes are:

```text
plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
plugins/cogentnexus-openclaw/src/v167-native-delivery-staging-order.test.ts
docs/operations/coordination/reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md
```

## Non-blocking execution notes

- The first test command used an npm wrapper form that interpreted `--reporter` as an unsupported npm config flag. It failed before Vitest execution; the local Vitest binary was then used successfully.
- `npm ci --ignore-scripts` installed the existing lockfile dependencies in the temporary checkout only. No dependency files changed. npm reported the pre-existing vulnerability notice; no audit fix or dependency upgrade was run.

## Review boundary

Task 167 repairs and verifies the repository behavior only. It does not authorize a new live Dashboard Send or install-over. Any live reacceptance must be authorized by a separately reviewed successor task.
