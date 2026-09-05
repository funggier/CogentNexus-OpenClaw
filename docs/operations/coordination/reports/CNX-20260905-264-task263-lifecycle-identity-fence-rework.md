# CNX-20260905-264 — Task263 Lifecycle Identity Fence Rework

## 1. Disposition

**PASS — source/test/CI repair complete; awaiting independent ChatGPT review.**

Task264 closes the Task263 lifecycle-identity defect without live runtime, semantic, installer, Gateway, database, release, or history-rewrite side effects. The exact candidate `cad96fad3d1cef07fac4173425f15714b33240d6` passed focused and full local validation plus all three exact-SHA branch workflows.

## 2. Objective and acceptance contract

- **Task:** `CNX-20260905-264`
- **Parent:** `CNX-20260905-263`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Starting remote HEAD:** `89e3fef3e935c98231f8198e2ea81b1ff2852b0e`
- **Task baseline:** Task263 candidate `4a5907af212c0b8c6f913036c6853523d7bab872` plus coordination commits
- **Required result:** exact lifecycle identity acceptance/rejection, `before_agent_run` fail-closed enforcement using `ctx.sessionKey + ctx.sessionId`, migration-safe NULL behavior, and no regression of existing generation/delivery/recovery fences.

Hard fences were source/test/docs/CI only. All prohibited live and destructive action counts remained zero.

## 3. Investigation and root cause

The Task263 helper `reactivateSessionForLifecycle()` treated every non-deleted owner row as acceptable. After lifecycle A was deleted and lifecycle B became active, a later A or unrelated C therefore received `{state: "active"}` without an explicit acceptance signal. The `session_start` path only inspected `state`, and the OpenClaw owner run boundary had no exact `ctx.sessionId` comparison.

The required OpenClaw hook context is available at the actual registration boundary in `v090.ts`; the repair therefore keeps the canonical `sessionKey` and adds an exact stored `session_id` comparison rather than inferring identity from state or prompt text.

## 4. Implementation

### RED

Test-only commit `9b332dc` (`test: fence recreated session lifecycle identities`) added the stale/deleted/current/unrelated lifecycle assertions, legacy NULL coverage, and an actual registered `before_agent_run` hook test. Against the unmodified Task263 production code:

- focused suite: **7 tests, 1 failed**;
- failure was the intended product boundary: stale A returned `state: "active", generation: 2` instead of the required explicit rejected result `{accepted:false,lifecycleMatches:false}`;
- no setup or fixture error caused the RED.

### Minimal production repair

Production commit `cad96fa` (`fix: enforce current lifecycle identity at run boundary`) changes only `plugins/cogentnexus-openclaw/src/v090.ts`:

- `reactivateSessionForLifecycle()` now returns `accepted`, `lifecycleMatches`, and current `sessionId` evidence;
- deleted A + A is rejected without reopening;
- deleted A + new B activates exactly once and increments generation once;
- active B + B is accepted idempotently;
- active B + stale A/C is rejected without mutation;
- active legacy `session_id IS NULL` binds the observed lifecycle deterministically without generation increment;
- `before_agent_run` blocks owner contexts whose `ctx.sessionKey + ctx.sessionId` do not identify the current active lifecycle;
- `session_start` returns the same fail-closed lifecycle-identity block for rejected callbacks;
- existing ticket, recovery, outbox, assistant delivery, workflow, and synthetic generation fences are untouched.

## 5. Files changed

Only these source/test files changed relative to the starting HEAD:

- `plugins/cogentnexus-openclaw/src/v090.ts`
- `plugins/cogentnexus-openclaw/src/v090-session-ownership.test.ts`

Coordination report/state files are added/updated in the publication commit after this candidate validation.

## 6. Validation evidence

### Focused GREEN

`npm test -- --run src/v090-session-ownership.test.ts`

- **1 file, 9/9 tests passed**
- Covers deleted A + A rejection, deleted A + B recreation, repeated B idempotency, active B + A/C rejection, identity immutability, legacy NULL binding, actual `before_agent_run` stale/current behavior, and existing delivery/generation behavior.

### Full GREEN and package checks

- `npm test -- --run`: **58 files, 289/289 tests passed**
- `npm run build`: passed; TypeScript compilation and dist canonicalization (`43` dist text files)
- `npm run plugin:validate`: passed
  - mixed-plugin artifact verification: PASS (`45` config properties, `5` tools)
  - ticket DB bootstrap: PASS (`9` required tables + v095 registration fence)
  - package verification: `{result:"ok", packedFileCount:196}`
- `git diff --check`: passed
- Local worktree was clean after excluding no files; watcher logs were removed and not committed.

