# CNX-20260906-274 — ChatGPT Discord Direct Safety Completion Review

## Verdict

`REWORK_REQUIRED__OWNER_CONTEXT_AND_STALE_SETTLEMENT_PROOFS_INCOMPLETE`

## Accepted evidence

Task274 candidate `35839a26673b35866334a36891a12d1c6d12e8ed` correctly repairs the concrete same-session outbound receipt ambiguity found in Task273 review.

The production change is intentionally narrow: for a canonical Discord owner session, a `message_sent` receipt without exact `runId` is ignored rather than inferred from the newest `runSessions` entry. This removes the unsafe `candidates.at(-1)` authority for runId-less Discord receipts while preserving non-Discord compatibility and exact-run settlement.

The Task274 regression also proves two concurrent Direct runs on the same Discord session remain accepted after an ambiguous no-runId receipt, and the exact candidate passed all required GitHub Actions:

- Validate `34016048105` — success;
- PS5.1 Acceptance Smoke `34016048117` — success;
- Windows Installer Pack Smoke `34016048133` — success.

The lifecycle helper-level evidence is also directionally correct: deletion suppresses a pending assistant delivery, late staging for the cancelled old run fails, lifecycle recreation advances to generation 2 in the tested sequence, and a fresh Direct Ticket stages at generation 2. The Discord durable timeout scan also remains non-promoting while a durable row exists.

## Blocking finding 1 — wrong callback owner/context consumption remains unproven and source is permissive

Task274 explicitly required that a wrong canonical session key / wrong owner context cannot arm or consume another run's public-hook fallback.

The current `reply_dispatch` arming path checks the Discord owner session when the fallback is created. However `reply_payload_sending` later resolves the fallback by `runId` and stages using the stored `fallback.sessionKey` / `fallback.ingressSurface`; it does not independently require the consuming callback's current `ctx.sessionKey` and trusted ingress surface to match the stored owner.

Therefore the exact required negative case is absent and the source does not yet demonstrate an explicit consume-time owner fence. The successor must create a RED test where a fallback is armed for session A/run R and a `reply_payload_sending` callback carrying the same run R but session B/wrong surface attempts consumption. It must not stage, mark, start a waiter, or alter A's Ticket. If that test is RED, add only the smallest consume-time owner/surface guard.

## Blocking finding 2 — stale native waiter after Delete is not directly exercised

Task274 required: stage generation N, delete/reset before native waiter settles, then release the stale waiter and prove it cannot complete the cancelled old Ticket.

The submitted test stages via the helper, deletes the session, and retries staging. It does not arm the registered public-hook waiter, hold `waitForIdle`, delete while the waiter is pending, release that stale waiter, and assert the old Ticket remains cancelled with no recreated delivery.

Source inspection suggests the current transaction should fail closed because deletion cancels the Ticket and removes pending assistant delivery while settlement requires an accepted Ticket joined to a pending delivery row. That is promising but must be proven through the production-shaped hook/waiter path before live acceptance.

## Blocking finding 3 — timeout test stops before required later exact settlement

Task274 required a staged Discord final to survive a later timeout scan and then settle exactly once. The submitted timeout test proves only the first half: no promotion and Ticket remains accepted. It does not call the exact settlement path afterward and prove one completion / one delivered row / no duplicate terminal transition.

This is likely test completion rather than a production defect, but it remains an explicit completion criterion.

## TDD note

Task274 production and tests are again contained in one candidate commit. The task did not require a separate RED commit, so this review does not reject on commit shape alone. Task275 must preserve observable RED evidence before any further production mutation.

## Live authority

No live deployment or semantic/session mutation is authorized by this review. Task272's parked Delete/test-message authority remains unconsumed. Do not install, restart, Delete, send, replay, redeliver, dispose, or mutate live Ticket/SQLite state until Task275 is independently accepted and a successor live task is explicitly authorized.
