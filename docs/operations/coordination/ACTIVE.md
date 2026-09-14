# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_HOOK_EVIDENCE_QUALIFICATION`
Execution mode: `SINGLE_EXECUTOR`
Task ID: `CNX-340B`
Parent: `CNX-340A`
Base candidate: `agent/v0.9.6-direct-model-call-timeout-authority-repair`
Base candidate HEAD: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
Active branch: `agent/v0.9.6-hook-evidence-qualification`

## Objective

Qualify the remaining `before_agent_run` hook evidence gap without sending another real Dashboard semantic request. Prove the registered callback is captured and invoked through an isolated deterministic harness, and that invocation reaches the canonical Ticket-first admission boundary without invoking a provider/model.

## Executor / Reviewer

- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human authority: fresh continuation explicitly authorized by the operator after CNX-340A.

## Prerequisites

- CNX-340A = PASS.
- CNX-340A report is durably published on GitHub.
- Candidate timeout repair HEAD `460a8cd661d02ba419cc1eff13c0efc721cfa928`.
- Candidate artifact SHA `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`.
- Provider/model reference `ollama/qwen3.8:27b`.
- Configured provider/agent timeout authority `2700s`.
- Published `v0.9.5` remains immutable at `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

## Hard fences

- No real Dashboard/Web Session request.
- No OpenAI/Ollama inference.
- No provider/model/routing/timeout configuration mutation.
- No controller mutation.
- No production database mutation.
- No installation or release/tag mutation.
- No retry/recovery/fallback/resend/duplicate-send/manual-dispatch test.
- Do not claim hook execution from static source inspection alone.
- Use an isolated test fixture/harness for invocation evidence.

## Required outcome

The matching task document is:
`docs/operations/coordination/tasks/CNX-20260914-340B-hook-evidence-qualification.md`

Hermes must publish:
`docs/operations/coordination/reports/CNX-20260914-340B-hook-evidence-qualification-report.md`

Then stop for independent ChatGPT review. Hermes must not self-accept the report.

## Status semantics

This ACTIVE entry authorizes execution only. It does not imply PASS. Any missing, inferred-only, contradictory, or production-mutating evidence must be reported as failure with the task's exact failure classification.

## Previous state

- Plan 2 remains closed and is not reopened.
- CNX-339 remains historical evidence and is not replayed.
- CNX-340A remains a completed repair on the candidate branch; CNX-340B is an evidence-qualification continuation, not a second timeout repair.
