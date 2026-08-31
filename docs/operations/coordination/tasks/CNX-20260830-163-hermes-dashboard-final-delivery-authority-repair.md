# CNX-20260830-163 — Hermes Dashboard Final-Delivery Authority Repair Attempt

Status: `READY_HERMES`

Execution mode: `REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_HERMES`

Current authorization: `CNX-20260830-163_HERMES_REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR`

Task ID: `CNX-20260830-163`

Updated: 2026-08-30 ICT

Executor: Hermes

Coordinator / final reviewer: ChatGPT

Review type at completion: ChatGPT review required before successor authorization

## Purpose

Give Hermes an isolated, repository-only attempt at the unresolved Task-162 production-boundary investigation and TDD repair, without repeating any semantic Dashboard action or touching the live Windows runtime.

This task is a delegated continuation of:

`docs/operations/coordination/tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`

Task 162 remains the parent repair objective. Task 163 exists so Hermes can independently trace the exact OpenClaw Dashboard/webchat delivery path, produce a production-faithful RED regression, and—only if the boundary is proven—implement the smallest CogentNexus-OpenClaw repair.

## Authoritative repository state

Repository:

`funggier/CogentNexus-OpenClaw`

Working branch:

`agent/v0.9.3-full-stabilization`

Branch state on task creation must not be assumed current. Hermes must fetch GitHub immediately before starting and before every write. GitHub remote state is authoritative.

Exact upstream OpenClaw source target for investigation:

- version: `v2026.7.1-2`
- commit: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

Upstream OpenClaw is read-only external evidence. Do not patch, fork, vendor, or upgrade it.

## Required reading before work

Read these first:

1. `docs/operations/coordination/ACTIVE.md`
2. `docs/operations/coordination/STATUS.md`
3. `docs/operations/coordination/tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`
4. `docs/operations/coordination/reports/CNX-20260830-162-session-handoff-checkpoint.md`
5. `docs/operations/coordination/reports/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance.md`
6. `docs/operations/coordination/reviews/CNX-20260830-160-dashboard-single-send-durable-delivery-reacceptance-review.md`
7. current production implementation around `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
8. recovery behavior in `skills/cogentnexus-openclaw/scripts/host_delivery.py`

Do not rely on summaries when exact source/history is available.

## Proven facts inherited from Task 160 / 161 / 162

Treat the following as established unless fresh source evidence disproves them:

- the authorized Dashboard request completed model inference and produced assistant text;
- `response_ready` committed, but no authoritative CogentNexus assistant durable-delivery row committed;
- the observed pre-model `reply_dispatch` dispatcher had no `appendBeforeDeliver`;
- exact OpenClaw source shows `reply_dispatch` runs before normal model dispatch and receives an abort-aware wrapper;
- the eventual normal final reply uses the original dispatcher, not the pre-model wrapper;
- therefore CogentNexus cannot assume `reply_dispatch` owns final persistence;
- Task-154's later `reply_payload_sending` fallback is not a reliable production contract;
- exact upstream `before_agent_finalize` is awaited post-model/pre-terminal and exposes `lastAssistantMessage`, but persistence from that hook alone is not yet accepted;
- native Dashboard persistence plus CogentNexus recovery injection must never produce duplicate semantic assistant messages.

## Primary objective

Prove an exact, plugin-accessible, exactly-once authority boundary for Dashboard/webchat assistant delivery that can establish all of:

1. the exact final assistant result identity;
2. authoritative native transcript persistence;
3. idempotent duplicate prevention;
4. durable CogentNexus delivery settlement;
5. fail-closed behavior when persistence cannot be proven;
6. no re-inference after an assistant result already exists;
7. no native-send + recovery-inject duplicate semantic side effect.

If no such public boundary exists without patching OpenClaw, stop and report `BLOCKED` with exact source evidence. Do not invent a weaker contract.

## Exact upstream trace required

Inspect exact OpenClaw commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`, especially:

`src/gateway/server-methods/chat.ts`

Trace and document, with file/line or commit-source evidence:

1. where `chat.send` creates the webchat `createReplyDispatcher(...)` instance;
2. the dispatcher deliver callback for final assistant payloads;
3. broadcast/delivery ordering relative to transcript mutation;
4. where the assistant transcript row is appended or otherwise persisted;
5. what message ID, run ID, session ID, hash, idempotency key, transcript search primitive, or dedupe primitive identifies that persisted assistant result;
6. how `chat.send` decides terminal success/failure;
7. whether plugin hooks can observe or verify the native persisted assistant row after the model result exists;
8. whether Gateway public API/runtime state can verify the exact native persistence without causing another semantic side effect;
9. how any candidate boundary interacts with `chat.inject` and current `host_delivery.py` recovery behavior.

Also inspect any directly referenced upstream helper files needed to establish the real order. Do not infer ordering from function names alone.

## Candidate rejection rule

Reject any candidate repair if any execution order can produce:

