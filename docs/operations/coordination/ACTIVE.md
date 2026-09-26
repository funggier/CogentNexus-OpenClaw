# Active Coordination

Status: `ACTIVE`
State: `CNX453_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-453-scheduled-supervisor-direct-lease-fence.md`
Assigned executor: `ChatGPT`
Human final authority: `Operator`
Working branch: `cnx-453-supervisor-direct-lease-fence`
Baseline SHA: `09eec4113b371d39334d90a332fa9a6455530db0`
GitHub issue: `#45`

## Trigger

CNX-451 live acceptance exposed a physical Gateway-recovery defect during an active Ollama Direct model call. The call had an unexpired 45-minute durable lease, but the scheduled Host still entered hard-hang maintenance and stopped the Gateway.

## Objective

Fence destructive Gateway recovery with the active Direct lease at the scheduled-supervisor boundary, and settle stale model-call/inference-attempt rows when startup recovery promotes interrupted Direct work.

## Dependency

CNX-451 soft-pressure code/CI/install qualification remains green, but its live acceptance is blocked until CNX-453 is repaired and requalified.

## Current classification

`CNX453_PHYSICAL_DEFECT_CAPTURED_RED_PREPARATION`
