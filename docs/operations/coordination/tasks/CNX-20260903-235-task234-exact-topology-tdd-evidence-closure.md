# CNX-20260903-235 — Task-234 Exact-Topology TDD Evidence Closure

Status: `READY_FOR_HERMES`
Date: 2026-09-03 ICT
Parent: `CNX-20260903-234`
Failure parent: `CNX-20260903-233`
Installer-requalification parent: `CNX-20260902-230`
Accepted repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows + repository operator
Coordinator / independent reviewer: ChatGPT

## Purpose

Close the remaining TDD/provenance and production-shaped settlement evidence gaps in Task 234 **before any live installation**.

Task-234 report claimed:

`PASS_DASHBOARD_ORIGIN_DISCORD_SESSION_DURABLE_STAGING_REPAIR_GREEN`

Independent review disposition:

`REJECT_PASS_TDD_EVIDENCE_INCOMPLETE__FUNCTIONAL_REPAIR_GREEN__EXACT_TOPOLOGY_HARDENING_REQUIRED`

The candidate repair remains functionally promising and fully GREEN in Actions, but it is not yet accepted live-install authority.

## Current candidate authority

Task-234 candidate repair SHA:

`43fd1d6f988431c7a94d24abc8a6811de46f78fa`

Candidate plugin payload fingerprint:

`964d471f9e330cfeffd270f2200d563dea8c3e7b9252409660df96f1173f58b7`

Task-234 opening authority / predecessor production tree:

`89a0f539c02dfef971cec9b6baa98a1929d2fb13`

Task-234 test-only commit:

`6b1e496fa67b0f09678268ba918a98a824610286`

Primary repair commit:

`278a235fa9df75990a3ea7f1a8e3930441ead76b`

Final type-annotation commit:

`43fd1d6f988431c7a94d24abc8a6811de46f78fa`

Task-234 report HEAD:

`71ed478c6a403361510a06c83b0844fe2fc44f3e`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Why Task 235 exists

Two independent evidence gaps remain.

### Gap A — committed corrected RED is not independently proven

`6b1e496...` is test-only, but the final regression harness needed corrections that landed in the same commit as production repair `278a235...`.

The corrected test therefore needs a predecessor-tree reconstruction proving that, **with production still exactly at `89a0f...`**, the production-shaped Dashboard-origin case fails for the intended staging reason while the Discord-origin negative case remains valid.

This is evidence reconstruction only; do not rewrite history.

### Gap B — exact Discord-associated owner settlement is not directly tested

The final Task-234 regression proves durable staging and marker creation but stops while the row is `pending`.

The exact new topology must be tested through:

```text
Dashboard-origin context
-> Discord-associated owner retained
-> before_agent_finalize candidate
-> before_message_write durable staging + marker
-> native transcript update
-> direct_result delivered
-> Ticket completed
-> exactly one delivery_confirmed
-> no direct_redelivery_timeout
-> no recovery regeneration
```

The same owner with true Discord-origin context must remain outside Dashboard staging.

## Hard live-system fences

Task 235 is repository/evidence hardening only.

