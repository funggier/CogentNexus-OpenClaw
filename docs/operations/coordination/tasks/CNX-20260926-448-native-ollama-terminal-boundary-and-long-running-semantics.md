# CNX-20260926-448 — Native Ollama Terminal Boundary and Long-Running Semantics

Status: `COMPLETE`
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

## Installed-candidate and live acceptance

Exact implementation commit:

`d6cf9e9c532da00880c16a700495edb833658cb4`

GitHub exact-SHA CI:

- Validate run `36214305293`: SUCCESS;
- PS5.1 Acceptance Smoke run `36214305250`: SUCCESS;
- Windows Installer Pack Smoke run `36214305241`: SUCCESS.

Physical install-over on OpenClaw 2026.9.5:

- installer exit: `0`;
- controller returned to MANAGED/active, generation `34`;
- provider ownership remained `openclaw`;
- Gateway 2026.9.5 healthy on `127.0.0.1:18789`;
- supervisor returned Ready/Enabled/Hidden with `LastTaskResult=0`;
- packaged payload versus installed extension: `296/296` byte-equal, no missing/changed/extra non-`node_modules` files;
- package-payload manifest SHA-256: `9559891cbdb63bf58b4b2b3fd05068ee0013fd7d65f2342d9ced7eee8c298b29`.

Fresh native Ollama multi-step acceptance:

- session: `agent:main:dashboard:b723e91b-d6d5-4407-8b9f-e8fee5847fe9`;
- run: `cnx448-live-native-ollama-small-v1`;
- Ticket: `CNXT-2ad1a0db-cd2e-4ac1-b1a5-43570009fabe`;
- provider/model: `ollama/qwen3:1.7b`;
- transcript seq 4: assistant `stopReason="toolUse"`, exact run id;
- transcript seq 5: toolResult;
- the Ticket remained non-terminal throughout the intermediate write and had no direct-result delivery;
- the second model call then completed and only then produced `response_ready` at `2026-09-26T04:04:20.141Z`;
- delivery confirmed at `2026-09-26T04:04:20.580Z`;
- exactly one `direct_result` delivery row exists and no outbox row remains.

The small-model tool invocation itself produced a tool validation error and the final assistant text reported that error. This does not weaken the terminal-boundary proof: the run still exercised the required `toolUse -> toolResult -> later assistant final` topology, and CogentNexus did not settle on the intermediate assistant write.

A simultaneous long-running `ollama/qwen3.8:27b` control later entered the existing hard-hang recovery path. Recovery preserved the original provider/model, produced the requested final `CNX448_OLLAMA_TOOL_FINAL`, retried delivery under resource pressure, and completed exactly once with one delivery row and no outbox residue. Task 448 does not change that timeout/recovery policy.

Post-acceptance runtime:

- SQLite integrity: `ok`;
- non-terminal Tickets: `0`;
- pending outbox: `0`;
- pending assistant delivery: `0`.

## Current classification

`CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`
