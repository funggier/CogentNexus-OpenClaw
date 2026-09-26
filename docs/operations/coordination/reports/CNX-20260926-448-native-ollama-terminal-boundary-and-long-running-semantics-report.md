# CNX-20260926-448 — Native Ollama Terminal Boundary and Long-Running Semantics Report

Status: `IN_PROGRESS`
Classification: `CNX448_LOCAL_GREEN_CI_PENDING`
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

## Current disposition

The source repair is locally GREEN. Remaining acceptance gates are:

1. exact candidate commit and branch publication;
2. GitHub exact-SHA CI;
3. physical install-over and source/installed parity;
4. fresh native Ollama live acceptance proving intermediate tool-use cannot complete a Ticket and true final settlement remains exactly once.

Current classification:

`CNX448_LOCAL_GREEN_CI_PENDING`
