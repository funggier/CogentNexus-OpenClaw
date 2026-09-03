# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK234_DASHBOARD_ORIGIN_DISCORD_SESSION_DURABLE_STAGING_TDD_REPAIR`
Current disposition: `TASK233_REAL_DURABLE_SEMANTIC_FAILURE_ACCEPTED__STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`
Task ID: `CNX-20260903-234`
Parent task: `CNX-20260903-233`
Installer-requalification parent: `CNX-20260902-230`
Accepted repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-03 ICT
Executor: Hermes / authenticated Windows + repository operator
Coordinator / independent reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Accepted pre-Task-234 production repair authority:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted pre-Task-234 plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

No Release/tag/asset mutation is authorized.

## Task 233 independent review

Review:

`reviews/CNX-20260903-233-human-manual-dashboard-send-semantic-requalification-review.md`

Verdict:

`ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`

Task 233 is a genuine runtime acceptance failure, unlike Tasks 231/232.

The user manually submitted once from Dashboard and runtime created:

```text
Ticket: CNXT-57ab3fb4-930e-43a6-bd16-90f5b84620e3
run:    e225362a-8872-45f8-a914-c90d835880c0
owner:  agent:main:discord:channel:1531199905673252946
```

OpenClaw/Ollama produced visible Dashboard assistant content, but CogentNexus created no attributable `cnx_assistant_delivery direct_result`; the Ticket later emitted `direct_redelivery_timeout` with:

`Direct response delivery was not confirmed before deadline`

No attributable Discord reply, direct operator Discord/API Send, semantic resend, manual DB write, lifecycle mutation, or historical-evidence mutation occurred.

## Provisional source root cause

Accepted source currently allows `before_agent_finalize` to recognize a Discord-associated owner Ticket, but the subsequent durable Dashboard staging path re-enters `stageDashboardDirectResult(...)`, which resolves only through `dashboardTicket(...)` / `isDashboardSession(...)` and therefore rejects owner keys shaped as:

`agent:*:discord:channel:*`

That source mismatch closely matches Task-233 live evidence.

However, owner session identity and ingress surface are not equivalent. Real Discord-origin turns on the same owner key must remain Discord/external-channel deliveries.

Therefore Task 234 must identify a trusted ingress-surface/correlation signal and must not broaden all Discord-associated sessions into Dashboard sessions.

## Active Task 234

Execute:

`tasks/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair.md`

Required flow:

```text
fresh authority
-> read-only Task-233 run/telemetry correlation
-> trusted ingress-surface contract investigation
-> genuine production-shaped RED
-> minimal production repair
-> targeted GREEN
-> full repository / Actions GREEN
-> report
-> STOP before live install/retest
```

If OpenClaw `2026.7.1-2` exposes no trustworthy way to distinguish Dashboard-origin from Discord-origin at the required boundary, stop as:

`BLOCKED_INGRESS_SURFACE_CONTRACT`

Do not guess from prompt content, `@Ce`, browser URL, or owner session key alone.

## Required TDD behavior

The new regression must cover both on the same Discord-associated owner-key shape:

1. **Dashboard-origin** — exact final must be durably staged/marked/settled once without legacy timeout.
2. **Discord-origin** — must remain external-channel/Discord delivery behavior and must not be claimed by Dashboard native staging.

Ordinary `agent:main:dashboard:*` behavior, duplicate handling, NO_REPLY handling, owner-generation fencing, and durable response-ready immutability must remain green.

## CI authority note

Task-233 report HEAD:

`827577a053979517a46f419a6f63564bd7420570`

- Windows Installer Pack Smoke — SUCCESS
- PS5.1 Acceptance Smoke — SUCCESS
- Validate `33706153188` — FAILURE

Validate failed only in `validate (windows-latest, 3.14)` because:

`src/v093-response-ready-boundary.test.ts`

timed out at 15 seconds during `npm test` (`1 failed / 279 passed`). Other matrix jobs passed, including Windows/Python 3.11, and the report commit is docs-only.

Task 234 must recheck/reproduce this timing anomaly. It must not call the report HEAD GREEN, and it must not increase timeouts blindly.

## Semantic / live mutation budget

```text
Dashboard semantic Sends: 0
Discord-origin semantic Sends: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway mutation: 0
plugin live mutation: 0
provider/model substitution: 0
process termination: 0
stale Task-223/Task-233 evidence mutation: 0
Release/tag/asset mutation: 0
force push: 0
```

Read-only live evidence and repository source/test/CI repair are authorized.

## Retry policy

Read-only/tooling retries: up to 2 additional evidence-driven attempts per logical operation.

Test/CI retry is permitted only when evidence indicates tooling/timing failure; deterministic product/test failures must be investigated rather than rerun until green.

Semantic retry budget remains `0`.

## Stop boundary

Hermes must publish:

`reports/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair.md`

Then stop for independent ChatGPT review.

Even after repository GREEN, do not install the candidate live, perform another Dashboard/Discord semantic turn, replay or manually settle the Task-233 Ticket, clean historical evidence, or mutate public Release/tag/assets.
