# Active Coordination

Status: `ACTIVE`
State: `CNX449_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-449-long-running-model-lease-guard.md`
Assigned executor: `ChatGPT`
Review owner: `ChatGPT independent final verification`
Human final authority: `Operator`
Working branch: `cnx-449-long-running-model-lease-guard`
Baseline release: `v0.9.8` (immutable)
Baseline SHA: `bffa539a59f8d0318cbffb062a73b205c8cb8705`

## Trigger

CNX-448 live qualification proved that a CPU-heavy `ollama/qwen3.8:27b` call can be healthy but make the Gateway fail lightweight probes long enough for the external Host to trigger hard-hang recovery prematurely.

## Objective

Protect unexpired Direct model-call leases from probe-only Gateway restart and extend the default Ollama lease to 45 minutes while leaving non-Ollama behavior at 15 minutes.

## Current classification

`CNX449_LOCAL_GREEN_CI_PENDING`
