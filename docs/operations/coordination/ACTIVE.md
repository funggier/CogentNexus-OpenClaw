# Active Coordination

Status: `IDLE`
State: `CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
Task: none
Last completed task: `CNX-20260926-449-long-running-model-lease-guard.md`
Follow-up backlog: `CNX-20260926-450-headless-agent-durable-settlement.md`
Human final authority: `Operator`
Working branch: `cnx-449-long-running-model-lease-guard`
Baseline release: `v0.9.8` (immutable)
Candidate product SHA: `dfb3706e7c11e61cc7987a7e4928f3c5d7203435`

## Last accepted result

CNX-449 is GREEN. Slow local `ollama/qwen3.8:27b` inference is protected by a 45-minute durable Direct model-call lease. An unexpired active Direct lease prevents probe-only hard-hang Gateway restart. A fresh installed-candidate live call completed after ~20m11s without Gateway restart.

## Follow-up

Task 450 / GitHub issue #42 records the separate headless `openclaw agent` return-to-caller delivery-receipt contract gap. It is backlog and is not active.

## Current classification

`CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
