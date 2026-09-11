# CNX-20260912 — Plan 2 Identity / Delivery Safety Review

Date: 2026-09-12
Repository: `funggier/CogentNexus-OpenClaw`
PR: #30 — `v0.9.5 Plan 2 — session generation contract`
Implementation head: `27e7f02af4556f9cd4ceede0c53122ce039ecdd0`
Merged main: `52617e55e9ab3b8aa3fe5c5c2ce71a305c43954c`

## Validation evidence

The final Plan 2 implementation head passed all four required exact-head GitHub Actions workflows:

- Validate #4030 / run `34625800173` — success
- PS5.1 Acceptance Smoke #2917 / run `34625800234` — success
- PS5.1 Live Runner Smoke #842 / run `34625800226` — success
- Windows Installer Pack Smoke #2908 / run `34625799984` — success

The Validate matrix included repository tests, `npm test`, `npm run evaluation`, `npm audit --omit=dev`, `npm run plugin:validate`, Python pytest, namespace isolation, and applicable Windows lifecycle checks.

## Review findings

### 1. Inference-attempt stale-owner fencing — PASS

`bindRunId()` verifies that the attempt is active and that its owner session is still active at the exact recorded generation before binding a RunID. `finishInferenceAttempt()` applies the same current-generation fence before ending an attempt.

The final regression suite additionally covers the delete/recreate boundary: stale work created under physical session S1 cannot bind or finish after S2 is recreated on the same `sessionKey` using the tombstoned generation.

### 2. Canonical Delivery Core stale-owner fencing — PASS

`stageDelivery()`, `acceptTransport()`, and `confirmDelivery()` verify the current owner generation. The idempotent `transport_accepted` and `confirmed` return paths also perform the owner check rather than returning stale rows silently.

Dedicated regression tests cover stale generation on both idempotent transport acceptance and idempotent confirmation.

### 3. Web Chat / Discord exact correlation — PASS

Both adapters require exact run/session correlation, reject ambiguous run or inference matches, derive delivery identity from the canonical Ticket + inference attempt + RunID + owner generation chain, and reject stale session generations before settlement.

Missing exact identity is treated as non-settling evidence.

### 4. Persistent idempotency authority — PASS

`cnx_assistant_delivery.idempotency_key` remains the unique durable key in the existing Ticket database schema. The Plan 2 Delivery Core reuses that authority rather than creating a second delivery store.

### 5. Earlier `sessionId` identity concern — FORMALLY DISCHARGED

The earlier review noted that canonical inference/delivery rows persist `sessionKey + generation` rather than duplicating `sessionId`. That concern is resolved by the stronger existing lifecycle invariant rather than by adding a second identity field to every downstream row.

The authoritative sequence is:

1. Physical lifecycle S1 begins at generation 0 and owns its authoritative `cnx_sessions.session_id`.
2. Physical deletion advances the durable generation to 1 before tombstoning S1.
3. Genuine recreation as S2 on the same `sessionKey` reuses tombstoned generation 1 rather than incrementing again.
4. Any stale S1 work still carries generation 0.
5. Inference bind/finish and Delivery Core owner checks compare recorded generation against the currently active `cnx_sessions` generation and fail closed for stale work.
6. Regression coverage in `v095-inference-attempt.test.ts` creates S1 work, deletes S1, recreates S2, confirms generation reuse, and proves the old work cannot bind or finish or create a fresh Run lookup.

Thus, the absence of duplicated `sessionId` in downstream records does not permit prior-session evidence to cross the recreated physical-session boundary under the tested invariant. `cnx_sessions` remains the sole durable lifecycle authority.

## Decision

Plan 2 identity and delivery safety review is **PASS / CLOSED**.

The architecture gap was formally discharged using the existing durable generation fence and dedicated delete/recreate regression proof. No additional session store or redundant lifecycle authority was introduced.

PR #30 was subsequently merged by explicit operator authorization into `main` as merge commit `52617e55e9ab3b8aa3fe5c5c2ce71a305c43954c`.

## Post-merge status note

Push-triggered Actions were dispatched for merge commit `52617e55e9ab3b8aa3fe5c5c2ce71a305c43954c`. At closeout verification, PS5.1 Acceptance Smoke #2918 and Windows Installer Pack Smoke #2909 were successful; Validate #4031 was still running at the time of the check. The available connector did not independently expose a post-merge Live Runner result at that moment.

This report therefore records the verified pre-merge gate and the observed post-merge status without claiming a complete post-merge four-workflow green result.

No release/tag/public-version mutation was made by this review.
