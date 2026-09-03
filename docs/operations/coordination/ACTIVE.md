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

## Task 233 independent review

Review:

`reviews/CNX-20260903-233-human-manual-dashboard-send-semantic-requalification-review.md`

Verdict:

`ACCEPT_FAIL_DURABLE_SEMANTIC_TRACE__DASHBOARD_ORIGIN_ON_DISCORD_ASSOCIATED_SESSION_STAGING_SCOPE_DEFECT_PROVISIONALLY_PROVEN__TDD_REPAIR_REQUIRED`

Task 233 is a genuine runtime acceptance failure, unlike Tasks 231/232.

Exact authoritative lineage from the Task-233 report:

```text
Ticket: CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4
run:    e225013e-8d50-4479-b227-ca9a10b89a46
owner:  agent:main:discord:channel:1531199905673252946
```

The one manual Dashboard Send entered runtime. The run recorded four internal Ollama `qwen3.5:9b` call records and reached `response_ready`; Dashboard displayed assistant content. CogentNexus created no attributable `cnx_assistant_delivery direct_result`, no Ticket outbox row, and no delivery confirmation. The Ticket then emitted `direct_redelivery_timeout` with:

`Direct response delivery was not confirmed before deadline`

No attributable Discord reply, direct operator Discord/API Send, semantic resend, manual durable DB/lifecycle mutation, or historical-evidence mutation occurred.

## Provisional source root cause

Accepted source currently allows `before_agent_finalize` to recognize a Discord-associated owner Ticket, but the subsequent Dashboard durable staging path re-enters `stageDashboardDirectResult(...)`, which resolves only through `dashboardTicket(...)` / `isDashboardSession(...)` and therefore rejects owner keys shaped as:

`agent:*:discord:channel:*`

That mismatch closely matches Task 233: native Dashboard result visible, durable `direct_result` absent.

Owner session identity is not the same thing as ingress surface. Real Discord-origin turns on the same owner key must remain Discord/external-channel deliveries.

Task 234 must therefore prove a trusted ingress-surface/correlation signal and must not simply broaden every Discord-associated session into Dashboard.

## Active Task 234

Execute:

`tasks/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair.md`

Required flow:

```text
fresh authority
-> read-only exact Task-233 lineage/telemetry correlation
-> trusted ingress-surface contract investigation
-> genuine production-shaped RED
-> minimal production repair
-> targeted GREEN
-> full repository / Actions GREEN
-> report
-> STOP before live install/retest
```

If OpenClaw `2026.7.1-2` exposes no trustworthy Dashboard-vs-Discord ingress discriminator at the required boundary, stop:

`BLOCKED_INGRESS_SURFACE_CONTRACT`

Do not guess from prompt content, `@Ce`, browser URL, or owner session key alone.

## Required TDD shape

On the same `agent:main:discord:channel:<id>` owner form:

1. **Dashboard-origin** must durably stage/mark/settle the Dashboard result exactly once and avoid legacy delivery timeout.
2. **Discord-origin** must stay on existing Discord/external-channel receipt semantics and must not be claimed by Dashboard native staging.

Ordinary `agent:main:dashboard:*`, duplicate handling, NO_REPLY, generation fencing, and durable response-ready immutability must stay GREEN.

Production must remain unchanged until genuine test-only RED is committed and demonstrated.

## Task-233 report-head CI

Task-233 report HEAD:

`827577a053979517a46f419a6f63564bd7420570`

- Windows Installer Pack Smoke — SUCCESS
- PS5.1 Acceptance Smoke — SUCCESS
- Validate `33706153188` — FAILURE

Validate failed only in Windows/Python 3.14 plugin tests because `src/v093-response-ready-boundary.test.ts` timed out at 15 seconds (`1 failed / 279 passed`). Other matrix jobs passed, including Windows/Python 3.11; the Task-233 report commit itself is docs-only.

Task 234 must recheck/reproduce this timing anomaly. Do not call the Task-233 report HEAD GREEN and do not increase timeout blindly.

## Semantic / live mutation budget

```text
Dashboard semantic Sends: 0
Discord-origin semantic Sends: 0
direct operator Discord/API Sends: 0
semantic retries: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway mutation: 0
live plugin mutation: 0
provider/model substitution: 0
process termination: 0
Task-223/Task-233 evidence mutation: 0
Release/tag/asset mutation: 0
force push: 0
```

Read-only live evidence and repository source/test/CI repair are authorized.

Read-only/tooling retries: up to 2 additional evidence-driven attempts per logical operation. Test/CI retry only for evidenced tooling/timing failure; deterministic failures require diagnosis.

## Stop boundary

Hermes must publish:

`reports/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair.md`

Then stop for independent ChatGPT review.

Even after repository GREEN, do not install/retest live, perform another Dashboard/Discord semantic turn, replay or manually settle Task 233, clean historical evidence, or mutate public Release/tag/assets.
