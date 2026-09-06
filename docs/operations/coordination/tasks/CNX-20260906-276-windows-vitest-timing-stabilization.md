# CNX-20260906-276 — Windows Vitest Timing Stabilization and Exact-SHA Gate Closure

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-275`
Executor: `Hermes`
Reviewer: `ChatGPT`

## Objective

Preserve the accepted Task275 Discord Direct source semantics while closing the remaining exact-SHA Validate blocker caused by unstable Windows Vitest wall-clock timing. Produce a candidate for which Validate, PS5.1 Acceptance Smoke, and Windows Installer Pack Smoke are all green on the exact same SHA.

## Starting evidence

Task275 source/test candidate: `9d3000e3d8d09d712f621c1985d7bde66c2519ef`.

Validate `34027500017` failed on two different pre-existing Windows tests across two attempts:

- attempt 1 / Windows 3.14: `ticket-runtime.test.ts` hard-ceiling test timed out;
- attempt 2 / Windows 3.11: the first test passed, but `v093-response-ready-boundary.test.ts` timed out.

Task275's 3 focused tests passed in both observed plugin runs. Task274's prior exact-SHA Windows 3.11 run executed the same v093 test in roughly 0.30 seconds, while Task275 attempt 2 showed broad suite slowdown.

## Required work

### A. Diagnose before changing policy

1. Compare the two failing Task275 Windows jobs with at least one recent green Windows Validate baseline.
2. Measure focused repeated execution of both flaky tests and their nearest SQLite-heavy neighbors on Windows.
3. Determine whether the instability comes from test-level semantics, SQLite contention/file parallelism, Vitest worker scheduling, hosted-runner resource variance, or another reproducible cause.
4. Record timings and evidence. Do not call a test flaky solely because a rerun passes.

### B. Stabilize the smallest correct boundary

Prefer, in order:

1. deterministic fixture/cleanup or worker-isolation repair if a concrete test race/contention is found;
2. targeted file/test timeout adjustment only when measured runtime distribution justifies it and the assertion remains meaningful;
3. Windows-specific Vitest concurrency/isolation configuration if suite-level resource contention is the demonstrated cause.

Do **not** solve this with an unexplained blanket global timeout increase. Do not weaken assertions, skip Windows, mark failures allowed, or remove matrix coverage.

Production runtime semantics are not expected to change. If a production defect is discovered, use RED -> minimal fix -> GREEN and explain the causal link before changing source.

### C. Preserve accepted behavior

Keep green:

- Task273 Discord durable pre-transport staging;
- Task274 no-runId Discord receipt ambiguity fence and lifecycle tests;
- Task275 owner-context, stale-waiter, and exactly-once settlement tests;
- Dashboard Direct behavior and `webchat` alias compatibility;
- Direct Recovery and response-ready immutability tests;
- full plugin suite and build/package validation.

### D. Exact-SHA acceptance

Run local focused/full validation and `git diff --check`.

Then require on one exact candidate SHA:

- Validate: success across the entire matrix;
- PS5.1 Acceptance Smoke: success;
- Windows Installer Pack Smoke: success.

If CI fails, diagnose the exact failure before any retry. Do not use repeated blind reruns to manufacture a green result. A single evidence-backed corrective rerun is acceptable only after documenting why no source/harness mutation is required.

## Hard fences

```text
live Discord/Dashboard semantic sends             = 0
live OpenClaw session Delete/reset                 = 0
manual live Ticket/session/SQLite mutation         = 0
recovery replay/redelivery/disposition              = 0
installer/install-over/uninstall/reset             = 0
Gateway/provider/service lifecycle mutation        = 0
Scheduled Task mutation                            = 0
release/tag/default-branch promotion               = 0
force push/history rewrite                         = 0
```

Task272's parked live Delete/test-message authority remains unconsumed.

## Completion

Publish:

`docs/operations/coordination/reports/CNX-20260906-276-windows-vitest-timing-stabilization.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop.
