# Session Deletion Ownership Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Session deletion a single CogentNexus ownership boundary that invalidates and cleans all actionable state while preserving audit history, then make a later Discord message on the same `sessionKey` create an independent lifecycle with exact identity and generation fencing.

**Architecture:** Keep `cnx_sessions` as the durable lifecycle authority using `sessionKey + sessionId + generation`. Delete produces a durable tombstone and cleans actionable Ticket, delivery, recovery, and inference state without deleting history; a later lifecycle with a different OpenClaw `sessionId` reactivates the same routing key at the tombstone generation. All downstream consumers must use exact lifecycle/attempt identity and fail closed instead of selecting the latest run or row.

**Tech Stack:** TypeScript, Vitest, Node `node:sqlite`, existing CogentNexus-OpenClaw TicketStore/SQLite event log, OpenClaw plugin hooks, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-10-session-deletion-ownership-contract-design.md`

## Global Constraints

- Session identity is `sessionKey + sessionId + generation`; `sessionKey` alone is not lifecycle identity.
- Delete advances the generation exactly once and leaves a durable `state=deleted` tombstone.
- Delete cancels actionable Tickets, suppresses actionable delivery, cancels recovery, and makes old work non-actionable.
- Audit/history in `ticket_events` is retained.
- A new lifecycle on the same `sessionKey` must use a different `sessionId` and the tombstone generation.
- Never infer current ownership from latest Session, latest Ticket, latest run, or latest attempt ordering.
- Old lifecycle work must fail closed after generation rotation.
- First new owner turn may race ahead of asynchronous `session_start` but only with sufficient exact lifecycle evidence proving it is genuinely new.
- Provider/model remains provenance metadata only; no provider-selection or Gateway ownership changes.
- Keep `agent/v0.9.5-architecture-repair` as the write branch; do not modify `main`.
- No release/tag/merge promotion is part of this work.

---

### Task 1: Establish lifecycle deletion regression coverage

**Files:**
- Modify: `plugins/cogentnexus-openclaw/src/v090-session-ownership.test.ts`
- Modify: `plugins/cogentnexus-openclaw/src/v090.ts`

**Interfaces:**
- Consumes: `deleteSessionByKey(path,{sessionKey,message,sessionId})`, `finalizeSessionDeletion(path,sessionKey,reason)`, `reactivateSessionForLifecycle(path,{sessionKey,sessionId})`, `sessionAuthority(path,sessionKey)`.
- Produces: regression coverage proving delete/recreate semantics at the Session ownership boundary.

- [ ] **Step 1: Write the failing test**

Add a test that creates two Tickets under Discord key `agent:main:discord:channel:K`, queues a pending assistant delivery and direct recovery for the old generation, deletes lifecycle `A`, finalizes the tombstone, and verifies:

```ts
expect(sessionAuthority(path, key).state).toBe("deleted");
expect(sessionAuthority(path, key).generation).toBe(oldGeneration + 1);
expect(db.prepare("SELECT count(*) AS count FROM ticket_outbox WHERE owner_session_key=? AND delivery_status='pending'").get(key))
  .toEqual({count:0});
expect(db.prepare("SELECT count(*) AS count FROM cnx_assistant_delivery WHERE owner_session_key=? AND status='pending'").get(key))
  .toEqual({count:0});
expect(db.prepare("SELECT count(*) AS count FROM cnx_direct_recovery WHERE owner_generation=? AND state<>'cancelled'").get(oldGeneration))
  .toEqual({count:0});