## 7. Exact-SHA GitHub Actions

All required workflows were terminal success for the same exact candidate SHA `cad96fad3d1cef07fac4173425f15714b33240d6`:

| Workflow | Run | Conclusion |
|---|---:|---|
| PS5.1 Acceptance Smoke | `33976180547` | success |
| Windows Installer Pack Smoke | `33976180585` | success |
| Validate | `33976180571` | success |

No watcher timeout or unrelated SHA is used as candidate evidence.

## 8. Acceptance matrix

| Criterion | Verdict | Evidence |
|---|---|---|
| Deleted A + A rejected | PASS | focused 9/9; `v090-session-ownership.test.ts` |
| Deleted A + genuinely new B accepted once | PASS | focused 9/9; generation/session identity assertions |
| Active B + repeated B idempotent | PASS | focused 9/9; unchanged generation assertion |
| Active B + stale A rejected | PASS | focused 9/9; explicit `accepted:false` |
| Active B + unrelated C rejected | PASS | focused 9/9; explicit `accepted:false` |
| Rejected lifecycle cannot mutate state/generation/session_id | PASS | final read-only identity row assertion plus focused test |
| `before_agent_run` uses session key + lifecycle ID and fails closed | PASS | actual registered-hook test; category `cnxclaw_lifecycle_identity` |
| Current B owner run remains admitted | PASS | actual registered-hook test; no lifecycle block for B |
| Legacy active NULL migration behavior deterministic | PASS | focused 9/9; binds ID with unchanged generation |
| Old Ticket/recovery/outbox/delivery/workflow/synthetic fences preserved | PASS | existing full suite 289/289 and focused regression |
| Reset/new/session succession regressions | PASS | full suite 58/58 |
| TypeScript/build/package/workflow validation | PASS | build, plugin validate, exact-SHA Actions 3/3 |

## 9. Risk and residual uncertainty

The repair is fail-closed for missing, stale, unrelated, deleting, or deleted lifecycle identities at the owner run boundary. A legacy active row with NULL identity is intentionally bound to the first observed lifecycle through the existing lifecycle-start path without generation churn; the focused test proves deterministic behavior, but historical databases cannot prove which lifecycle originally owned such a row before binding. No live database was inspected or mutated under this task.

The `session_start` return object is aligned with the existing OpenClaw hook outcome convention used by the plugin; ChatGPT should independently verify the host's handling of a blocking `session_start` result if runtime-level acceptance is later authorized. Task264 does not claim live hook execution.

## 10. Hard-fence / side-effect ledger

```text
live OpenClaw session delete/reset              = 0
live Discord/Dashboard semantic messages        = 0
manual live Ticket/session/SQLite mutation      = 0
installer/install-over/uninstall/reset           = 0
Gateway stop/start/restart                       = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Repository effects were limited to two commits for source/test work and the report/state publication commit. Pushes were fast-forward only.

## 11. Reviewer verification packet

| # | Critical claim | Why it matters | Exact evidence | Suggested reviewer check |
|---:|---|---|---|---|
| 1 | Stale/different active lifecycle is explicitly rejected | Prevents stale owner admission and identity hijack | `cad96fa`, `v090.ts` `reactivateSessionForLifecycle` | Inspect active-row predicate and returned `accepted` field |
| 2 | Owner run is fail-closed on lifecycle mismatch | Prevents model execution under stale OpenClaw lifecycle | `cad96fa`, `v090.ts` `before_agent_run` | Invoke/check hook with same key and A/B IDs |
| 3 | RED caught the exact Task263 defect | Proves regression was not written after a passing fix | `9b332dc`; focused RED 7 tests/1 failure | Re-run parent tree test or inspect failure boundary |
| 4 | Focused lifecycle matrix is green | Proves required identity cases | 9/9 focused test result | Run `npm test -- --run src/v090-session-ownership.test.ts` |
| 5 | No broad regressions | Protects old generation/delivery/recovery behavior | 58 files, 289/289 | Run full plugin test suite |
| 6 | Candidate passed authoritative CI | Binds Windows/validation evidence to exact source | Runs `33976180547`, `33976180585`, `33976180571` | Query each run and verify `headSha` exactly |

## 12. Publication state

- **Candidate/source exact SHA:** `cad96fad3d1cef07fac4173425f15714b33240d6`
- **Publication report path:** `docs/operations/coordination/reports/CNX-20260905-264-task263-lifecycle-identity-fence-rework.md`
- **Publication commit:** recorded after the report/state update
- **Required next state:** `WAITING_FOR_CHATGPT_REVIEW`
- **Review owner:** ChatGPT

Hermes does not self-accept this report and performs no further Task264 mutation after publication.
