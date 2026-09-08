# CNX-20260906-274 — Discord Direct Concurrent Receipt and Lifecycle Fence Completion

## Disposition

`PASS_SOURCE_TEST_CI__WAITING_FOR_CHATGPT_REVIEW`

Task274 closed the reviewed safety gaps in Task273 using RED -> minimal repair -> GREEN. No live Discord/Dashboard send, session Delete/reset, installer, Gateway/provider mutation, recovery action, or manual live database mutation was performed.

## Authority and exact candidate

- Task: `CNX-20260906-274`
- Parent: `CNX-20260906-273`
- Executor: Hermes
- Candidate commit: `35839a26673b35866334a36891a12d1c6d12e8ed`
- Remote branch: `agent/v0.9.3-full-stabilization`
- Remote HEAD after candidate publication: `35839a26673b35866334a36891a12d1c6d12e8ed`
- Evidence/test file: `plugins/cogentnexus-openclaw/src/v274-discord-receipt-lifecycle.test.ts`

## Repair

The generic `message_sent` handler previously inferred a missing `runId` from the newest run mapped to a session. That is unsafe for concurrent Discord Direct turns because the installed OpenClaw outbound contract does not guarantee a per-turn `runId` in the receipt.

The minimal repair now:

- recognizes canonical Discord owner session keys;
- refuses to infer a run from a runId-less Discord `message_sent` receipt;
- emits a categorical fail-closed observation;
- preserves exact-run settlement and existing Dashboard compatibility.

Task273's accepted exact owner/session/generation durable staging path is unchanged.

## TDD evidence

### Concurrent receipt RED -> GREEN

The registered-hook production-shaped test creates two Direct runs sharing one canonical Discord session, stages both exact durable final rows, and delivers a receipt with no `runId`. Before the repair, the handler proceeded into newest-run inference; the RED assertion required an explicit ambiguous-receipt fail-closed observation. After the repair, the test passes and confirms neither Ticket is settled by the ambiguous receipt.

The test also exercises the registered `before_agent_run` and `message_sent` hooks, exact owner session key, two distinct run IDs, and durable Ticket rows. No `message_sent.runId` is fabricated.

### Lifecycle/generation proof

The test stages a Discord Direct final at generation `0`, deletes/finalizes the session, and proves:

- the pending assistant delivery is suppressed by the session boundary;
- a late old-generation staging attempt returns `staged: false`;
- lifecycle recreation produces the contract's actual generation `2` after delete/finalize;
- a fresh Ticket on the recreated canonical key stages with generation `2`.

The generation value is recorded from the live lifecycle primitive rather than normalized to an assumed increment.

### Timeout-boundary proof

A Discord-staged durable final was passed through the timeout/recovery scan using a later timestamp. The test was already GREEN without additional production changes because the existing v091/v092 durable-delivery guard excludes a Ticket that already owns a durable `direct_result` row. It verifies:

- timeout scan returns no competing recovery;
- the Ticket remains accepted;
- the durable final remains authoritative.

Existing suites continue to cover Dashboard Direct semantics, Discord `NO_REPLY`, exact idempotency/mismatch behavior, session ownership, recovery, and native delivery boundaries.

## Validation

Focused Task274 suite:

- `src/v274-discord-receipt-lifecycle.test.ts`: `2 passed` in the final focused run before the timeout proof was added; `3 passed` after adding the timeout proof.

Full plugin suite after final changes:

- Test files: `60 passed`
- Tests: `294 passed`

Local build/package checks:

- TypeScript build: `PASS`
- mixed-plugin artifact/schema verification: `PASS` (`45` config properties, `5` tools)
- ticket DB bootstrap: `PASS` (`9` required tables + v095 registration fence)
- package verification: `PASS` (`200` packed files)
- `git diff --check`: `PASS`

Exact-SHA GitHub Actions for candidate `35839a26673b35866334a36891a12d1c6d12e8ed`:

| Workflow | Run ID | Head SHA | Result |
|---|---:|---|---|
| Validate | `34016048105` | `35839a26673b35866334a36891a12d1c6d12e8ed` | `success` |
| PS5.1 Acceptance Smoke | `34016048117` | `35839a26673b35866334a36891a12d1c6d12e8ed` | `success` |
| Windows Installer Pack Smoke | `34016048133` | `35839a26673b35866334a36891a12d1c6d12e8ed` | `success` |

## Changed paths

- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/v274-discord-receipt-lifecycle.test.ts`

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

Task272's parked live Delete/test-message authority remains unconsumed. Task274 is source/test/CI evidence only and does not authorize live deployment or acceptance.

## Handoff

Set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop. A separately reviewed successor authority is required before deployment/requalification or any use of Task272's parked live authority.