1. native Dashboard assistant persistence/send;
2. CogentNexus still believing delivery is unconfirmed;
3. recovery later calling `chat.inject` for the same semantic assistant result;
4. a second visible/persisted assistant message.

A text equality guess by itself is not sufficient unless the exact native transcript authority and race behavior are proven.

## TDD contract

### Phase A — investigation only

No production source change before the exact authority boundary is proven.

### Phase B — test-only RED

After proving the boundary, add the smallest production-faithful regression test that reproduces the actual Dashboard path.

The RED must demonstrate at minimum:

- pre-model `reply_dispatch` does not provide an append-capable dispatcher;
- no second `reply_payload_sending` callback is required or assumed;
- the exact assistant result becomes available on the real post-model path;
- success remains withheld until authoritative persistence is verified;
- if native persistence already exists, CogentNexus does not schedule or execute duplicate recovery injection;
- if authoritative persistence cannot be established, behavior remains fail-closed;
- no second inference/model generation occurs after the assistant result already exists.

Commit this **test-only RED state separately before any production source change**.

Record in the report:

- exact RED commit SHA;
- exact failing test/assertion;
- why the failure is expected on pre-repair production code;
- relevant CI/Actions run and job if CI is triggered.

### Phase C — minimal repair

Only after verified RED, modify the smallest possible CogentNexus-OpenClaw production surface required to make the regression GREEN.

Prefer existing public OpenClaw plugin/runtime/API primitives. Do not patch OpenClaw.

Preserve:

- Task-155 duplicate safety;
- one authoritative assistant result per run/generation;
- no re-generation after a result already exists;
- fail-closed semantics;
- Ticket/workflow/delivery ownership boundaries;
- durable recovery semantics;
- no duplicate native-send + recovery-inject side effect.

Do not perform unrelated refactors.

### Phase D — GREEN validation

At the exact final production repair SHA, run all relevant repository validation, including at minimum:

- full CogentNexus-OpenClaw plugin tests;
- Task-155 duplicate public-hook regression;
- new Task-163 production-faithful regression;
- repository Validate workflow / relevant full matrix;
- Windows PowerShell 5.1 Acceptance Smoke;
- Windows Installer Pack Smoke;
- dependency/package audit required by the repository.

Any production/source change after a validation run invalidates that run for final acceptance and requires fresh validation.

## Repository-only authorization

Hermes is authorized to:

- inspect GitHub repository state and history;
- inspect exact upstream OpenClaw source read-only;
- add regression tests;
- make the minimal CogentNexus-OpenClaw production repair after RED;
- run repository-local tests;
- trigger/inspect repository CI and workflows;
- commit/push only to `agent/v0.9.3-full-stabilization` using normal non-force history;
- write a Task-163 report with exact evidence.

## Hard fence — prohibited actions

Hermes must NOT:

- send any semantic Dashboard message;
- click/focus/type/paste into Dashboard for semantic testing;
- send a semantic user message through another live OpenClaw surface;
- install-over, uninstall, reinstall, or reset the real Windows candidate;
- restart or mutate live Gateway, Ollama, Supervisor, or OpenClaw runtime;
- manually edit Ticket/workflow/result/outbox/delivery/database live state;
- delete arbitrary live state;
- patch OpenClaw source;
- upgrade dependencies;
- change unrelated product behavior;
- publish a release/tag/package;
- merge to default/release branch;
- force push.

Repository CI on hosted runners is allowed. Real-machine lifecycle or semantic acceptance is not.

## Coordination ownership

While Task 163 is active, Hermes is the executor. ChatGPT remains coordinator/final reviewer.

Hermes should not open a live-successor task on its own. It should finish by publishing a report and setting out a recommended disposition:

- `PASS` — proven boundary, RED committed before production repair, repair GREEN, required validation GREEN;
- `FAIL` — attempted repair is demonstrated incorrect or validation fails;
- `BLOCKED` — no safe public authority boundary exists or an external constraint prevents a valid TDD repair.

Do not convert uncertainty into PASS.

## Required completion report

Create:

`docs/operations/coordination/reports/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair.md`

The report must include:

1. exact starting HEAD;
2. upstream source trace and exact delivery/transcript ordering;
3. candidate boundaries considered and rejected;
4. chosen authority boundary and duplicate-safety argument;
5. test-only RED commit SHA and failing assertion;
6. production repair commit(s);
7. files changed;
8. tests/workflows and exact results;
9. exact final HEAD;
10. hard-fence compliance statement;
11. PASS / FAIL / BLOCKED;
12. recommended next action for ChatGPT review.

## Acceptance gate

Task 163 itself does not authorize any new Dashboard Send or live Windows mutation, even if Hermes reports PASS.

ChatGPT must review Hermes' evidence and repository state first. Only after explicit ChatGPT acceptance may coordination advance to the separate repaired-candidate Windows install-over/provenance/health checkpoint.
