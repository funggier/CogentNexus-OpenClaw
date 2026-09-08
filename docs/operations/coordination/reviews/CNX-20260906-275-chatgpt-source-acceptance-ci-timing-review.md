# CNX-20260906-275 — ChatGPT Source Acceptance and CI Timing Review

## Verdict

`ACCEPT_SOURCE_TEST_REPAIR__CI_TIMING_STABILITY_BLOCKS_DEPLOYMENT`

## Accepted source/test evidence

Task275 candidate `9d3000e3d8d09d712f621c1985d7bde66c2519ef` closes the remaining Discord Direct authority gaps from Tasks273-274.

Accepted production behavior:

- public `reply_payload_sending` fallback consumption now requires the current callback session key and trusted ingress surface to match the fallback owner/surface that armed the exact run;
- legacy Dashboard `channelId: webchat` compatibility is preserved;
- a pending durable `direct_result` suppresses legacy `recoverUndeliveredDirect` delegation even when the in-memory native-ownership marker is absent, preventing competing inference recovery after durable final capture.

Accepted Task275 production-shaped proofs:

1. wrong consume-time Discord owner cannot stage or start a waiter; the exact owner still stages and settles;
2. a public-hook waiter held across Delete/finalize cannot complete the deleted generation after stale release, while a genuinely recreated lifecycle can stage fresh work;
3. a durable final survives a later timeout scan, then exact settlement completes once and a second settlement is a no-op.

The focused Task275 suite passes 3/3, Tasks273-274 remain green, the local full plugin suite passes 61 files / 297 tests, and build/package/diff validation is green.

## Independent CI review

Exact candidate `9d3000e3d8d09d712f621c1985d7bde66c2519ef` has:

- PS5.1 Acceptance Smoke `34027500012`: success;
- Windows Installer Pack Smoke `34027500042`: success;
- Validate `34027500017`: failure on attempt 1 and the one bounded corrective rerun.

The two Validate failures are not stable on the same test:

- attempt 1: Windows 3.14 timed out in pre-existing `ticket-runtime.test.ts` (`dispatches nothing for a zero or invalid limit...`); Task275 tests passed;
- attempt 2: that ticket-runtime test passed, while Windows 3.11 timed out in pre-existing `v093-response-ready-boundary.test.ts`; Task275 tests again passed.

Attempt 2 shows broad runner slowdown rather than an isolated Task275 path regression: Python still passed 531 tests, but many SQLite-heavy Vitest files ran several times slower than the prior green candidate. The failing v093 test performs only three recovery scans. Task275's new recovery guard adds a read-only `SELECT 1 FROM cnx_assistant_delivery WHERE kind='direct_result' AND status='pending' LIMIT 1` per scan. On Task274 exact-SHA Validate `34016048105`, the same Windows 3.11 v093 test passed in about 0.30 seconds; on Task275 attempt 2 it exceeded the 15-second wall-clock timeout while surrounding tests were also strongly inflated.

This is strong evidence of Windows runner/Vitest timing instability, not evidence of a semantic Task275 defect. However, exact-SHA Validate is still objectively red. The acceptance gate must not be waived by classification alone.

## Decision

Task275 source/test repair is accepted and should be preserved. Live deployment/requalification remains blocked until a successor produces a fully green exact-SHA Validate candidate without blind retrying or masking a real defect.

Open Task276 to diagnose and stabilize the Windows Vitest timing boundary. Prefer deterministic test/harness isolation or evidence-backed targeted timeout policy over a blanket global timeout increase. Production semantics must remain unchanged unless new RED evidence proves a genuine production defect.

## Live authority

No install-over, Gateway/provider mutation, live session Delete/reset, Discord/Dashboard semantic send, Ticket/recovery disposition, manual SQLite mutation, Scheduled Task mutation, release promotion, or force push is authorized by this review.

Task272's previously granted Delete/test-message authority remains parked and unconsumed. A new cumulative install-over will require fresh explicit human authority after source/CI acceptance.
