# Active Coordination

Status: `ACTIVE`
State: `CNX453_FOLLOWUP_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-453-scheduled-supervisor-direct-lease-fence.md`
Assigned executor: `ChatGPT`
Human final authority: `Operator`
Working branch: `cnx-453-supervisor-direct-lease-fence`
Baseline SHA: `09eec4113b371d39334d90a332fa9a6455530db0`
First CNX-453 candidate: `21176b07ad98ada944612d444fe5e2d9a8ee0d2b`
GitHub issue: `#45`

## Trigger

CNX-451 live acceptance exposed a physical Gateway-recovery defect during an active Ollama Direct model call. The scheduled Host entered hard-hang recovery before the 45-minute lease expired, and the two-minute Windows Scheduled Task limit could terminate recovery before verified restart.

## Current repair state

Candidate `21176b07...` is exact-SHA CI GREEN and physically installed. It repaired the outer lease fence, lane-drift discovery, Windows task budget (`PT15M`), and fresh-session startup settlement.

Physical requalification exposed one narrower follow-up: if the interrupted session is older than the 15-minute resume-authority freshness fence, startup correctly refuses to resume it but also leaves its pre-boundary model-call / canonical inference-attempt active. The follow-up separates execution settlement from resume authority.

Local follow-up validation is GREEN:
- focused startup settlement: `2/2 PASS`;
- CNX-453 Host regression set: `33/33 PASS`;
- full Python: `754 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `95 files / 444 tests PASS`;
- build/evaluation/plugin validation/audit/diff-check/skill validation: PASS.

## Dependency

CNX-451 soft-pressure code/CI/install qualification remains green, but live acceptance waits for CNX-453 to reach a clean physical durable state.

## Current classification

`CNX453_FOLLOWUP_LOCAL_GREEN_CI_PENDING`
