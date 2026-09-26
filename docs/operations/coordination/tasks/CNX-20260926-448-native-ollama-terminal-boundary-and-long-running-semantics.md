# CNX-20260926-448 — Native Ollama Terminal Boundary and Long-Running Semantics

Status: `ACTIVE`
Owner: ChatGPT
Executor: ChatGPT
Parent: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`
Baseline release: `v0.9.8` (immutable)
Working branch: `cnx-448-native-ollama-terminal-boundary`
GitHub issue: `#40` — `https://github.com/funggier/CogentNexus-OpenClaw/issues/40`

## Objective

Extend the terminal-authority repair pattern proven by CNX-446 to native OpenClaw/Ollama Direct runs so intermediate assistant tool-use messages cannot become durable results or close Tickets.

Long-running local inference is allowed. Duration alone must not be treated as terminal success or failure.

## Production evidence

Observed live OpenClaw 2026.9.5 session:

- Dashboard session: `agent:main:dashboard:4e97d1d4-2007-43d0-838d-0a929f1e8140`
- OpenClaw session id: `94168f40-4dcf-458c-b2fd-c9b4d73ff053`
- run id: `189e1a24-8230-4d50-90fc-d24d25ca1acc`
- Ticket: `CNXT-c7c1531f-81cc-4ac7-a205-516c936a9424`
- provider/model: `ollama/qwen3.8:27b`
- model-call duration: `1235402 ms`
- first assistant write: `stopReason="toolUse"` with two tool calls
- CNX incorrectly staged that intermediate text, marked response ready, confirmed delivery, and completed the Ticket
- tool results then continued
- later assistant event: `stopReason="aborted"`, `errorMessage="request timed out"`
- CNX subsequently recorded `host_terminal_conflict`

The defect is terminal classification, not model slowness.

## Required semantics

1. Reuse the CNX-446 terminal-authority architecture; do not build an unrelated settlement path.
2. Exact run/session correlation remains mandatory whenever native OpenClaw exposes `__openclaw.runId`.
3. Native assistant messages with `stopReason="toolUse"` are non-terminal.
4. Assistant messages containing tool-call content are non-terminal until a later assistant final exists.
5. `aborted`, error, timeout, or interrupted terminal evidence must not become terminal-success delivery.
6. Unknown native terminal state fails closed: keep the Ticket non-terminal/recoverable rather than falsely completing it.
7. Proven native final messages without Codex `runTerminal` metadata remain supported.
8. Codex/App-Server `runTerminal=true` semantics from CNX-446 remain unchanged.
9. Provider/model/auth routing remains OpenClaw-owned.
10. v0.9.8 tag/release remain immutable.
11. Long-running local inference is permitted; timeout policy must remain separate from terminal-result classification.

## TDD

RED must reproduce the live native topology:

- accepted Dashboard Direct Ticket;
- native Ollama assistant message with exact run id;
- visible reasoning/text plus tool calls;
- `stopReason="toolUse"`;
- prove the current fallback incorrectly creates a durable direct result.

GREEN must prove:

- tool-use assistant write receives no CNX delivery marker;
- Ticket remains `accepted`;
- `response_ready_at` and `delivery_confirmed_at` remain null;
- no `direct_result` row exists;
- exact native terminal success can still stage and settle;
- wrong native run id cannot capture a Ticket;
- aborted/error native writes cannot settle success;
- Codex CNX-446 regression tests remain GREEN;
- exactly-once durable result/delivery invariants remain intact.

## Implementation direction

Primary repair surface:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Introduce provider-neutral terminal classification around the existing CNX-446 boundary. Provider-specific metadata supplies evidence; the settlement layer remains shared.

Native OpenClaw/Ollama negative terminal evidence should include at minimum:

- `stopReason="toolUse"`;
- any unresolved `toolCall` content;
- `stopReason="aborted"`;
- explicit error/timeout metadata.

Where native `__openclaw.runId` is present, bind fallback staging to that exact run instead of session-only selection.

## Validation

- RED -> GREEN focused CNX-448 tests;
- CNX-446 terminal-boundary tests;
- Dashboard verified-delivery suite;
- full plugin Vitest suite;
- TypeScript/build validation;
- repository Python validation gates;
- `git diff --check`;
- exact commit/SHA evidence;
- GitHub exact-SHA CI;
- physical install-over/source parity before live acceptance;
- fresh native Ollama live acceptance with tool use or equivalent multi-step continuation.

## PASS criteria

A native intermediate tool-use write cannot create `response_ready`, durable result, delivery confirmation, or Ticket completion, while a true native final still settles exactly once.

## Report destination

`docs/operations/coordination/reports/CNX-20260926-448-native-ollama-terminal-boundary-and-long-running-semantics-report.md`

## Local qualification checkpoint — 2026-09-26

RED evidence reproduced the production defect before the repair: the native Ollama `toolUse` message received a CogentNexus delivery marker and incorrectly became the durable Direct result.

Implemented repair:

- native terminal-authority classification around the existing CNX-446 settlement boundary;
- `toolUse` / tool-call-bearing assistant messages classify non-terminal;
- aborted/error/timeout/interrupted writes classify interrupted and cannot settle success;
- exact native `__openclaw.runId` binds to the exact Dashboard Ticket and owner session when present;
- explicit unknown native stop reasons fail closed;
- existing Codex/App-Server `runTerminal=true` behavior remains unchanged;
- legacy native messages without projected stop metadata remain compatible when no negative terminal evidence exists.

Local validation:

- focused CNX-448 + CNX-446 + Dashboard delivery: `20/20 PASS`;
- full plugin Vitest: `94 files / 441 tests PASS`;
- TypeScript/build: PASS;
- full Python: `745 passed, 5 skipped, 38 subtests passed`;
- evaluation: PASS, evidence SHA-256 `357596ae0d381f1331b9c1403b8800e21d2f44149dcbe24c6e0fbf4beca16c83`;
- plugin validation: PASS (`46` config properties, `5` tools, `9` required DB tables, `296` packed files);
- `npm audit --omit=dev`: `0 vulnerabilities`;
- `git diff --check`: PASS.

No timeout value or provider/model routing was changed. Long-running Ollama execution remains permitted; Task 448 changes only terminal-result authority.

## Current classification

`CNX448_LOCAL_GREEN_CI_PENDING`
