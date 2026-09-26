# Active Coordination

Status: `ACTIVE`
State: `CNX448_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-448-native-ollama-terminal-boundary-and-long-running-semantics.md`
Assigned executor: `ChatGPT`
Review owner: `ChatGPT independent final verification`
Human final authority: `Operator`
Working branch: `cnx-448-native-ollama-terminal-boundary`
Baseline release: `v0.9.8` (immutable)
Baseline SHA: `49915000ecbec131112937cd44ec7a5f0effa00a`

## Trigger

Fresh live Dashboard session `agent:main:dashboard:4e97d1d4-2007-43d0-838d-0a929f1e8140` exposed a native Ollama terminal-boundary defect.

The run `189e1a24-8230-4d50-90fc-d24d25ca1acc` used `ollama/qwen3.8:27b`. Its first assistant write had `stopReason="toolUse"` and tool calls, but CogentNexus staged that intermediate text as the durable Direct result and completed Ticket `CNXT-c7c1531f-81cc-4ac7-a205-516c936a9424`. Tool execution then continued and the run later ended `aborted/request timed out`, producing `host_terminal_conflict`.

## Current objective

Extend the CNX-446 terminal-authority fence to native OpenClaw/Ollama events without globally requiring `runTerminal`.

Required invariant:

```text
intermediate/tool-use assistant output
!= terminal success
!= response_ready
!= durable direct_result
!= delivery_confirmed
!= completed
```

Long-running local inference is explicitly acceptable and must remain separate from terminal classification.

## Current phase

Local implementation and qualification are GREEN.

- GitHub issue: `#40`;
- focused contracts: `20/20 PASS`;
- full plugin Vitest: `94 files / 441 tests PASS`;
- full Python: `745 passed, 5 skipped, 38 subtests passed`;
- build/evaluation/plugin validation/audit/diff-check: PASS.

Next gates:

1. commit and push exact candidate SHA;
2. require GitHub exact-SHA CI GREEN;
3. physical install-over/source parity;
4. fresh native Ollama live acceptance;
5. close Task 448 only after runtime evidence is GREEN.

## Safety constraints

- do not rewrite `v0.9.8`;
- do not weaken exact run/session ownership;
- do not globally require `__openclaw.runTerminal`;
- do not change OpenClaw-owned provider/model/auth routing;
- do not treat model slowness alone as failure;
- fail closed on ambiguous terminal authority.
