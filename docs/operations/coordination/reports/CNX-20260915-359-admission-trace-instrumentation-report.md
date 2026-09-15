# CNX-20260915-359 — Admission Trace Instrumentation Report

## Classification

`DIAGNOSTIC CANDIDATE READY — HUMAN DASHBOARD GATE PENDING`

This work adds evidence only. It does not prove the CNX-357 OpenAI lifecycle and does not claim PASS, CURRENT_RED, or a repair.

## Authority and identity

- Repository: `https://github.com/funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting remote SHA: `171dfc0ffc0c2fabb1a301f2c0b087188e758584`
- Coordination task commit: `847cbfa7ef390b3a6ce3a19a255a051e6c4aa08f`
- Candidate source commit: recorded after this report commit by remote read-back
- No `main`, tag, release, force-push, or history rewrite was touched.

## Task-before-code gate

A new task was created and pushed before production source modification:

`docs/operations/coordination/tasks/CNX-20260915-359-admission-trace-instrumentation.md`

## TDD evidence

### RED

Focused test: `src/v359-admission-trace.test.ts`

Before implementation, with dependencies installed, the test failed:

```text
TypeError: (0 , admissionTraceFields) is not a function
Tests: 1 failed
```

The first attempt before `npm ci` was a harness dependency failure (`vitest is not recognized`), not counted as RED. `npm ci` then enabled the genuine RED run above.

### GREEN and regression

- Focused trace test: **PASS** — 1 test.
- Plugin build: **PASS** — TypeScript compile and LF canonicalization.
- Full plugin test suite: **PASS** — 76 files, 338 tests.
- `npm run plugin:validate`: **PASS**.
  - mixed-plugin artifact verification: PASS
  - ticket DB bootstrap: PASS
  - package contents: `openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`, 246 files

## Diagnostic contract implemented

The existing `before_agent_run` handler now emits non-secret JSON log records using a per-hook `traceId` and these correlation fields when available:

- `runId`
- `sessionKey`
- `sessionId`
- `timestamp`

States emitted on the admission path include:

- `admission.trace.started`
- `admission.trace.input`
- `admission.trace.eligible`
- `admission.trace.ticket-decision`
- `admission.trace.ticket-persisted`
- `admission.trace.blocked`
- `admission.trace.completed`

The trace records only eligibility/config/classification/outcome/ticket identifiers. It does not include the prompt or secrets. Existing return values, Ticket persistence, provider routing, and admission semantics were left unchanged.

## Changed paths

- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/v359-admission-trace.test.ts`
- `docs/operations/coordination/tasks/CNX-20260915-359-admission-trace-instrumentation.md`
- this report

## Runtime activation boundary

The candidate was built and package-validated in the isolated checkout. No Dashboard action was performed. The live OpenClaw installation was not mutated in this phase; therefore active-runtime identity is **not yet proven**. A supported install/reload step must precede the fresh human-gated Dashboard test and must record the exact installed artifact/source identity.

## Required human Dashboard handoff — STOP HERE

Operator must perform the UI action; Hermes must not control Dashboard.

1. Open a **new Dashboard session** in the normal OpenClaw UI. Do not reuse the old CNX-357 session.
2. Select provider/model: **OpenAI / `gpt-5.6-luna`**.
3. If the UI retains an old conversation, use the UI's **New session/reset** action first.
4. Submit exactly one payload:

```text
Reply exactly with CNX359-DONE.
```

Do not resend `CNX357-DONE`, do not use the prior session key, and do not submit any second test. After the visible result, report the fresh Dashboard session key/result and stop; the next phase will correlate the trace `traceId + runId + sessionKey + sessionId` and classify the earliest missing transition.

## Current proof status

- Existing CNX-357 OpenAI response remains reply-path evidence only.
- The new candidate provides the previously missing admission-boundary evidence for a fresh run.
- No new live request has been made.
- No defect is proven.
- No Ticket-first PASS is proven.
