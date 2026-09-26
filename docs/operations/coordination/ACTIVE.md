# Active Coordination

Status: `IDLE`
State: `CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`
Task: none
Assigned executor: none
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

## Completed result

Task 448 is complete.

- exact implementation SHA: `d6cf9e9c532da00880c16a700495edb833658cb4`;
- exact-SHA GitHub CI: three required workflows SUCCESS;
- physical install-over: PASS, controller returned MANAGED generation `34`;
- package/installed payload parity: `296/296` exact, manifest SHA-256 `9559891cbdb63bf58b4b2b3fd05068ee0013fd7d65f2342d9ced7eee8c298b29`;
- fresh native Ollama multi-step acceptance: PASS;
- intermediate `stopReason="toolUse"` did not create `response_ready`, delivery, or Ticket completion;
- later native final settled exactly once;
- SQLite integrity `ok`, non-terminal Tickets `0`, pending outbox `0`, pending assistant delivery `0`.

A simultaneous long-running `ollama/qwen3.8:27b` control entered the existing recovery path and still completed exactly once. Task 448 did not alter timeout/recovery thresholds.

## Current classification

`CNX448_NATIVE_OLLAMA_TERMINAL_BOUNDARY_GREEN`

No new task is active.

## Safety constraints

- do not rewrite `v0.9.8`;
- do not weaken exact run/session ownership;
- do not globally require `__openclaw.runTerminal`;
- do not change OpenClaw-owned provider/model/auth routing;
- do not treat model slowness alone as failure;
- fail closed on ambiguous terminal authority.
