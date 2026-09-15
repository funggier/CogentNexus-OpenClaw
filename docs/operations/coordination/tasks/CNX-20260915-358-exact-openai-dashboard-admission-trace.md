# CNX-20260915-358 — Exact OpenAI Dashboard Admission Trace

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Parent: `CNX-357`
Execution mode: `READ_ONLY_EXISTING_RUN_TRACE`
Base release: `v0.9.5`

## Objective

Trace the already-executed CNX-357 OpenAI Dashboard request backward from the known Dashboard session/run evidence to the CogentNexus effective admission boundary.

This task exists because CNX-357 established:

- the Operator successfully selected `OpenAI / GPT-5.6 Luna`;
- exactly one semantic request was submitted;
- the Dashboard visibly returned `CNX357-DONE`;
- the fresh Dashboard session key was `agent:main:dashboard:fffd7146-8d4b-4a1b-88dc-d9f249d98779`;
- OpenClaw runtime session listing showed the same session key with runtime session ID `4a027d34-4c87-4158-9afc-d08157942615` and model `openai/gpt-5.6-luna`;
- no fresh durable Ticket/Run/Call/Inference/Result/Delivery lineage could be correlated to that request.

Current source also explicitly treats canonical Dashboard sessions as eligible for durable admission even when `senderIsOwner=false` in current OpenClaw WebChat behavior.

The remaining question is therefore causal:

```text
exact Dashboard request
-> OpenClaw agent lifecycle
-> before_agent_run
-> durableAdmissionEligible
-> Ticket-first decision
-> durable Ticket
```

Where is the first point at which the expected invariant is not observed?

## Hard fences

- No new semantic request.
- Do not replay CNX-344.
- Do not resend `CNX357-DONE`.
- No provider/model/auth/configuration mutation.
- No credential extraction or display.
- No provider installation or modification.
- No plugin reinstall/enable/disable.
- No Gateway restart/stop/start.
- No production source modification.
- No OpenClaw source modification.
- No SQLite/Ticket/session/delivery mutation.
- No undocumented mutating Gateway methods.
- No changes to `main` or `v0.9.5` tag.
- No force-push/history rewrite.

## Exact target run

Use ONLY the existing CNX-357 request:

- Dashboard session key: `agent:main:dashboard:fffd7146-8d4b-4a1b-88dc-d9f249d98779`
- Runtime session ID: `4a027d34-4c87-4158-9afc-d08157942615`
- Provider/model: `openai/gpt-5.6-luna`
- Payload: `Reply exactly with CNX357-DONE.`
- Dashboard displayed time: `Sep 15, 2026, 9:25 PM`

Do not substitute another session or run.

## Required investigation

### 1. Verify exact identities

Confirm the target session key/runtime session ID using supported OpenClaw read-only status/log surfaces.

Confirm the request timestamp as closely as supported.

### 2. Trace runtime logs

Search the installed OpenClaw and CogentNexus logs around the exact request time and session identity.

Look specifically for evidence of:

- agent run creation;
- `before_agent_run` dispatch;
- CogentNexus hook invocation;
- `durableAdmissionEligible` decision;
- `senderIsOwner` value;
- Dashboard namespace detection;
- Ticket classification;
- `ticketFirst` decision;
- Ticket creation/admission;
- block/allow return behavior;
- provider invocation;
- result/delivery handling.

Capture only non-secret evidence.

### 3. Compare runtime evidence with source

Use current v0.9.5 source on the task branch to establish the expected path.

Relevant source contract includes:

```ts
api.on("before_agent_run", ...)
```

and:

```ts
durableAdmissionEligible({ sessionKey, senderIsOwner })
```

The source contract states that canonical Dashboard sessions are eligible even when `senderIsOwner=false` because WebChat may not carry a channel sender identity.

Determine whether runtime evidence shows the same path.

### 4. Trace backward to first divergence

Use root-cause tracing.

Start from the observed fact:

```text
OpenAI / GPT-5.6 Luna produced CNX357-DONE
```

Trace backward:

```text
visible response
-> OpenAI execution
-> agent run
-> before_agent_run
-> CogentNexus handler
-> durableAdmissionEligible
-> Ticket-first branch
-> Ticket persistence
```

Identify the FIRST boundary where expected behavior and observed behavior diverge.

Do not jump directly to a fix hypothesis.

## Decision rules

### CURRENT_RED / DEFECT

Use only if the existing exact run provides direct evidence that OpenAI inference/user-visible response occurred while the expected Ticket-first admission path was skipped, bypassed, or materially failed for this same request.

A log sequence such as:

```text
agent run
-> OpenAI request
-> response
```

without the expected CogentNexus admission path may qualify only when the evidence establishes that the CogentNexus hook was expected to govern this run and was bypassed or failed.

### BOUNDARY_CLOSED / PASS

Use only if the exact existing run can be proven to have entered durable Ticket-first admission and the apparent missing durable correlation was caused by an inspection/correlation limitation rather than a runtime bypass.

### UNRESOLVED / BLOCKED

Use when runtime logs/status surfaces cannot establish the required causal sequence with sufficient confidence.

Do not treat absence of logs alone as proof of a defect.

## Important distinction

CNX-357 already established that the Dashboard action was real.

Do not reopen the question:

> “Was OpenAI actually selected?”

That is already established for this run.

The remaining question is:

> “What happened to this exact Dashboard request at the CogentNexus admission boundary?”

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260915-358-exact-openai-dashboard-admission-trace-report.md`

The report must include:

- exact source/task starting SHA;
- exact target session key/runtime session ID;
- request timestamp;
- relevant OpenClaw/CogentNexus runtime log evidence;
- `before_agent_run` evidence;
- `durableAdmissionEligible` evidence;
- Ticket-first decision evidence;
- Ticket persistence evidence if present;
- OpenAI execution evidence;
- exact first-divergence boundary if proven;
- no-secret accounting;
- hard-fence accounting;
- changed paths;
- remote read-back verification;
- final classification.

## Non-authorization

This task does NOT authorize a production fix.

If and only if `CURRENT_RED` is proven, stop and hand off to ChatGPT for independent review before creating a separate TDD repair task.

Do not mutate production code in CNX-358.
