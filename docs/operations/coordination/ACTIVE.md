# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK232_EXISTING_SESSION_DASHBOARD_SEMANTIC_DURABLE_REQUALIFICATION`
Current disposition: `TASK231_PRODUCT_FAILURE_REJECTED__SEMANTIC_BUDGET_UNCONSUMED__EXISTING_SESSION_REEXECUTION_AUTHORIZED`
Task ID: `CNX-20260903-232`
Parent task: `CNX-20260903-231`
Installer-requalification parent: `CNX-20260902-230`
Repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-03 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted source/runtime authority

Exact repaired source:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-230 managed convergence remains accepted.

## Task 231 review result

Task-231 report disposition `FAIL_DASHBOARD_TURN` is not accepted as a product failure.

Independent review:

`reviews/CNX-20260903-231-post-repair-managed-dashboard-semantic-durable-requalification-review.md`

Verdict:

`REJECT_PRODUCT_FAILURE_CLASSIFICATION__ACCEPT_FAIL_CLOSED_PRESERVATION__SEMANTIC_BUDGET_UNCONSUMED__EXISTING_SESSION_REEXECUTION_AUTHORIZED`

Task 231 made zero semantic submissions, zero new Tickets/model calls/results, and zero Discord Sends. It stopped because the executor incorrectly treated the Discord-associated Dashboard session as ineligible and tried to create a fresh empty session, despite task authority explicitly allowing Dashboard turns on sessions originally associated with Discord.

## Active Task 232

Execute:

`tasks/CNX-20260903-232-existing-session-dashboard-semantic-durable-requalification.md`

The intended Dashboard session is explicitly eligible:

```text
agent:main:discord:channel:1531199905673252946
```

Existing history is allowed.

`New session` must not be clicked.

Exact one-shot Dashboard message, no `@Ce` prefix:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Task-231 left this exact text as an unsent draft. Fresh UI evidence wins: if the exact draft remains, do not retype or alter it; if the composer is empty, enter it once; if composer content differs, stop without Send.

## Send / semantic retry boundary

Dashboard `Send message` activations:

`1 maximum`

After the single Send activation or any observed new semantic lineage:

`SEMANTIC_RETRY_GATE=CLOSED`

It cannot reopen. UI uncertainty, timeout, slow Ollama response, or missing immediate evidence is never permission to click Send again.

Required PASS shape:

```text
Dashboard Send activations: 1
Dashboard human submissions: 1
new Ticket lineage: 1
new OpenClaw session/run lineage: 1
new Ollama/model-call lineage: 1
new durable semantic/result lineage: 1
new logical Dashboard assistant result: 1
Discord replies attributable to Dashboard turn: 0
direct operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual product/data/lifecycle mutations: 0
```

## Routing / Discord boundary

Normal environment invariant:

```text
Dashboard-origin turn -> Dashboard result
Discord-origin turn   -> Discord result
```

Discord channel `1531199905673252946` is read-only negative control only during Task 232.

Discord-origin test messages: `0`.
Direct operator Discord/API Sends: `0`.

A conclusively attributable Discord reply from the Dashboard-origin Task-232 turn is `FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`.

## Retry policy

Read-only tooling/observer retries remain bounded to up to 2 additional evidence-driven attempts per logical observation and must be recorded.

Semantic Send/submission/model/Ticket/result/effect retries: `0`.

## Historical evidence / other hard fences

Task-223 transaction, matching inventory, ownership manifest and backup remain immutable forensic evidence.

No installer/reset/uninstall/reinstall, manual lifecycle/Gateway repair, plugin mutation, manual Ticket/outbox/recovery/SQLite write, recovery replay, provider/model substitution, process kill, stale-evidence cleanup/finalization, product/source/test/workflow edit, Release/tag/asset mutation, force push, Discord-origin acceptance turn, `New session`, or second Dashboard Send is authorized.

## Stop boundary

Hermes must publish:

`reports/CNX-20260903-232-existing-session-dashboard-semantic-durable-requalification.md`

Then stop for independent ChatGPT review before any Discord-origin acceptance or further semantic turn.