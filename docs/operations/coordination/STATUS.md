# Coordination Channel Status

**State:** `IN_PROGRESS_CHATGPT`  
**Execution mode:** `OFFLINE_REPOSITORY_TDD_PUBLIC_HOOK_DUPLICATE_DURABLE_AUTHORITY_REWORK`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 154 is independently `REWORK` and authorizes only the narrow offline duplicate-safety repair  
**Execution trigger:** direct ChatGPT repository work; no Hermes/live execution authorized by Task 155

## Active work

Task:

[`tasks/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`](tasks/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md)

Task ID:

`CNX-20260830-155`

## Task-154 review result

Task-154 report:

`docs/operations/coordination/reports/CNX-20260830-154-dashboard-durable-capture-public-hook-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-154-dashboard-durable-capture-public-hook-repair-review.md`

Disposition: **REWORK**.

The public-hook fallback architecture is retained, but duplicate re-observation is unsafe because current code returns at `fallback.owned` before durable authority is consulted again.

This means:

- repeated same-text final can fall back to OpenClaw's original unmarked payload;
- repeated changed-text final can bypass CogentNexus durable mismatch fail-closed behavior;
- duplicate-row suppression alone is insufficient proof of duplicate delivery safety.

## Task-155 TDD gate

Before production code changes, a test-only RED commit must prove both defects against current code:

1. same-text repeat must be required to return the same marker-bearing durable payload while row count stays one;
2. changed-text repeat must be required to fail closed through durable text mismatch;
3. only one settlement waiter/pulse ownership sequence may start;
4. append-capable behavior must remain unchanged.

After RED, make only the minimum fallback change needed to reuse idempotent durable staging on repeat callbacks while guarding first-ownership side effects.

## Verification gate

Focused regressions first, then directly affected delivery tests, full plugin tests, build, `plugin:validate`, package verification, `git diff --check`, and exact-SHA GitHub Actions including Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke.

## Required output

ChatGPT must publish:

`docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`

Then stop for independent review.

## Release / live fence

Phase P remains FAIL. No Dashboard semantic Send, Windows install-over, lifecycle mutation, Phase Q, merge, tag, GitHub Release, or promotion is authorized by Task 155. No force push.