```text
Dashboard semantic Sends: 0
Discord-origin semantic Sends: 0
direct operator Discord/API Sends: 0
semantic retries: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway mutation: 0
live plugin mutation: 0
provider/model substitution: 0
process termination: 0
Task-223/Task-233 forensic evidence mutation: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

Read-only inspection of the live installed OpenClaw package/source/docs is authorized.

## Phase A — fresh authority

Before work:

1. fetch fresh branch HEAD;
2. verify Task 235 is active and `READY_FOR_HERMES`;
3. verify `43fd1d6...` and `89a0f...` remain ancestors of current authority as expected;
4. compare Task-234 report HEAD/current coordination state and classify any drift;
5. verify public `v0.9.3` remains `26ce64a...`;
6. verify exact candidate Actions remain:
   - Validate `33760819493` SUCCESS;
   - Windows Installer Pack Smoke `33760819324` SUCCESS;
   - PS5.1 Acceptance Smoke `33760819312` SUCCESS.

Unexpected unrelated product/source/test/workflow drift:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — exact OpenClaw 2026.7.1-2 ingress contract

Read the exact installed/source contract for OpenClaw `2026.7.1-2` used by the live runtime.

Capture authoritative evidence for the hook contexts used by:

- `before_agent_finalize`;
- `before_message_write`.

At minimum establish the exact semantics and availability of:

```text
ctx.messageProvider
ctx.channel
ctx.channelId
ctx.sessionKey
ctx.runId
```

Determine whether `messageProvider` and `channel` are guaranteed equivalent provider-surface aliases, whether either is canonical, and whether contradictory recognized values can occur legitimately.

Do not use current-main documentation alone when exact installed source/type/docs are available.

If exact-version evidence cannot establish a trustworthy surface discriminator:

`BLOCKED_INGRESS_SURFACE_CONTRACT`

## Phase C — predecessor corrected-RED reconstruction

Use a **unique disposable checkout/worktree** rooted exactly at:

`89a0f539c02dfef971cec9b6baa98a1929d2fb13`

Do not alter the coordination branch for this phase.

Apply only a corrected production-shaped test/harness representing the final intended Task-234 topology. Production implementation must remain byte-identical to predecessor.

Prove with `git diff` that only test/harness evidence differs from `89a0f...`.

The reconstructed test must use a Discord-associated owner:

`agent:main:discord:channel:1531199905673252946`

and valid schema/session authority setup.

### Required reconstructed RED result

Dashboard-origin trusted context must fail against predecessor production for the intended reason at the Dashboard durable staging boundary, e.g. no marker/durable `direct_result` because the Discord-associated owner is rejected by Dashboard-only staging.

The paired true Discord-origin case on the same owner must remain negative without a Dashboard staging row/marker.

The failure must not be caused by:

- missing schema;
- un-awaited async hook;
- malformed run ID / fixture;
- test cleanup race;
- syntax/type/build failure unrelated to the product boundary.

Record exact command/output and failure assertion.

If corrected predecessor test does not fail for the intended reason:

`FAIL_RED_RECONSTRUCTION`

## Phase D — strengthen current exact-topology regression

On the normal branch/current candidate, extend or replace the Task-234 regression so the Dashboard-origin + Discord-associated owner case proves the complete native settlement chain.

Required assertions:

1. owner session remains exactly the Discord-associated key;
2. `before_agent_finalize` receives trusted Dashboard/WebChat context;
3. `before_message_write` returns the exact assistant answer plus CogentNexus marker;
4. exactly one `cnx_assistant_delivery` row exists with:
   - `kind=direct_result`;
   - correct text;
   - `status=pending` before transcript settlement;
   - native claim present/unexpired;
5. Host recovery cannot claim/regenerate while native ownership is pending;
6. simulate only the already-proven OpenClaw boundary: native append completed, then `onSessionTranscriptUpdate` emits the marker-bearing message;
7. row becomes `delivered`;
8. Ticket becomes `completed` with non-null `delivery_confirmed_at`;
9. exactly one `delivery_confirmed` event exists;
10. exactly one logical completion exists for the Ticket;
11. no `direct_redelivery_timeout` event exists for that Ticket;
12. later recovery returns no duplicate/regenerated output.

### Same-owner Discord negative control

With trusted Discord-origin context on the same owner:

- no Dashboard marker is injected;
- no Dashboard `direct_result` is created;
- no native Dashboard transcript candidate settles the Discord turn;
- existing Discord/external-channel semantics remain authoritative.

### Missing/ambiguous context

Test missing and contradictory recognized ingress context according to the exact Phase-B contract.

If the exact framework contract says contradictory provider fields are invalid/ambiguous, they must **not** grant the new Dashboard-on-Discord-owner exception.

If exact `2026.7.1-2` semantics establish one field as authoritative and another as a different concept, encode that documented precedence explicitly.

Never guess.

## Phase E — decision on production source

### If all strengthened tests pass on `43fd1d6...`

Do **not** edit production source.

Record:

`CANDIDATE_REPAIR_CONFIRMED_WITHOUT_ADDITIONAL_PRODUCTION_CHANGE`

### If a strengthened safety/settlement test fails

Treat that as a new genuine RED on the current candidate.

Requirements:

1. commit the test-only RED separately;
2. prove deterministic failure for the expected product reason;
3. make the smallest production fix in a separate commit;
4. rerun targeted GREEN;
5. preserve owner identity and cross-surface routing fences.

Do not weaken tests or broaden every Discord owner into Dashboard.

## Phase F — targeted validation

At minimum run:

- strengthened Task-235/Task-234 exact-topology regression;
- `v162-dashboard-transcript-authority.test.ts`;
- `v091-dashboard-verified-delivery.test.ts`;
- `v154-dashboard-public-hook-fallback.test.ts`;
- `v207-direct-discord-no-reply.test.ts`;
- `v090-dashboard-delivery.test.ts`;
- `v093-response-ready-boundary.test.ts`;
- any ingress/provenance test directly affected.

All must pass.

## Phase G — full GREEN

Run and record on the exact final candidate:

- full plugin `npm test`;
- build/evaluation;
- `npm audit --omit=dev`;
- plugin validation;
- package dry-run;
- representative/full Python validation required by workflow;
- PowerShell/POSIX syntax and acceptance checks;
- `git diff --check`;
- Validate workflow;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

Do not increase timeouts merely to obtain GREEN.

## Phase H — provenance

Record:

- disposable predecessor checkout SHA;
- exact reconstructed test diff and RED output;
- any new test-only RED commit if current candidate exposes a defect;
- any additional minimal production repair commit;
- exact final production/test changed files;
- exact plugin payload fingerprint;
- exact Actions run IDs/conclusions;
- public tag immutability;
- clean final worktree;
- retry ledger;
- zero live mutation ledger.

## Allowed final dispositions

Use one primary disposition:

- `PASS_TASK234_TDD_EVIDENCE_CLOSED__EXACT_TOPOLOGY_GREEN`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_INGRESS_SURFACE_CONTRACT`
- `FAIL_RED_RECONSTRUCTION`
- `FAIL_EXACT_TOPOLOGY_SETTLEMENT`
- `FAIL_CROSS_SURFACE_FENCE`
- `FAIL_TARGETED_GREEN`
- `FAIL_FULL_VALIDATION`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Then STOP for independent ChatGPT review.

Even after PASS, do not install/retest live, send Dashboard/Discord semantic traffic, replay/settle Task 233 manually, clean Task-223/Task-233 forensic evidence, or mutate public Release/tag/assets.
