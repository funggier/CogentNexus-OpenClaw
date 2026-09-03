# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK235_TASK234_EXACT_TOPOLOGY_TDD_EVIDENCE_CLOSURE`
Current disposition: `TASK234_FUNCTIONAL_REPAIR_GREEN__PASS_REJECTED_PENDING_TDD_AND_EXACT_TOPOLOGY_EVIDENCE_CLOSURE`
Task ID: `CNX-20260903-235`
Parent task: `CNX-20260903-234`
Failure parent: `CNX-20260903-233`
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

Accepted pre-Task-234 production authority remains:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Task-234 functional candidate repair:

`43fd1d6f988431c7a94d24abc8a6811de46f78fa`

Candidate plugin payload fingerprint:

`964d471f9e330cfeffd270f2200d563dea8c3e7b9252409660df96f1173f58b7`

The Task-234 candidate is **not yet live-install authority**.

## Task 234 independent review

Review:

`reviews/CNX-20260903-234-dashboard-origin-discord-session-durable-staging-tdd-repair-review.md`

Verdict:

`REJECT_PASS_TDD_EVIDENCE_INCOMPLETE__FUNCTIONAL_REPAIR_GREEN__EXACT_TOPOLOGY_HARDENING_REQUIRED`

Accepted from Task 234:

- root-cause direction matches Task-233 durable staging failure;
- repair preserves owner/session identity instead of globally broadening Discord sessions into Dashboard;
- true Discord-origin context is kept off the Dashboard staging path;
- exact candidate SHA `43fd1d6...` has all required GitHub Actions GREEN;
- live mutation / semantic Send budget remained zero.

## Why PASS is not yet accepted

### 1. Corrected genuine RED is not independently committed/proven

`6b1e496...` is test-only, but corrections needed for the final valid regression harness were committed together with production repair in `278a235...`.

Task 235 must reconstruct the corrected production-shaped test against predecessor `89a0f539...` in a disposable checkout and prove deterministic RED at the intended staging boundary with production byte-identical to predecessor.

### 2. New exact topology test stops at pending staging

The Task-234 regression proves:

```text
Dashboard-origin + Discord-associated owner
-> marker returned
-> direct_result pending
```

It does not directly prove on that same owner topology:

```text
native transcript update
-> delivered
-> Ticket completed
-> exactly one delivery_confirmed
-> no direct_redelivery_timeout
-> no recovery regeneration
```

Existing `v162-dashboard-transcript-authority.test.ts` proves downstream settlement only for an ordinary `agent:main:dashboard:*` owner.

### 3. Ambiguous ingress context must be explicitly fail-closed

Candidate source currently checks `webchat` before `discord`. Task 235 must capture the exact OpenClaw `2026.7.1-2` hook-context contract and establish the correct behavior for missing or contradictory recognized ingress fields. Do not infer precedence.

## Active Task 235

Execute:

`tasks/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Required flow:

```text
fresh authority
-> exact OpenClaw 2026.7.1-2 ingress contract proof
-> disposable predecessor corrected-RED reconstruction
-> strengthen exact Discord-owner Dashboard settlement regression
-> same-owner Discord negative control
-> missing/ambiguous ingress fail-closed proof
-> production change only if new test exposes a real defect
-> targeted GREEN
-> full repository / Actions GREEN
-> report
-> STOP before live install/retest
```

If strengthened tests pass on `43fd1d6...`, do not edit production source.

If a strengthened test exposes a product defect, commit a new test-only RED first, then the smallest production fix, then GREEN.

## Exact candidate CI already independently rechecked

For `43fd1d6f988431c7a94d24abc8a6811de46f78fa`:

- Validate `33760819493` — SUCCESS
- Windows Installer Pack Smoke `33760819324` — SUCCESS
- PS5.1 Acceptance Smoke `33760819312` — SUCCESS

These GREEN results do not waive the missing TDD/exact-topology evidence.

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
force push/history rewrite: 0
```

Read-only inspection of exact installed OpenClaw source/types/docs and disposable repository evidence reconstruction are authorized.

## Stop boundary

Hermes must publish:

`reports/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Then stop for independent ChatGPT review.

Even after PASS, do not install/retest live, perform another Dashboard/Discord semantic turn, replay or manually settle Task 233, clean historical evidence, or mutate public Release/tag/assets.
