# CNX-20260905-259 — Task258 Stale-Owner Recovery Disposition Contract Repair

Status: `REPAIRED_STALE_OWNER_RECOVERY_CONTRACT__NEW_CANDIDATE_REVIEW_REQUIRED`

## Authority and ancestry

- Opening authority: Task259 `READY_FOR_HERMES`, fetched from GitHub before work.
- Opening source HEAD: `fad7dbb98b9238bad00dcf2c1ba43fc0de949c32`.
- Required review ancestor `500f74d3c6b00de0add6311f75d784b0d45f1dfd`: verified with `git merge-base --is-ancestor` (exit 0).
- Task258 forensic report: `f44cf675bcbd9e6944cd6635861236637f3eb22f`.
- Task258 review commit: `500f74d3c6b00de0add6311f75d784b0d45f1dfd`.
- Subject Ticket: `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`.
- Baseline reference inspected: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`; it only changes streaming evidence PID binding and contains no compliant stale-owner disposition contract.

## Root cause findings

### Liveness

`src/v091-direct-recovery.ts` selected pending recovery when the Ticket was accepted, workflow-ineligible, the session was `active`, and generation matched. It did not require `cnx_sessions.updated_at` freshness. Therefore a durable `active` row with stale owner evidence remained automatically emittable indefinitely; `nextDirectRecoveryWakeMs()` also continued to arm a wake for it.

Repair: `DIRECT_RECOVERY_SESSION_LIVENESS_MS = 15 minutes` and a parameterized `updated_at` freshness fence are now applied to both `dueDirectRecovery()` and pending recovery wake selection. Legacy minimal test schemas without `updated_at` retain compatibility; production schema has the column. Stale durable state is not treated as fresh owner intent.

### Disposition

The existing `cancelSessionByKey()` / `cancelSessionTickets()` path was not compliant: it resolves an owner session and cancels all non-terminal Tickets for that session, rather than binding exact Ticket and owner generation. It also couples session cancellation with broad outbox suppression. No exact-ticket, auditable, idempotent product disposition API existed.

Repair: `disposeDirectRecoveryTicket()` was added to `src/v090.ts`. It requires exact `ticketId`, `ownerSessionKey`, and `ownerGeneration`; requires an existing recovery row; performs one immediate transaction; marks only the exact Ticket and recovery row cancelled; clears only that Ticket's pending outbox/assistant-delivery rows; writes one `direct_recovery_dispositioned` event; and returns an idempotent already-dispositioned result on repeat. It has no workflow execution, resend, replay, session-generation mutation, or semantic-send side effect. The exact recovery predicate is false after the transition.

## TDD evidence

- RED regression added before production implementation: exact disposition test failed because `disposeDirectRecoveryTicket` did not exist (after dependency installation, the only initial cleanup issue was a test-held SQLite connection, corrected in fixture lifecycle).
- Liveness regression added for a demonstrably stale `active` session.
- Targeted GREEN command:
  `npm test -- --run src/v090.test.ts src/v091-direct-recovery.test.ts src/v091-host-stall-contract.test.ts`
  Result: exit 0; 3 files, 12 tests passed.
- Full GREEN command:
  `npm test`
  Result: exit 0; 58 files, 286 tests passed.
- Build/schema command:
  `npm run plugin:build`
  Result: exit 0; TypeScript build passed, 43 dist text files canonicalized, mixed-plugin artifact verification PASS (45 config properties, 5 tools).
- Earlier package validation also passed: ticket DB bootstrap PASS (9 required tables + v095 registration fence), package contents PASS (196 packed files).

## Changed paths

- `plugins/cogentnexus-openclaw/src/v090.ts`
- `plugins/cogentnexus-openclaw/src/v090.test.ts`
- `plugins/cogentnexus-openclaw/src/v091-direct-recovery.ts`
- `plugins/cogentnexus-openclaw/src/v091-direct-recovery.test.ts`
- `plugins/cogentnexus-openclaw/src/v091-host-stall-contract.test.ts` (fixture now records fresh owner liveness for its positive contract).
- This report.

## Effect ledger and hard fences

No live installation, live database, subject recovery row, Gateway process, installer/Scheduled Task, Dashboard/Discord/API send, recovery execution, replay, resend, release/tag mutation, or force push was performed. All live hard-fence counts are **0**. All database mutations occurred only in temporary Vitest fixtures under the system temp directory.

Transient/non-product issues observed: first test command from repository root failed with missing root `test` script (exit 1); fresh clone initially lacked `node_modules` and required `npm install --ignore-scripts`; one Windows SQLite fixture cleanup hit `EBUSY` until the test connection was explicitly closed. None affected the final product result.

## Candidate consequence and final disposition

Because production source changed, baseline `6822af4…` is no longer an executable candidate for any later live install-over. The post-repair commit below is a new candidate requiring independent review, authoritative CI, exact SHA binding, and fresh Windows proof before any successor action.

Final disposition: **`REPAIRED_STALE_OWNER_RECOVERY_CONTRACT__NEW_CANDIDATE_REVIEW_REQUIRED`**.

Task259 stops here for independent review. No live successor, recovery, cancellation, installer, Gateway restart, or semantic acceptance action was opened or executed.
