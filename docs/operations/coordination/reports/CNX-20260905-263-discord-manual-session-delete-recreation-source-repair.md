# CNX-20260905-263 — Discord Manual Session Delete/Recreation Source Repair

**Disposition:** `PASS_SOURCE_REPAIR__CI_GREEN__LIVE_ACCEPTANCE_REQUIRED`

**Repository:** `funggier/CogentNexus-OpenClaw`
**Branch:** `agent/v0.9.3-full-stabilization`
**Executor:** Luna
**Reviewer / next baton:** Musethree
**Task:** `CNX-20260905-263`

## Opening authority and exact candidate

Fresh remote authority was fetched before execution. The branch opened at
`d042a77a8b11aed6ff66051533c2ca8b317b9a3f`, with ACTIVE/STATUS
`READY_FOR_LUNA`, executor Luna, and Task263 source/test/docs-only authority.
The task explicitly forbade live OpenClaw session deletion/reset, semantic
messages, SQLite mutation, installer activity, Gateway lifecycle changes,
release/tag/default-branch changes, and force-push/history rewrite.

TDD execution used a fresh detached worktree and ended at exact remote
candidate:

`4a5907af212c0b8c6f913036c6853523d7bab872`

Ancestry was linear:

`4a5907a` <- `b920c5d` <- `d042a77`

- RED test commit: `b920c5d` — `test: cover Discord session recreation lifecycle`
- Production repair commit: `4a5907a` — `fix: reactivate fresh session lifecycle owners`
- `v090.ts` blob: `b42545dfa356696d5e4b3cae76a4dadda72fd383`
- `v090-session-ownership.test.ts` blob: `c2233cfbb666a6d89a1e23ecff00a9b3918643b4`
- Candidate worktree was detached, clean, and separate from this report checkout.

## Root cause

`cnx_sessions` tracked state and generation but not the OpenClaw lifecycle
identity (`sessionId`). The `session_start` hook called `sessionAuthority()`
and only warned when a row was tombstoned. Since `ensureSession()` uses
`INSERT OR IGNORE`, a deleted row remained deleted forever when a later
Discord lifecycle reused the same canonical `sessionKey`.

The delete path also did not persist the deleted lifecycle identity, so it
could not distinguish stale callbacks from a genuinely new lifecycle.

## Minimal repair

- Added migration-safe nullable `session_id` to `cnx_sessions`; existing
  databases gain the column through the existing `ensureColumn` path.
- Delete now records `event.sessionId` when available while preserving all
  existing cancellation, outbox suppression, recovery cancellation, workflow
  suppression, and synthetic-work cancellation behavior.
- Added `reactivateSessionForLifecycle(path, {sessionKey, sessionId})`:
  - a deleted row reactivates only for a different lifecycle identity;
  - generation advances exactly once;
  - repeated start for the same lifecycle is idempotent;
  - stale start for the deleted lifecycle cannot reopen the tombstone;
  - active rows are not hijacked by an unrelated lifecycle identity.
- Wired `session_start` to the lifecycle-aware helper and `session_end(deleted)`
  to persist the deleted lifecycle identity.
- No unrelated refactor and no live runtime change.

## TDD evidence

### RED

After bootstrapping dependencies in the fresh plugin checkout with
`npm ci --ignore-scripts`, the focused suite ran against the unmodified
production behavior plus the new regression:

- `6` existing tests passed.
- The new recreation test failed at the intended product boundary:
  `expected undefined to be type of 'function'` for the absent
  `reactivateSessionForLifecycle` helper.
- No fixture/setup error caused the failure.

A later assertion initially used a long-lived `TicketStore` connection and
returned `undefined` after an external connection committed the deletion.
That test-only harness issue was corrected to reopen SQLite read-only; it was
not treated as a product failure.

### GREEN

Focused command:

`npm test -- --run src/v090-session-ownership.test.ts`

Result: **1 test file, 7/7 tests passed**.

The regression covers deletion cancellation, fresh B reactivation, generation
advance, repeated B idempotency, stale A non-reactivation, old ticket
cancellation, fresh admission, and generation arithmetic. Existing same-key
reset, stop, delivery, synthetic, and cross-session tests remain green.

Broader local verification:

- `npm test`: **58/58 files, 287/287 tests passed**
- `npm run build`: passed; TypeScript compilation and dist canonicalization
- `npm run plugin:validate`: passed; schema/artifact checks, ticket DB bootstrap,
  and package-content verification
- `git diff --check`: passed

## Exact-SHA CI

Remote candidate `4a5907af212c0b8c6f913036c6853523d7bab872` was re-anchored
before inspection. GitHub Actions terminal results:

- `PS5.1 Acceptance Smoke` run `33968568428`: success
- `Windows Installer Pack Smoke` run `33968568349`: success
- `Validate` run `33968568357`: success

Exact candidate CI: **3/3 workflows successful**. The predecessor coordination
commit `d042a77` had an unrelated Validate failure before the repair; it is not
used as candidate evidence.

## Hard-fence ledger

```text
live OpenClaw sessions.delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
live Ticket/session/SQLite mutation              = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

No actual user Discord session was used to prove source behavior.

## Scope and handoff

Task263 source repair is accepted locally and has exact-SHA CI green evidence.
This report does **not** claim live lifecycle acceptance. A separate bounded
successor is required for the real web Delete -> later Discord message flow;
that successor must receive explicit authority for any real session deletion
and semantic Discord message. Until then, the stale recovery row remains
intentionally untouched because owner intent is unproven.

After publication, baton is handed to Musethree for independent review of the
source semantics, migration safety, idempotency, RED/GREEN evidence, and exact
candidate CI. No further live or semantic action is authorized by Task263.
