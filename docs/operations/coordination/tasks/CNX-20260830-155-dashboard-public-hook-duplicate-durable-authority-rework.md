# CNX-20260830-155 — Dashboard Public-Hook Duplicate Durable Authority Rework

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `OFFLINE_REPOSITORY_TDD_PUBLIC_HOOK_DUPLICATE_DURABLE_AUTHORITY_REWORK`
Owner: ChatGPT
Executor: ChatGPT
Opened: 2026-08-30 ICT

## Objective

Repair the Task-154 public-hook fallback duplicate-safety defect using strict RED -> minimal GREEN -> full verification.

Task 154 established the correct fallback hook (`reply_payload_sending`) for production dispatchers that lack `appendBeforeDeliver`, but its first implementation returns early once fallback ownership is established. That early return bypasses durable marker/text authority on repeated callbacks.

No live Windows execution and no Dashboard semantic Send are authorized.

## Predecessor

Task-154 report:

`docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-154-dashboard-durable-capture-public-hook-repair-review.md`

Disposition: `REWORK`.

Reviewed production repair lineage:

- `e0182d89c91647e7070c2b95fc0b9b0fffc0378a`
- `4c5d2d3d0b5d49f47a31cbf49ee45d2b9e1a7c77`
- verification descendant `74732d847add15295265afc472ef3455ce89f3f3`

## Proven defect

The Task-154 fallback currently checks:

```ts
if (kind !== "final") return;
if (fallback.owned) return;
```

before routing repeated qualifying finals through `stageDashboardDirectResult(...)`.

Because OpenClaw falls back to the original payload when a `reply_payload_sending` hook returns no replacement payload, an already-owned repeated callback can bypass CogentNexus durable marker/text authority.

Consequences:

1. same-text repeat can reach native delivery without the durable marker-bearing text;
2. changed-text repeat bypasses the generation-bound durable text mismatch check instead of failing closed;
3. the existing regression proves only duplicate-row suppression, not duplicate delivery safety.

## Phase 1 — Genuine RED before production edit

Before changing production source, modify/add focused regression coverage against the current implementation and record a test-only commit SHA.

The RED must prove all of the following through the registered public hook path:

1. first qualifying `kind=final` callback stages one durable direct-result row and returns marker-bearing text;
2. second same-text callback for the same armed run/generation must return the same marker-bearing durable text, while durable row count remains exactly one;
3. second changed-text callback for the same armed run/generation must fail closed through the existing durable text-mismatch authority;
4. only one native-settlement waiter/pulse ownership sequence is started for the generation;
5. append-capable dispatcher behavior remains unchanged.

On the pre-fix implementation, assertions (2) and (3) must fail for the intended `fallback.owned` early-return reason, not because of fixture/setup errors.

Do not edit production code until the RED is observed in fresh CI/test output.

## Phase 2 — Minimal repair

Make the smallest source change in the owning fallback callback.

Required behavior:

- keep non-final filtering unchanged;
- do not bypass `stageDashboardDirectResult(...)` merely because the fallback already owns the generation;
- repeated same-text qualifying callbacks must reuse the idempotent durable authority and return its marker-bearing `nativeText`;
- repeated changed-text qualifying callbacks must reach the existing durable mismatch check and fail closed;
- worker pulse / native-settlement waiter creation must occur only on first ownership, never on repeated callbacks;
- existing append-capable `appendBeforeDeliver` path must remain behaviorally unchanged;
- delivery failure/recovery settlement and telemetry privacy must remain unchanged.

Avoid broad refactoring. Prefer separating "durable stage/re-observation" from "first-ownership waiter/pulse side effects" within the existing fallback path.

## Phase 3 — GREEN verification

At minimum verify:

1. focused new same-text repeat regression;
2. focused changed-text repeat fail-closed regression;
3. single waiter/pulse assertion;
4. existing Task-154 public-hook first-final regression;
5. append-capable path regressions;
6. `v091-dashboard-verified-delivery.test.ts` full file;
7. directly related response-ready/delivery boundary tests;
8. full plugin test suite;
9. `npm run build`;
10. `npm run plugin:validate`;
11. package verification as applicable;
12. `git diff --check`;
13. exact-repair-SHA GitHub Actions: Validate, Windows Installer Pack Smoke, PS5.1 Acceptance Smoke.

No success claim may rely only on the executor report; exact-SHA CI must be checked independently before Task-155 closeout.

## PASS boundary

`PASS` requires:

- genuine pre-production RED observed;
- same-text repeated public-hook callback returns the durable marker-bearing text without a second durable row;
- changed-text repeated callback fails closed through durable text authority;
- no second waiter/pulse ownership sequence is started;
- append-capable path unchanged;
- relevant/full tests, build, validation, package checks, diff check, and exact-SHA CI are GREEN;
- no live/runtime/Dashboard semantic mutation occurred.

Otherwise publish the narrowest truthful failure/blocker.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`

Include:

- exact RED commit SHA and failing assertion/output;
- exact production repair commit SHA;
- source-level explanation of the early-return defect;
- same-text marker reuse evidence;
- changed-text fail-closed evidence;
- single waiter/pulse evidence;
- append-path preservation evidence;
- complete relevant test/build/plugin/package results;
- exact CI run IDs/results;
- explicit confirmation of zero live Windows/runtime/Dashboard semantic mutation.

Then stop for independent review before any live install-over or Dashboard reacceptance.

## Hard fence

No Dashboard click/focus/type/paste/Send; no semantic transport; no live Windows/runtime mutation; no install/install-over/update/uninstall/reset/reinstall; no manual plugin/controller/database mutation; no OpenClaw source patch; no dependency upgrade; no unrelated refactor; no merge/tag/release; no force push.
