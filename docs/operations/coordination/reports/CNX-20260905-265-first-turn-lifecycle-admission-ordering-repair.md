# CNX-20260905-265 — First-Turn Lifecycle Admission Ordering Repair

## 1. Disposition

**PASS — source/test/CI repair complete; awaiting independent ChatGPT review.**

Task265 removes the first-turn race identified in the Task264 review. A new lifecycle B is now reconciled atomically at the registered `before_agent_run` boundary even when asynchronous `session_start(B)` has not yet run. No live runtime, semantic, installer, Gateway, database, release, or history-rewrite action was performed.

## 2. Authority and objective

- **Task:** `CNX-20260905-265`
- **Parent:** `CNX-20260905-264`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Starting remote HEAD:** `4abe1f511a2ee02352fca554f0b652e916d17c0f`
- **Parent candidate:** `cad96fad3d1cef07fac4173425f15714b33240d6`
- **Required behavior:** reconcile exact `ctx.sessionKey + ctx.sessionId` at first owner admission; preserve stale/different lifecycle rejection, idempotency, migration safety, and all existing generation fences.

## 3. Root cause

OpenClaw treats `session_start` as an asynchronous void observation hook. The lifecycle can be durably created and returned to the reply pipeline before the plugin's `session_start` callback completes. Task264's `before_agent_run` check was read-only and therefore observed deleted A instead of newly created B during this interval, blocking the legitimate first owner turn.

The race was confirmed by a registered-hook regression that tombstones A, registers the plugin, invokes `before_agent_run(B)` without invoking `session_start(B)`, and observes the Task264 baseline block.

## 4. TDD evidence

### RED

Test-only commit `f5f0c23` (`test: reproduce first-turn lifecycle ordering race`) added the actual registered-hook ordering regression. Against the Task264 baseline:

- focused suite: **10 tests, 1 failed**;
- failure occurred at the intended first-turn boundary: `before_agent_run(B)` was incorrectly classified as `cnxclaw_lifecycle_identity` block before `session_start(B)`;
- an initial Windows `EBUSY` cleanup issue was identified as test-harness resource leakage (unclosed read-only SQLite handle), fixed in the test before the final GREEN run; it was not treated as a product failure.

### Minimal fix

Production commit `ec1fdbb` (`fix: reconcile lifecycle before first owner turn`) changes `plugins/cogentnexus-openclaw/src/v090.ts` so the owner `before_agent_run` hook calls the existing transactional `reactivateSessionForLifecycle()` and decides from its `accepted` predicate. The same helper remains used by `session_start`.

This makes reconciliation and admission one atomic operation:

- deleted A + B activates B and increments generation once;
- repeated B is accepted without churn;
- A/C are rejected while B is active;
- NULL legacy identity binds deterministically without generation increment.

### GREEN

Focused command:

`npm test -- --run src/v090-session-ownership.test.ts`

Result: **1 file, 10/10 tests passed**.

The first-turn test proves B admission before any `session_start(B)`, exact active/B durable identity, stale A/C fail-closed behavior, delayed duplicate B idempotency, and unchanged generation.

## 5. Validation

- Full plugin suite: `npm test -- --run` → **58 files, 290/290 tests passed**
- TypeScript build: `npm run build` → passed; 43 dist text files canonicalized
- Plugin validation: `npm run plugin:validate` → passed
  - mixed-plugin artifact verification: PASS (`45` config properties, `5` tools)
  - ticket DB bootstrap: PASS (`9` required tables + v095 registration fence)
  - package verification: `result: ok`, `packedFileCount: 196`
- `git diff --check`: passed

## 6. Exact-SHA GitHub Actions

All required workflows completed successfully for the same candidate SHA:

`ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`

| Workflow | Run | Conclusion |
|---|---:|---|
| PS5.1 Acceptance Smoke | `33977733180` | success |
| Windows Installer Pack Smoke | `33977733182` | success |
| Validate | `33977733191` | success |