expect(db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=?").get(oldTicketId).count).toBeGreaterThan(0);
expect((reactivateSessionForLifecycle(path,{sessionKey:key,sessionId:"A"})).accepted).toBe(false);
expect((reactivateSessionForLifecycle(path,{sessionKey:key,sessionId:"B"})).accepted).toBe(true);
expect(sessionAuthority(path,key).generation).toBe(oldGeneration + 1);
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test -- --run src/v090-session-ownership.test.ts`
Expected: the new assertions fail only where the existing implementation does not yet satisfy the full deletion ownership contract; no fixture/setup error is acceptable.

- [ ] **Step 3: Write minimal implementation**

Strengthen `revokeSession()` only where the failing assertions show a gap. The implementation must remain one transaction for lifecycle tombstoning and actionable cleanup, must preserve `ticket_events`, and must not transfer old ownership. Use exact owner generation for recovery and delivery cleanup rather than recency.

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test -- --run src/v090-session-ownership.test.ts`
Expected: PASS for the full focused file, including existing cross-session/reset/recreation tests.

- [ ] **Step 5: Commit**

```bash
git add plugins/cogentnexus-openclaw/src/v090.ts plugins/cogentnexus-openclaw/src/v090-session-ownership.test.ts
git commit -m "test: enforce session deletion ownership cleanup"
```

---

### Task 2: Fence inference attempts to the deleted lifecycle

**Files:**
- Modify: `plugins/cogentnexus-openclaw/src/v095-inference-attempt.ts`
- Test: `plugins/cogentnexus-openclaw/src/v095-inference-attempt.test.ts`
- Modify if needed: `plugins/cogentnexus-openclaw/src/v095-inference-hook-bridge.ts`

**Interfaces:**
- Consumes: `beginInferenceAttempt`, `findInferenceAttempt`, `bindRunId`, `finishInferenceAttempt` and Session authority fields.
- Produces: inference attempts that cannot remain actionable across a Session deletion/generation rotation and terminal evidence that remains attached to the original attempt.

- [ ] **Step 1: Write the failing test**

Create an old-generation inference attempt and then delete the owning Session. Verify that exact terminal handling cannot settle work as current lifecycle state:

```ts
const attempt = beginInferenceAttempt(db, {
  ticketId: ticket.ticketId,
  sessionKey: key,
  sessionGeneration: generation,
  callId: "call-A",
});
deleteSessionByKey(path,{sessionKey:key,message:"delete",sessionId:"S1"});
expect(() => finishInferenceAttempt(db, attempt.attemptId, "late-success")).toThrow(/session|generation|stale/i);
const row = findInferenceAttempt(db, "run-A", "call-A");
expect(row?.sessionGeneration).toBe(generation);
```

Also add the ambiguity fence: two attempts for the same `runId` with different `callId`s must not permit a consumer without `callId` to select one by `ORDER BY started_at DESC LIMIT 1`.

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test -- --run src/v095-inference-attempt.test.ts`
Expected: FAIL at the intended stale-lifecycle boundary if the current implementation allows late completion, or FAIL at the test's explicit ambiguity assertion if a latest-attempt shortcut remains.

- [ ] **Step 3: Write minimal implementation**

Add an exact Session authority check before terminalizing an attempt. The check must compare the attempt's `sessionKey` and `sessionGeneration` against current `cnx_sessions` state. Keep `callId` as the exact attempt identity; do not replace it with run recency. Update the hook bridge only to propagate exact `runId + callId + sessionKey + generation` evidence.

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test -- --run src/v095-inference-attempt.test.ts`
Expected: PASS, including existing provider/failover attempt tests.

- [ ] **Step 5: Commit**

```bash
git add plugins/cogentnexus-openclaw/src/v095-inference-attempt.ts plugins/cogentnexus-openclaw/src/v095-inference-attempt.test.ts plugins/cogentnexus-openclaw/src/v095-inference-hook-bridge.ts
git commit -m "fix: fence inference attempts by session generation"
```

---

### Task 3: Enforce deletion fencing at Delivery Core

**Files:**
- Modify: `plugins/cogentnexus-openclaw/src/v095-delivery-core.ts`
- Modify: `plugins/cogentnexus-openclaw/src/v095-delivery-core.test.ts`
- Modify: `plugins/cogentnexus-openclaw/src/v095-delivery-discord.ts` only if a test identifies an adapter identity leak

**Interfaces:**
- Consumes: `prepareDelivery`, `stageDelivery`, `acceptTransport`, `confirmDelivery`, `findExactDelivery`.
- Produces: delivery records that can only progress under the exact current Ticket/session/generation/inference/run identity.

- [ ] **Step 1: Write the failing test**

Extend the existing generation-rotation test so that after `transport_accepted`, Session deletion or rotation makes confirmation fail and leaves the Ticket non-completed:

```ts
expect(() => confirmDelivery(db, idempotencyKey, {evidenceType:"discord_message_sent"}))
  .toThrow(/owner session|generation is stale/i);
expect(store.get(ticket.ticketId)?.status).toBe("accepted");
```

Add an exact-inference test where a delivery prepared for `inferenceAttemptId=A` cannot be found/confirmed using `inferenceAttemptId=B` under the same Ticket/run/session.

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test -- --run src/v095-delivery-core.test.ts`
Expected: FAIL only where the current code allows stale delivery confirmation or identity substitution.

- [ ] **Step 3: Write minimal implementation**

Keep the current transaction-level Session check in `confirmDelivery()` and strengthen any missing checks in `stageDelivery()`/`acceptTransport()` so a session already tombstoned cannot receive new transport progress. Do not infer identity from an event's latest run or latest delivery row.

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test -- --run src/v095-delivery-core.test.ts`
Expected: PASS with the existing exact identity and idempotency coverage.

- [ ] **Step 5: Commit**

```bash
git add plugins/cogentnexus-openclaw/src/v095-delivery-core.ts plugins/cogentnexus-openclaw/src/v095-delivery-core.test.ts plugins/cogentnexus-openclaw/src/v095-delivery-discord.ts
git commit -m "fix: enforce delivery session deletion fencing"
```

---

### Task 4: Prevent deleted lifecycle recovery from waking

**Files:**
- Modify: `plugins/cogentnexus-openclaw/src/v090.ts`
- Modify: `plugins/cogentnexus-openclaw/src/wake_authority_v095.py` if the current wake path does not already reject stale owner generation
- Test: existing wake/recovery test file that owns the failing path

**Interfaces:**
- Consumes: `cnx_direct_recovery.owner_generation`, Session authority, Wake Authority decision path.
- Produces: a wake decision that is suppressed for deleted/superseded owner generation and permitted only for the exact current owner.

- [ ] **Step 1: Write the failing test**

Create a pending recovery with `owner_generation=g`, delete the Session, and invoke the wake path. Verify:

```ts
expect(result).toMatchObject({queued:false,suppressed:true});
expect(result.reason).toMatch(/session|generation|deleted/i);
```

Then reactivate lifecycle `S2` and verify that old recovery remains cancelled rather than being reused by the new lifecycle.

- [ ] **Step 2: Run test to verify it fails**

Run the focused wake/recovery test command for the owning suite.
Expected: FAIL if stale recovery is still wakeable or reused.

- [ ] **Step 3: Write minimal implementation**

At the wake authority boundary, require `state=active` and exact `owner_generation` equality before queueing or dispatching recovery. A Session tombstone must force suppression. Do not create a new recovery record by mutating the old lifecycle's row; the new lifecycle must get its own recovery ownership.

- [ ] **Step 4: Run test to verify it passes**

Run the focused wake/recovery test again.
Expected: PASS with existing scheduler/single-wake semantics unchanged.

- [ ] **Step 5: Commit**

```bash
git add plugins/cogentnexus-openclaw/src/v090.ts plugins/cogentnexus-openclaw/src/wake_authority_v095.py <focused-test-file>
git commit -m "fix: suppress recovery from deleted sessions"
```

---

### Task 5: Lock the Discord first-turn recreation race

**Files:**
- Modify: `plugins/cogentnexus-openclaw/src/v090.ts` only if needed
- Modify: `plugins/cogentnexus-openclaw/src/v090-session-ownership.test.ts`
- Inspect/fix: `plugins/cogentnexus-openclaw/src/v090-entry.ts` or current lifecycle hook registration file if the failure belongs there

**Interfaces:**
- Consumes: OpenClaw `before_agent_run` context with `sessionKey + sessionId`, `reactivateSessionForLifecycle`, lifecycle fence predicate.
- Produces: first owner turn for genuinely new `S2` accepted even when `session_start(S2)` is asynchronous, while stale `S1` remains blocked.

- [ ] **Step 1: Write the failing test**

Extend the existing first-turn ordering test with an explicit old/new lifecycle pair:

```ts
// Tombstoned A remains blocked.
expect(staleResult).toMatchObject({outcome:"block",category:"cnxclaw_lifecycle_identity"});
// New B is accepted before async session_start(B) commits.
expect(currentResult).not.toMatchObject({outcome:"block",category:"cnxclaw_lifecycle_identity"});
```

Verify that B becomes active through the lifecycle-registration path without a second generation increment.

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test -- --run src/v090-session-ownership.test.ts`
Expected: FAIL if the hook still depends exclusively on the asynchronous callback or if it cannot distinguish B from stale A.

- [ ] **Step 3: Write minimal implementation**

Use the exact `sessionId` in the owner context to distinguish a new lifecycle. Allow one deterministic registration of B against the tombstone generation, and keep S1 fail-closed. Do not weaken the check to `state=active` or `sessionKey` only.

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test -- --run src/v090-session-ownership.test.ts`
Expected: PASS, including stale callback and idempotency cases.

- [ ] **Step 5: Commit**

```bash
git add plugins/cogentnexus-openclaw/src/v090.ts plugins/cogentnexus-openclaw/src/v090-session-ownership.test.ts plugins/cogentnexus-openclaw/src/v090-entry.ts
git commit -m "fix: admit first turn of a new discord lifecycle"
```

---

### Task 6: Add the contract to coordination evidence

**Files:**
- Modify: `docs/operations/coordination/ACTIVE.md`
- Modify: `docs/operations/coordination/STATUS.md`
- Create: `docs/operations/coordination/reports/CNX-20260910-session-deletion-ownership-implementation.md`

**Interfaces:**
- Consumes: final focused test results, commit SHAs, and exact branch/PR metadata.
- Produces: a durable handoff stating the semantic contract, changed files, evidence, remaining CI state, and explicit release boundary.

- [ ] **Step 1: Write the evidence document**

Record:

```text
Contract: Session deletion invalidates operational ownership but retains history.
Old lifecycle: sessionKey + S1 + gN -> deleted + gN+1.
New lifecycle: same sessionKey + S2 -> active + gN+1.
No transfer: old Ticket/delivery/recovery/inference remain bound to S1/gN.
No heuristic: latest-row/latest-run selection is forbidden.
```

Include exact local test commands/results and exact commit SHAs.

- [ ] **Step 2: Update coordination state**

Set ACTIVE/STATUS to the actual next gate only after the code and focused tests are green. Do not mark release-ready merely because the contract document exists.

- [ ] **Step 3: Run documentation consistency checks**

Run the repository's Markdown/coordination consistency checks if present; otherwise run `git diff --check`.
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add docs/operations/coordination/ACTIVE.md docs/operations/coordination/STATUS.md docs/operations/coordination/reports/CNX-20260910-session-deletion-ownership-implementation.md
git commit -m "docs: record session deletion ownership implementation"
```

---

### Task 7: Full verification and exact-head CI gate

**Files:**
- No source changes unless a verification failure requires a targeted repair; then create a new TDD task before editing.

**Interfaces:**
- Consumes: all preceding commits on `agent/v0.9.5-architecture-repair`.
- Produces: exact-head verification evidence for local tests, build, validation, and GitHub Actions.

- [ ] **Step 1: Run focused lifecycle tests**

```bash
cd plugins/cogentnexus-openclaw
npm test -- --run src/v090-session-ownership.test.ts
npm test -- --run src/v095-inference-attempt.test.ts
npm test -- --run src/v095-delivery-core.test.ts
```

Expected: all focused suites PASS.

- [ ] **Step 2: Run broader plugin verification**

```bash
npm test
npm run build
npm run plugin:validate
```

Expected: all commands PASS.

- [ ] **Step 3: Check repository hygiene**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors and no unintended generated files.

- [ ] **Step 4: Fetch exact PR head**

Read PR #29 and record the actual `head_sha`. Verify it is the intended branch and is not `main`.

- [ ] **Step 5: Inspect exact-head GitHub Actions**

Fetch the workflow runs associated with the exact head SHA and require the relevant Validate, PS5.1 Acceptance Smoke, Windows Installer Pack Smoke, and PS5.1 Live Runner Smoke workflows to finish successfully before calling this change green.

- [ ] **Step 6: Resolve verification failures minimally**

If any workflow fails, inspect the failing job and logs, identify the concrete failure, add a focused RED test when behavior is wrong, and make the minimum fix on the same feature branch. Do not rerun blindly without understanding the failure.

- [ ] **Step 7: Commit verification evidence**

After all gates are green, update the implementation report and coordination state with exact commit/workflow IDs and keep PR #29 Draft because release/merge promotion is not authorized by this contract.

```bash
git add docs/operations/coordination/reports/CNX-20260910-session-deletion-ownership-implementation.md docs/operations/coordination/ACTIVE.md docs/operations/coordination/STATUS.md
git commit -m "docs: record session deletion verification evidence"
```

---

## Completion Criteria

The contract is considered implemented only when:

1. Delete makes the old lifecycle fully non-actionable inside CNX.
2. Actionable Ticket, outbox, assistant delivery, recovery, and inference state cannot survive as work for the old lifecycle.
3. Audit/history remains queryable.
4. A new Discord message on the same `sessionKey` creates a new lifecycle with a different `sessionId` and exactly the tombstone generation.
5. Stale lifecycle callbacks and late inference/delivery evidence fail closed.
6. New lifecycle work does not inherit old Ticket/delivery/recovery ownership.
7. First-turn asynchronous `session_start` ordering remains safe.
8. No latest-run/latest-row heuristic remains in the ownership-critical path.
9. Focused tests, full plugin tests/build/validation, and exact-head CI are green.
10. No release/tag/merge promotion has been performed.
