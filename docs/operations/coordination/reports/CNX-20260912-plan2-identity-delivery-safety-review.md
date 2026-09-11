# CNX-20260912 — Plan 2 Identity / Delivery Safety Review

Date: 2026-09-12
Repository: `funggier/CogentNexus-OpenClaw`
PR: #30 — `v0.9.5 Plan 2 — session generation contract`
Branch: `agent/v0.9.5-plan2-delivery-session-identity`
Reviewed head: `d6559d21faea18e29a45b6bd55e5215edcf54610`
Base: `main` / `1e81b3cb9a8fe31a8e4df90563f15a3cde255c59`

## Validation evidence

All four required exact-head GitHub Actions workflows completed successfully for `d6559d21faea18e29a45b6bd55e5215edcf54610`:

- Validate #4024 / run `34624369169` — success
- PS5.1 Acceptance Smoke #2911 / run `34624369213` — success
- PS5.1 Live Runner Smoke #839 / run `34624369080` — success
- Windows Installer Pack Smoke #2902 / run `34624369150` — success

Validate completed the repository matrix successfully, including `npm test`, `npm run evaluation`, `npm audit --omit=dev`, `npm run plugin:validate`, Python pytest, namespace isolation, and Windows lifecycle checks where applicable.

## Review findings

### 1. Inference-attempt stale-owner fencing — PASS

`bindRunId()` now verifies that the attempt is active and that its owner session is still active at the exact recorded generation before binding a RunID. `finishInferenceAttempt()` applies the same current-generation fence before ending an attempt.

This closes the previously identified stale-generation binding path.

### 2. Canonical Delivery Core stale-owner fencing — PASS

`stageDelivery()`, `acceptTransport()`, and `confirmDelivery()` verify the current owner generation. The idempotent `transport_accepted` and `confirmed` return paths also perform the owner check rather than returning stale rows silently.

The dedicated regression tests cover stale generation on both idempotent transport acceptance and idempotent confirmation.

### 3. Web Chat / Discord exact correlation — PASS

Both adapters require exact run/session correlation, reject ambiguous run or inference matches, derive the delivery identity from the canonical Ticket + inference attempt + RunID + owner generation chain, and reject stale session generations before settlement.

Missing exact identity is treated as non-settling evidence.

### 4. Persistent idempotency authority — PASS

`cnx_assistant_delivery.idempotency_key` remains a unique durable key in the existing Ticket database schema. The Plan 2 Delivery Core reuses that authority rather than creating a second delivery store.

### 5. Remaining architectural gap: `sessionId` is not carried by canonical attempt/delivery identity — OPEN

The approved v0.9.5 architecture defines physical lifecycle identity as:

`sessionKey + sessionId + generation`

and explicitly distinguishes the physical OpenClaw session incarnation from the logical session key. The durable `cnx_sessions` table already stores `session_id`, and lifecycle checks can validate it.

However, the current Plan 2 `InferenceAttempt` identity carries:

`sessionKey + sessionGeneration`

and the canonical `DeliveryAttempt` identity carries:

`ownerSessionKey + ownerGeneration`

without persisting the authoritative `sessionId` alongside those records.

This matters because genuine session recreation after deletion intentionally reuses the tombstoned generation. Therefore, generation alone is not a complete physical-incarnation discriminator when the same `sessionKey` is recreated with a different `sessionId`.

Current tests and exact-head CI prove generation fencing, but they do not prove the stronger contract:

> stale work from the previous `sessionId` cannot be accepted by a recreated physical session that reuses the same generation.

## Decision

Plan 2 CI is green at the reviewed head, but the architecture review is **not merge-ready** until the `sessionId` identity gap is either:

1. explicitly incorporated into the canonical inference/delivery identity and covered by regression tests; or
2. formally proven unnecessary by a stronger existing invariant that is documented and tested at the same boundary.

No release/tag/public-version mutation was made by this review.
