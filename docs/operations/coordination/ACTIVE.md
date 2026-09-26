# Active Coordination

Status: `ACTIVE`
State: `CNX451_LIVE_SOFT_ACCEPTANCE_PENDING`
Task: `CNX-20260926-451-soft-context-pressure-pass.md`
Assigned executor: `ChatGPT`
Human final authority: `Operator`
Working branch: `cnx-451-soft-context-pressure-live-v2`
Baseline/main SHA: `520d07d5bdb26be22fc03fd48a241c91bc3436ea`
GitHub issue: `#43`

## Accepted prerequisites

- CNX-451 implementation candidate `09eec4113b371d39334d90a332fa9a6455530db0` passed exact-SHA CI and physical install-over.
- CNX-453 infrastructure blocker is GREEN and closed on main at `520d07d5bdb26be22fc03fd48a241c91bc3436ea`.
- CNX-453 physical qualification proved >23-minute Ollama inference can remain protected by the Direct lease, terminal settlement remains exactly once, and `OLLAMA_KEEP_ALIVE=6h` is live.

## Remaining objective

Produce a fresh live owner-session turn whose context guard classifies pressure as `soft`, then prove:
- `context_pressure_soft_observed` is durable;
- the hook does not return a terminal block;
- model inference starts;
- no recovery/context-maintenance authority is created by the soft observation;
- terminal response settles exactly once with zero outbox residue.

CNX-452 remains backlog for hard-pressure compact/resume semantics.

## Current classification

`CNX451_LIVE_SOFT_ACCEPTANCE_PENDING`
