# CNX-20260906-275 — Discord Direct Owner Context and Stale Settlement Proof

## Disposition

`BLOCKED_CI_UNRESOLVED__WAITING_FOR_CHATGPT_REVIEW`

Task275 source/test work is locally GREEN and the Task275-specific proofs pass. Exact-SHA GitHub Actions are not fully green because the Validate workflow's Windows 3.11 matrix job timed out in unrelated pre-existing tests on both the first run and the one permitted corrective rerun. No live deployment or semantic/session mutation was performed.

## Authority and candidate

- Task: `CNX-20260906-275`
- Parent: `CNX-20260906-274`
- Executor: Hermes
- Candidate source/test commit: `9d3000e3d8d09d712f621c1985d7bde66c2519ef`
- Remote branch: `agent/v0.9.3-full-stabilization`
- Remote HEAD at source/test publication: `9d3000e3d8d09d712f621c1985d7bde66c2519ef`

## TDD evidence

A production-shaped RED was observed before the production repair:

- wrong canonical Discord session B consumed a fallback armed for session A/run R;
- the callback incorrectly returned a marked payload, proving the permissive consume-time behavior;
- the test required fail-closed behavior and no Ticket mutation.

The minimal source repair adds an explicit consume-time match for `ctx.sessionKey` and trusted ingress surface against the stored fallback owner/surface. Legacy Dashboard `channelId: webchat` compatibility was preserved after the full-suite regression exposed that production-shaped alias.

A second RED exposed a concrete timeout authority gap: a directly staged pending `direct_result` without the in-memory native ownership marker was delegated to legacy recovery, clearing response readiness before exact settlement. The minimal v091 wrapper guard now suppresses legacy recovery whenever any pending durable direct result exists.

## Task275 proof results

Focused file `src/v275-discord-owner-context-stale-settlement.test.ts`: **3 tests passed**.

1. Wrong consume-time owner/surface cannot stage or start a waiter; exact owner still stages and settles.
2. Registered public-hook waiter is held across Delete/finalize; stale release cannot complete the deleted generation, and a recreated lifecycle can stage a fresh Discord Direct Ticket.
3. A durable final survives a later timeout scan, then exact settlement completes once; repeated settlement is a no-op. The durable delivery row is `delivered`, `delivery_confirmed_at` is set, and exactly one `delivery_confirmed` plus one `completed` event exists.

Accepted regressions:

- Task273 `src/v273-discord-direct-delivery.test.ts`: passed.
- Task274 `src/v274-discord-receipt-lifecycle.test.ts`: passed.
- Legacy Dashboard fallback `src/v154-dashboard-public-hook-fallback.test.ts`: passed after preserving the `channelId: webchat` alias.

## Local validation

- Full plugin suite: `61 test files / 297 tests passed`
- TypeScript build: `PASS`
- mixed-plugin artifact verification: `PASS` (`45` config properties, `5` tools)
- ticket DB bootstrap: `PASS` (`9` required tables + v095 registration fence)
- package verification: `PASS` (`202` packed files)
- `git diff --check`: `PASS`

## Exact-SHA CI evidence

All listed runs are bound to candidate `9d3000e3d8d09d712f621c1985d7bde66c2519ef`.

| Workflow/run | Result | Evidence |
|---|---|---|
| PS5.1 Acceptance Smoke `34027500012` | success | completed on exact candidate SHA |
| Windows Installer Pack Smoke `34027500042` | success | completed on exact candidate SHA |
| Validate `34027500017`, first result | failure | Windows 3.14 first run timed out in existing `src/ticket-runtime.test.ts` test `dispatches nothing for a zero or invalid limit...`; `296 passed / 1 failed` |
| Validate `34027500017`, corrective rerun | failure | Windows 3.11 timed out in existing `src/v093-response-ready-boundary.test.ts` at 15s; `296 passed / 1 failed` |

The corrective rerun was performed once, on the same exact SHA, after recording the first failure. No third retry was performed. The Validate workflow is therefore not claimed as PASS.

## Changed paths in candidate

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `plugins/cogentnexus-openclaw/src/v275-discord-owner-context-stale-settlement.test.ts`

## Hard-fence ledger

- live Discord/Dashboard semantic sends: `0`
- live OpenClaw session Delete/reset: `0`
- manual live Ticket/session/SQLite mutation: `0`
- recovery replay/redelivery/disposition: `0`
- installer/install-over/uninstall/reset: `0`
- Gateway/provider/service lifecycle mutation: `0`
- Scheduled Task mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

Task272's parked live Delete/test-message authority remains unconsumed. This report does not authorize live deployment, requalification, another semantic turn, or session deletion.

## Handoff

The source/test evidence is ready for ChatGPT review, but the exact-SHA Validate gate is blocked by unrelated Windows matrix timeout instability. Set coordination state to `WAITING_FOR_CHATGPT_REVIEW` with disposition `BLOCKED_CI_UNRESOLVED__WAITING_FOR_CHATGPT_REVIEW`, and stop.
