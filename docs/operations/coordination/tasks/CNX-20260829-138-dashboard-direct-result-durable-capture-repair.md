# CNX-20260829-138 — Dashboard Direct-Result Durable Capture Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `OFFLINE_SOURCE_TDD_DIAGNOSIS_AND_REPAIR_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Diagnose and repair the clean Task-137 product/runtime defect in which a real Dashboard direct response became visibly available and `response_ready` was committed, but the exact final payload was not durably staged into `cnx_assistant_delivery` before the receipt deadline. The runtime correctly refused regeneration to avoid duplicate output, leaving the Ticket failed.

This is an **offline source TDD repair task**. It does not authorize another live Dashboard semantic Send.

## Authority and historical evidence

Task-137 report:

`docs/operations/coordination/reports/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-137-final-dashboard-durable-delivery-reacceptance-review.md`

Accepted source candidate before this repair:

`1424d6fbee2c458c8c30440616783d2fa1bc1201`

Accepted installed payload/plugin fingerprint before this repair:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Task-137 historical Ticket:

`CNXT-a38e1408-205f-4606-a5c8-ec54e9515aea`

Task-137 Send ledger is permanently consumed `1 / 1`. Do not resend its nonce or semantics.

## Confirmed defect boundary

The following are proven by Task 137 and source inspection:

- Ticket-first admission worked;
- one direct model call completed;
- the visible Dashboard result matched the requested ACK exactly;
- `response_ready` was committed;
- no `cnx_assistant_delivery` direct-result row existed;
- after the receipt deadline the shipped fail-closed path produced `failure_delivery_suppressed` rather than regenerating inference;
- no duplicate semantic external side effect was observed;
- production source on the branch had not drifted from accepted candidate `1424d6f...`.

The exact implementation root cause is **not yet proven**. Do not assume one before RED reproduction.

Relevant source surfaces include, but are not automatically limited to:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`
- `plugins/cogentnexus-openclaw/src/v092-durable-delivery-boundary.ts`
- `plugins/cogentnexus-openclaw/src/v093-response-ready-boundary.test.ts`
- release wiring in `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- only directly implicated Ticket/delivery storage code if required by the reproducer.

Potential callback-shape, correlation, final-count, registration/order, session-authority, or staging-timing explanations are hypotheses only.

## Phase 0 — fresh authority and baseline

Before editing:

1. Fresh-fetch branch HEAD, `ACTIVE.md`, and `STATUS.md`; require Task 138 to remain authoritative and unsuperseded.
2. Confirm no unexpected production/source change has landed since Task 138 was opened.
3. Record exact starting HEAD and relevant file SHAs.
4. Inspect existing Dashboard verified-delivery tests and release wiring before modifying production code.
5. Do not touch the installed Windows runtime during this task.

If branch authority has changed or unrelated source edits conflict with the repair boundary, stop and report `BLOCKED` rather than overwrite them.

## Phase 1 — deterministic RED reproducer

Create the narrowest automated regression test that reproduces the Task-137 class through the **registered runtime delivery hook/callback boundary**, not merely by manually calling `finalizeDirectRun` into the already-known fail-closed fallback.

The RED test must demonstrate a realistic callback/event/dispatcher shape or sequencing under which:

1. a Dashboard direct Ticket exists and is correlated to the real run/session contract;
2. a final assistant payload is available for native Dashboard delivery;
3. the current shipped hook path fails to stage the exact final text into `cnx_assistant_delivery` before the direct run reaches `response_ready`/receipt monitoring;
4. the result would consequently enter the unverifiable fail-closed class if left unchanged.

Requirements:

- RED must fail against the unmodified Task-138 starting source for the intended semantic reason;
- no production/source fix before RED evidence is captured;
- avoid brittle tests that merely assert current implementation details without modeling the runtime contract;
- preserve redaction/no-secret telemetry behavior.

Record the exact failing test name, command, assertion, and observed failure.

If no deterministic source-level reproducer can be constructed from available contracts, do **not** guess a production fix. Publish Task 138 as `BLOCKED_DIAGNOSTIC_EVIDENCE_GAP` with the smallest additional diagnostic instrumentation/task recommendation.

