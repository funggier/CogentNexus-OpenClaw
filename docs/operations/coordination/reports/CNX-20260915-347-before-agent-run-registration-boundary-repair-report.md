# CNX-347 — before_agent_run Registration Boundary Repair

## Status

**BLOCKED — no RED regression was reproduced; no production change was made.** Stop for independent ChatGPT review. This is not self-acceptance.

## Authority and baseline

- Repository: `funggier/CogentNexus-OpenClaw`
- Remote: `https://github.com/funggier/CogentNexus-OpenClaw.git` (GitHub remote inspected via `git remote -v`)
- Branch: `cnx-347-source-investigation`
- Task: `docs/operations/coordination/tasks/CNX-20260915-347-before-agent-run-registration-boundary-repair.md` (read from `origin/cnx-347-source-investigation`)
- Required baseline: `fce4e37b984d350969655ac22646edb89104b0eb`
- Remote branch HEAD inspected before this evidence commit: `aaa15f4312dd8dfe2cbf85d7d8038cd2d9a926a5`
- Lineage check: baseline is an ancestor of the remote branch (`git merge-base --is-ancestor`, exit 0)
- Task activation commit: `037ebf976e0558dc0baf9689b240c320043a626c`

This report and the focused diagnosis test are being committed and pushed to the same remote branch. They are not treated as evidence until the post-push remote ref and GitHub paths are verified.

## Source inspection

The requested chain was inspected:

`v091-release-entry.ts` → `v091-final-entry.ts` → `v090-final-entry.ts` → `v090-entry.ts` → `v090.ts` → canonical `index.ts`.

The canonical admission owner remains in `index.ts`:

- hook: `before_agent_run`
- priority: `2000`
- activation: `config.preInferenceAdmission !== false`
- Ticket-first behavior: guarded by `config.ticketFirst === true`

The release path passes the composed runtime API through the wrapper chain and reaches the canonical registration. `durableAdmissionEligible` was not changed.

Existing wiring tests inspected included `v091-wiring.test.ts` and `index.test.ts`.

## Regression test added

Added:

`plugins/cogentnexus-openclaw/src/cnx347-registration-boundary.test.ts`

It exercises the canonical `v091-release-entry` registration path with Host authority, `preInferenceAdmission=true`, and `ticketFirst=true`; it asserts exactly one `before_agent_run` registration at priority `2000` and verifies the effective handler returns the Ticket admission block.

## Focused execution

Command:

```text
npm test -- --run src/cnx347-registration-boundary.test.ts
```

Result:

```text
Test Files  1 passed (1)
Tests       1 passed (1)
```

The required RED state was not observed: the new regression test is already GREEN against the inspected source. Consequently, applying a production edit would not satisfy the evidence-first/TDD contract and would risk an unrelated semantic change.

## Production changes

None. In particular:

- `durableAdmissionEligible` unchanged.
- No provider, timeout, config, controller, runtime, database, or v0.9.5 history mutation.
- No duplicate admission path introduced.
- No force-push or history rewrite.

## Validation not run

Full suite, build, plugin validation, and complete duplicate-owner validation were intentionally not run after the RED prerequisite failed. They must not be represented as PASS.

## Fence accounting

- CNX-344 resend/replay: not performed.
- Live semantic request: not performed.
- UI interaction: not performed.
- Runtime/config/provider/database mutation: not performed.
- Install/restart/rebuild: not performed.
- v0.9.5 mutation: not performed.
- Manual/fallback provider dispatch: not performed.

## Review handoff

Independent ChatGPT review is required to determine whether the already-GREEN regression test is asserting the wrong boundary, whether a different effective runtime registration harness is required, or whether the source branch already contains the intended repair. No CNX-347 acceptance is claimed.
