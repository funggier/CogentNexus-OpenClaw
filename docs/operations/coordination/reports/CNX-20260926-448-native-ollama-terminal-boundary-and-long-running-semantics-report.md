# CNX-20260926-448 — Native Ollama Terminal Boundary and Long-Running Semantics Report

Status: `COMPLETE`
Classification: `CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`
GitHub issue: `#40`
Working branch: `cnx-448-native-ollama-terminal-boundary`
Baseline SHA: `49915000ecbec131112937cd44ec7a5f0effa00a`
Baseline release: `v0.9.8` (immutable)

## Trigger and live evidence

A fresh OpenClaw 2026.9.5 Dashboard run exposed a native Ollama terminal-boundary defect:

- session key: `agent:main:dashboard:4e97d1d4-2007-43d0-838d-0a929f1e8140`;
- OpenClaw session id: `94168f40-4dcf-458c-b2fd-c9b4d73ff053`;
- Ticket: `CNXT-c7c1531f-81cc-4ac7-a205-516c936a9424`;
- run: `189e1a24-8230-4d50-90fc-d24d25ca1acc`;
- provider/model: `ollama/qwen3.8:27b`;
- direct model-call duration: `1235402 ms`.

The first assistant transcript row for the run carried `stopReason="toolUse"`, visible text, and two tool calls. CogentNexus incorrectly treated that intermediate row as terminal, added its delivery marker, persisted it as the durable Direct result, confirmed delivery, and completed the Ticket.

OpenClaw then continued with the two tool results. The same run later emitted an assistant row with `stopReason="aborted"` and `errorMessage="request timed out"`. CogentNexus subsequently recorded `host_terminal_conflict` because the Ticket was already completed while host terminal truth was interrupted.

The defect is terminal classification. The user's acceptance of long-running `qwen3.8:27b` execution means execution duration is intentionally not used as a success/failure classifier.

## Reuse of CNX-446 architecture

CNX-446 already established the correct design principle for Codex/App-Server mirrors:

```text
visible assistant output
!= terminal authority
```

Task 448 extends that same boundary rather than adding a second settlement architecture.

- Codex/App-Server remains governed by exact run correlation plus authoritative `runTerminal=true`.
- Native OpenClaw/Ollama supplies different terminal evidence and does not globally require `runTerminal`.
- Both paths converge on the same durable-result and delivery machinery only after terminal-success authority is established.

## RED evidence

A focused regression was added using the exact production topology:

- exact run id;
- exact Dashboard owner session;
- `provider="ollama"`;
- `model="qwen3.8:27b"`;
- `stopReason="toolUse"`;
- visible assistant reasoning text;
- two `toolCall` content parts.

Before the repair:

```text
1 failed / 4 passed
```

The failure showed that the current implementation returned the intermediate assistant message with an injected CogentNexus delivery marker:

```text
<!-- cogentnexus-openclaw-delivery:bc1ca22486c56782fc4b791a970600c8 -->
```

This reproduced the live false-completion defect.

## Repair

Production source:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

A native terminal-authority classifier was added before the preserved native fallback may stage a Direct result.

Current classifications:

- tool-call-bearing message or `toolUse/tool_use` stop: `non-terminal`;
- explicit error or aborted/error/timeout/cancelled/interrupted stop: `interrupted`;
- native stop/completed/complete/end-turn success stop without negative evidence: `terminal-success`;
- unknown explicit stop reason: `unknown` and therefore fail closed;
- historical native write with no projected stopReason retains legacy compatibility when no negative terminal evidence exists.

When native `__openclaw.runId` exists, fallback settlement is now bound to that exact run and requires the Ticket owner session to match. Session-only fallback remains only for legacy messages that do not project exact run identity.

No admission logic, provider selection, model selection, authentication authority, Ticket settlement implementation, or timeout value was changed.

## Regression coverage

Dedicated Task 448 tests prove:

1. the live native `toolUse` topology remains non-terminal;
2. a native terminal message for another exact run cannot capture the Ticket;
3. aborted/error native output cannot settle success;
4. an exact native terminal success still settles exactly once.

The CNX-446 regression suite also now permanently covers native tool-use false completion.

Focused result:

```text
3 files / 20 tests PASS
```

Breakdown:

- CNX-448 native boundary: 4 PASS;
- CNX-446 terminal boundary: 5 PASS;
- Dashboard verified-delivery: 11 PASS.

## Full local qualification

Plugin Vitest:

```text
94 files / 441 tests PASS
```

TypeScript/build:

```text
PASS
canonicalized 44 dist text files to LF
```

Full Python:

```text
745 passed, 5 skipped, 38 subtests passed
```

Evaluation:

- PASS;
- evidence SHA-256: `357596ae0d381f1331b9c1403b8800e21d2f44149dcbe24c6e0fbf4beca16c83`.

Plugin validation:

- 46 config properties;
- 5 tools;
- 9 required Ticket DB tables;
- 296 packed files;
- PASS.

Production dependency audit:

```text
0 vulnerabilities
```

Git whitespace validation:

```text
git diff --check: PASS
```

## Exact candidate and GitHub CI

Implementation commit:

`d6cf9e9c532da00880c16a700495edb833658cb4`

Commit subject:

`fix: fence native Ollama terminal delivery`

Exact-SHA GitHub CI:

- Validate `36214305293`: SUCCESS;
- PS5.1 Acceptance Smoke `36214305250`: SUCCESS;
- Windows Installer Pack Smoke `36214305241`: SUCCESS.

## Physical install-over

A real install-over was run against the existing OpenClaw 2026.9.5 installation.

Result:

- installer exit code `0`;
- package validation and Ticket DB bootstrap PASS;
- pre-install native handoff PASS;
- plugin local-package install PASS;
- controller returned to `active` / MANAGED at generation `34`;
- provider ownership remained `openclaw`;
- Gateway 2026.9.5 returned healthy on `127.0.0.1:18789`;
- supervisor returned Ready / Enabled / Hidden / `LastTaskResult=0`;
- SQLite integrity remained `ok`.

The installer again exercised the known OpenClaw 2026.9.5 CLI non-exit behavior during plugin lifecycle mutation. Its existing bounded reconciliation path handled the mutation and the installer completed successfully.

## Package/installed parity

A fresh `npm pack --ignore-scripts` payload was compared byte-for-byte with the installed extension, excluding dependency material under `node_modules` from the package identity contract.

Result:

- package files: `296`;
- present and compared: `296`;
- matched: `296`;
- missing: `0`;
- changed: `0`;
- extra installed non-`node_modules` files: `0`;
- package-payload manifest SHA-256: `9559891cbdb63bf58b4b2b3fd05068ee0013fd7d65f2342d9ced7eee8c298b29`.

Therefore the installed candidate is byte-contract equal to the package produced from the exact source candidate.

## Fresh native Ollama multi-step acceptance

A fresh Dashboard session was created through OpenClaw. OpenClaw initially resolved the user's normal local target `ollama/qwen3.8:27b`. To obtain a bounded control while the 27B run continued, a separate fresh Dashboard session was switched through the OpenClaw-owned `sessions.patch` boundary to `ollama/qwen3:1.7b`; CogentNexus did not select or override the provider/model.

Acceptance session:

- session: `agent:main:dashboard:b723e91b-d6d5-4407-8b9f-e8fee5847fe9`;
- OpenClaw session id: `47b4d0c9-44c6-4f3f-bb4b-d90a45b43312`;
- run: `cnx448-live-native-ollama-small-v1`;
- Ticket: `CNXT-2ad1a0db-cd2e-4ac1-b1a5-43570009fabe`;
- provider/model: `ollama/qwen3:1.7b`.

Transcript/evidence order:

1. first native model call started `03:57:28.804Z`;
2. assistant seq 4 persisted at `04:02:28.562Z` with exact run id, provider/model `ollama/qwen3:1.7b`, and `stopReason="toolUse"`;
3. toolResult seq 5 persisted at `04:02:29.868Z`;
4. a second native model call started at `04:02:30.176Z`;
5. the second model call ended at `04:04:19.653Z`;
6. only after that later model completion did CogentNexus record `response_ready` at `04:04:20.141Z`;
7. delivery was confirmed and the Ticket completed at `04:04:20.580Z`.

At the intermediate tool-use boundary:

- Ticket remained `accepted`;
- `response_ready_at` remained null;
- `delivery_confirmed_at` remained null;
- there was no `direct_result` delivery row.

The model selected the generic `tool_call` surface with invalid arguments for the requested file read, so the toolResult was a validation error and the later assistant final reported that error. This still exercises the required production topology: an intermediate assistant `toolUse`, a toolResult, then a later assistant terminal write. The semantic contract under test is terminal authority, not tool argument quality.

Final durable state:

- exactly one `direct_result` delivery row;
- delivery status `delivered`;
- zero outbox rows for the Ticket;
- no duplicate settlement.

This directly proves the production defect is repaired.

## Long-running qwen3.8 control and recovery observation

The simultaneous fresh `ollama/qwen3.8:27b` run used:

- session: `agent:main:dashboard:a9817a41-2845-4ee6-8aea-6d65c261aa4d`;
- run: `cnx448-live-native-ollama-tool-v5`;
- Ticket: `CNXT-71469a13-022a-4517-b0e6-3bdf9ba5668d`.

The first model call remained long-running and the existing Host logic later authorized its hard-hang recovery path. This is separate from Task 448's terminal-result classifier. No timeout or recovery threshold was changed by Task 448.

Recovery preserved `ollama/qwen3.8:27b`, generated final `CNX448_OLLAMA_TOOL_FINAL`, and created one durable delivery. Delivery experienced two bounded retries under severe resource pressure:

- one Node subprocess exited with JavaScript heap OOM;
- one `chat.inject` call exceeded its bounded command timeout.

The existing retry/reconciliation path subsequently confirmed delivery at `04:28:07.001322Z` and completed the Ticket exactly once.

This run is therefore recorded as resilience evidence, not as the primary terminal-boundary acceptance.

## Post-acceptance runtime cleanliness

Final database checks:

- `PRAGMA integrity_check = ok`;
- global non-terminal Tickets: `0`;
- pending outbox: `0`;
- pending assistant deliveries: `0`.

Both fresh acceptance Tickets have exactly one delivery row and zero outbox rows.

## Final disposition

Task 448 is GREEN. The native OpenClaw/Ollama path now shares the CNX-446 terminal-authority principle without globally requiring Codex `runTerminal` metadata:

`intermediate/tool-use output != terminal authority`

Current classification:

`CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`
