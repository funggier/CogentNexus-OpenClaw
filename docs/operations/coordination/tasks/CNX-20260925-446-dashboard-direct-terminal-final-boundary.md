# CNX-20260925-446 — Dashboard Direct Terminal-Final Boundary Repair

Status: `IN_PROGRESS`
Owner: ChatGPT
Executor: ChatGPT
Parent: `CNX-20260922-444-v097-gateway-interruption-direct-recovery.md`
Target release line: `v0.9.8`
Working branch: `cnx-446-dashboard-direct-terminal-final-boundary`

## Objective

Prevent CogentNexus-OpenClaw from treating a visible non-terminal assistant progress/commentary message as the durable Direct result for a Dashboard run that is still executing.

A Direct Ticket may become `response_ready`, `delivery_confirmed`, and `completed` only from terminal/final authority for the exact run. A visible message by itself is not terminal authority.

## Why this task exists

A real OpenClaw 2026.9.5 Dashboard run exposed an early-completion defect.

Production evidence:

- Dashboard session key: `agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6`
- OpenClaw session id: `3dfbe4db-db86-4b07-9f89-6dc3757c07d9`
- run id: `63bb6787-a016-426b-9ba0-d84ac15ff555`
- Ticket: `CNXT-f191f552-305a-4950-a77c-1dfd3444d253`
- provider/model: `openai/gpt-5.6-luna`
- Ticket admitted before inference: PASS
- route: Direct, `workflow_eligible=0`: PASS
- first visible assistant progress message persisted at approximately `2026-09-25T08:11:16.592Z`
- CNX marked `response_ready`, `delivery_confirmed`, and `completed` from that progress message at approximately `08:11:16.587Z-08:11:16.595Z`
- the run then continued tool execution until the real final answer at approximately `08:13:07.217Z`
- OpenClaw recorded `model.completed` at `08:13:07.244Z` and `session.ended=success` at `08:13:07.249Z`

The durable payload SHA-256 stored by CNX was proven to match the first progress/commentary text, not the final answer.

## Production terminal evidence finding

The false progress message and the true final message both carried `stopReason="stop"`; therefore `stopReason` alone is not terminal authority.

For the OpenAI/Codex mirrored path in OpenClaw 2026.9.5:

- progress/commentary message:
  - `__openclaw.runId` present
  - `__openclaw.mirrorOrigin="codex-app-server"`
  - `__openclaw.runTerminal` absent
- true terminal assistant message:
  - same exact run id
  - same mirror origin
  - `__openclaw.runTerminal=true`

OpenClaw's UI can still expose Stop while the run is active; that is a user-visible projection of internal execution state. CNX must rely on internal terminal/run authority, not on the UI button itself.

Important provider-neutrality evidence: recent native Ollama terminal messages on OpenClaw 2026.9.5 do not carry `__openclaw.runTerminal`. Therefore CNX MUST NOT require that field globally.

