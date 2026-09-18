# CNX-20260918-405 — ChatGPT Review

## Decision

`ACCEPTED`

Classification accepted:

`PRODUCTION_REGISTRY_LIFECYCLE_PATH_MAPPED`

## Review basis

CNX-405 correctly separates direct source/runtime evidence from mechanism inference.

The report establishes that one OpenClaw process can execute multiple plugin-registration/load lifecycles without requiring duplicate filesystem roots, and that cache activation or registry replacement can change active registry identity without a new plugin-side registration event.

It also correctly refuses to claim a production caller identity, cache decision, registry identity, or exact activation sequence where the available PID-correlated evidence does not support one.

No unsupported causal assignment is required to accept the task's stated mapping objective.

## Boundary accepted

The registry-lifecycle investigation is sufficient for its read-only mapping objective.

Further lifecycle archaeology is not the highest-value primary workstream for the Operator's newly explicit product goal:

> Use CogentNexus-OpenClaw like ordinary OpenClaw: select provider/model in Web Chat, switch provider/model, and continue the same session and work.

The Operator explicitly authorized continued work toward that goal after CNX-405.

## Important carry-forward evidence

Subsequent repository review confirms:

- OpenClaw already owns Cloud provider/model/auth/routing in the v0.9.5 design.
- `V095_PROVIDER_SWITCH_ACCEPTANCE.md` already specifies Web Chat provider switching while preserving CNX identity.
- Model selection via `sessions.patch` is intentionally passed through without mutating CNX Ticket state.
- Real OpenAI Dashboard execution has already been demonstrated in CNX-357/CNX-367.
- CNX-375/CNX-376 show the current practical continuity failure: the model path succeeds, but CNX Ticket-first admission is skipped because `before_agent_run` is absent from the live composed hook registry.

Therefore the next workstream must preserve OpenClaw routing authority and determine the exact working Ollama/OpenClaw vertical slice plus the CNX continuity boundary, rather than creating a new provider router.

## Successor

Authorized successor:

`CNX-20260918-406 — Real Provider Runtime Baseline: Ollama Web Chat End-to-End Trace`

CNX-406 is read-only archaeology. It must not mutate provider/auth/routing or production runtime.

## Reviewer

ChatGPT

Human final authority: Operator