The Validate run included repository pytest, npm test, evaluation, audit, plugin validation, and package dry-run checks. A Node.js 20 deprecation annotation for upload-artifact was non-blocking and did not affect the conclusion.

## 7. Acceptance matrix

| Criterion | Verdict | Evidence |
|---|---|---|
| No row + B establishes active B and admits | PASS | shared transactional helper; existing lifecycle coverage |
| Deleted A + A rejected without mutation | PASS | focused 10/10 |
| Deleted A + B first owner turn admitted before session_start(B) | PASS | registered-hook ordering regression, focused 10/10 |
| Deleted A + B generation increments exactly once | PASS | durable row assertion in first-turn test |
| Active B + repeated B idempotent | PASS | focused lifecycle matrix and delayed session_start(B) assertion |
| Active B + stale A rejected | PASS | registered `before_agent_run` hook test |
| Active B + unrelated C rejected | PASS | registered `before_agent_run` hook test |
| Rejected lifecycle cannot mutate state/generation/session_id | PASS | durable identity assertion after stale A/C |
| Deleting row rejected | PASS | shared helper predicate and Task264 regression coverage |
| Legacy active NULL lifecycle binds deterministically without generation churn | PASS | focused migration test |
| Delayed/duplicate session_start(B) is idempotent | PASS | first-turn ordering test |
| Old Ticket/recovery/outbox/delivery/workflow/synthetic fences preserved | PASS | full 290/290 suite |
| Build/package/schema validation | PASS | build and plugin validation |
| Exact candidate CI | PASS | Actions runs 33977733180/182/191 |

## 8. Risk and residual uncertainty

The lifecycle identity decision is now fail-closed for stale, unrelated, deleted, deleting, missing, or missing-ID owner contexts, while the legitimate first new lifecycle can establish itself transactionally at the actual model-admission boundary. The existing legacy NULL compatibility behavior remains intentionally first-observed binding without generation churn.

Task265 still does not claim live Discord Delete → first message acceptance; live semantic and lifecycle actions remain outside the hard fence. Runtime-level OpenClaw behavior is represented by the registered-hook ordering test and exact CI, not by a live host action.

## 9. Hard-fence / side-effect ledger

```text
live OpenClaw session delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
manual live Ticket/session/SQLite mutation      = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Repository changes were limited to the test commit, production fix commit, and this report/state publication. All pushes were fast-forward only.

## 10. Reviewer verification packet

| # | Critical claim | Why it matters | Exact evidence | Suggested reviewer check |
|---:|---|---|---|---|
| 1 | First B owner turn reconciles before `session_start(B)` | Closes the user-visible first-turn race | `f5f0c23`, `ec1fdbb`, focused 10/10 | Inspect registered-hook ordering test and invoke it |
| 2 | `before_agent_run` uses one transactional lifecycle primitive | Prevents read/write ordering race | `ec1fdbb`, `v090.ts` | Verify hook calls `reactivateSessionForLifecycle` and uses `accepted` |
| 3 | Stale A/C remain fail-closed after B | Prevents lifecycle hijacking | focused 10/10 | Check durable row remains active/B after stale probes |
| 4 | Delayed duplicate `session_start(B)` is harmless | Covers asynchronous callback arriving after first turn | focused 10/10 | Inspect delayed callback assertion |
| 5 | Full plugin regressions remain green | Protects old generation/delivery/recovery fences | 58 files, 290/290 | Run full suite |
| 6 | Exact-SHA CI is green | Authoritative cross-platform evidence | Runs `33977733180`, `33977733182`, `33977733191` | Verify each run `headSha` equals candidate |

## 11. Publication state

- **Candidate/source SHA:** `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`
- **Report path:** `docs/operations/coordination/reports/CNX-20260905-265-first-turn-lifecycle-admission-ordering-repair.md`
- **Required next state:** `WAITING_FOR_CHATGPT_REVIEW`
- **Review owner:** ChatGPT

Hermes must not self-accept this report and performs no further Task265 mutation after publication.