## Root-cause candidate

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts` currently has a `before_message_write` fallback that, when no `before_agent_finalize` candidate exists, selects the single accepted Dashboard Direct Ticket for the session and stages the current assistant text.

That fallback does not prove that the current assistant write is terminal. A mirrored progress/commentary write can therefore be staged, marker-bearing, settled, and used to close the Ticket while the exact OpenClaw run remains active.

## Required semantics

1. Visible assistant output is not sufficient terminal authority.
2. A non-terminal mirrored progress/commentary write MUST NOT create `cnx_assistant_delivery`, `response_ready`, `delivery_confirmed`, or `completed`.
3. An exact terminal mirrored write MAY be used when OpenClaw supplies authoritative terminal metadata for the exact run.
4. Mirrored terminal metadata MUST be correlated to the exact Ticket run id and owner session; session-only matching is insufficient when exact run identity exists.
5. Existing `before_agent_finalize` terminal-candidate authority remains valid and should be preferred when present.
6. Native provider paths such as Ollama that do not expose `__openclaw.runTerminal` MUST retain their proven delivery behavior.
7. Historical OpenClaw 2026.7.1-2 development compatibility MUST not be silently broken.
8. `stopReason="stop"` MUST NOT be used by itself as terminal proof.
9. If Gateway/process interruption occurs after progress but before terminal final, the Ticket MUST remain recoverable/non-terminal rather than falsely completed.
10. Provider/model/auth routing remains OpenClaw-owned and unchanged.
11. v0.9.7 tag/release remain immutable.

## TDD requirements

RED tests MUST reproduce the production topology before the repair:

- accepted Dashboard Direct Ticket;
- mirrored assistant progress text with:
  - exact `__openclaw.runId`
  - `mirrorOrigin="codex-app-server"`
  - `stopReason="stop"`
  - no `runTerminal`;
- `before_message_write` occurs while no final candidate has been established;
- prove the current implementation incorrectly stages/settles that progress message.

GREEN tests MUST prove:

- mirrored non-terminal progress is persisted without CNX delivery marker ownership;
- Ticket remains `accepted`;
- `response_ready_at` and `delivery_confirmed_at` remain null;
- no Direct-result delivery row is created from progress;
- a later mirrored message with the same exact run id and `runTerminal=true` is eligible for terminal staging;
- wrong/missing mirrored run identity cannot capture another Ticket;
- `stopReason="stop"` without terminal authority remains non-terminal;
- existing native Ollama/legacy fallback behavior remains GREEN;
- existing `before_agent_finalize -> before_message_write -> transcript settlement` path remains GREEN;
- exactly one durable result and exactly one delivery confirmation occur.

## Implementation direction

Prefer a narrow terminal-authority fence rather than changing Ticket admission or provider routing.

Expected repair area:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Candidate strategy:

- detect OpenClaw mirrored-message metadata;
- if a final candidate is already established by `before_agent_finalize`, preserve exact candidate matching;
- otherwise, for mirrored messages, permit fallback staging only when `__openclaw.runTerminal === true`;
- bind the mirrored fallback to exact `__openclaw.runId` and owner session;
- preserve the existing native/legacy path where this metadata is not provided, subject to existing authority checks.

Do not introduce UI scraping or make the Stop button part of the runtime contract.

## Validation

Before candidate acceptance:

- focused CNX-446 Vitest RED -> GREEN;
- existing Dashboard durable-delivery tests PASS;
- existing Ollama/native delivery tests PASS;
- full plugin Vitest suite PASS;
- TypeScript/build validation PASS;
- repository validation gates PASS;
- `git diff --check` PASS;
- production npm audit remains clean;
- install-over/source parity PASS before live validation;
- fresh OpenClaw 2026.9.5 Dashboard acceptance proves:
  - progress can appear while run remains active;
  - Ticket remains accepted during progress/tool work;
  - final durable payload corresponds to the true terminal answer;
  - exactly one delivery marker/result;
  - Ticket completes only after terminal authority;
  - no duplicate recovery/delivery/inference.

## PASS criteria

Task is PASS only when the live defect is no longer reproducible and native Ollama behavior remains intact.

## FAIL / BLOCKED criteria

FAIL/BLOCKED if any repair:

- globally requires `runTerminal` and breaks native Ollama;
- uses `stopReason="stop"` as sole terminal proof;
- closes a Ticket from a progress/commentary message;
- weakens exact run/session ownership;
- changes provider/model/auth routing;
- rewrites v0.9.7 history.

## Evidence required

Record:

- RED failure evidence;
- exact changed source/tests;
- focused and full test counts;
- exact commit SHA(s);
- exact-SHA CI status;
- install/source parity;
- fresh live Ticket/run/session identity;
- progress-vs-terminal timestamps and durable payload hash;
- duplicate counts;
- final classification.

## Report destination

`docs/operations/coordination/reports/CNX-20260925-446-dashboard-direct-terminal-final-boundary-report.md`

## Current classification

`CNX446_DASHBOARD_DIRECT_TERMINAL_BOUNDARY_RED_PENDING`