## Phase 2 — root-cause proof

From the RED reproducer and source trace, state the exact condition that prevented durable staging.

Root-cause evidence must identify:

- the hook/callback API contract actually exercised;
- which correlation/filter/ordering/staging condition rejected or missed the valid final payload;
- why existing tests did not cover that condition;
- why the proposed fix does not broaden delivery ownership or permit duplicate semantic delivery.

Do not classify unrelated legacy recovery code as root cause merely because it later emitted the fail-closed event.

## Phase 3 — minimal production fix

Apply the smallest change that makes the valid Dashboard final payload durable **before native transport can make the result externally visible** for the reproduced contract.

The fix must preserve all of these invariants:

- Ticket-first admission remains unchanged;
- exact final text is stored durably before transport ownership proceeds;
- one stable idempotency identity per Ticket/owner generation;
- repeated observation of the same final remains idempotent;
- changed final content under the same durable identity fails closed;
- session authority/generation fencing remains enforced;
- native delivery acknowledgement remains required for successful terminal completion;
- once a durable `direct_result` exists, inference regeneration remains forbidden;
- if the final payload genuinely cannot be durably captured, fail closed rather than risk duplicate output;
- no payload/nonce/secrets are added to logs.

Do not weaken duplicate prevention simply to turn Task-137 failure into completion.

## Phase 4 — GREEN validation

At minimum run and record:

1. the new targeted regression test alone — must GREEN;
2. `v091-dashboard-verified-delivery.test.ts` — must GREEN;
3. `v093-response-ready-boundary.test.ts` — must GREEN;
4. any directly affected delivery/recovery tests — must GREEN;
5. full plugin `npm test` — must GREEN;
6. plugin build — must GREEN;
7. `npm run plugin:validate` — must GREEN.

If the repository CI is triggered by the repair commits, wait for and record the relevant workflow/check conclusions. A failing relevant workflow blocks Task 138 completion unless proven unrelated and separately documented.

Production/source changes require re-running the full relevant validation after the final edit.

## Phase 5 — scope and diff audit

Before reporting completion:

- inspect the complete diff from Task-138 starting HEAD;
- require only files necessary for the regression test, minimal repair, and Task-138 report/coordination bookkeeping;
- verify no installer, lifecycle, provider, model, unrelated recovery, release, or dependency change slipped into scope;
- record exact final source HEAD before the report commit and exact report commit HEAD after publication.

## Required Task-138 report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-138-dashboard-direct-result-durable-capture-repair.md`

Include:

- Task ID, branch, starting HEAD, and ACTIVE verification;
- exact RED test and failing evidence before production edit;
- exact source-level root cause, or explicit diagnostic evidence gap if not proven;
- changed files and rationale;
- minimal fix summary;
- targeted GREEN results;
- full plugin tests/build/plugin validation results;
- relevant GitHub Actions/workflow results;
- exact source repair commit(s) and final HEAD;
- scope/diff audit;
- explicit confirmation that no live Dashboard semantic Send, install/reinstall/reset, lifecycle/recovery action, provider/model/config mutation, database cleanup, release, merge, tag, or force push occurred;
- final verdict: `COMPLETED`, `PARTIAL`, `BLOCKED`, or `FAIL`.

Then STOP for independent ChatGPT review.

## Hard fence

Task 138 authorizes repository/source/test/CI work only.

Forbidden:

- any live Dashboard semantic Send/resend;
- reuse of Task-136 or Task-137 nonce/semantics;
- alternate semantic injection through CLI/Gateway/API/database;
- install/install-over/reset/uninstall/reinstall;
- start/stop/restart/enable/disable of live runtime;
- recovery/crash injection;
- provider/model/OpenClaw/config mutation;
- manual Ticket/outbox/delivery/ack mutation;
- SQLite cleanup/normalization/write on the live runtime database;
- process kill or task/service mutation;
- reboot;
- credential/secret access;
- merge/tag/GitHub Release;
- force push.
