# Active Coordination Task

Status: `READY_FOR_LUNA`
Execution mode: `DUAL_AGENT_BATON__TASK260_DEPLOYMENT_TRANSITION_SAFETY_REQUALIFICATION`
Current disposition: `TASK259_ACCEPTED__DUAL_AGENT_BATON_ENABLED__TASK260_READY`
Task ID: `CNX-20260905-260`
Parent task: `CNX-20260905-259`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT

Assigned executor: `Luna`
Handoff from: `Musethree`
Next actor after report: `Musethree`
Coordination protocol: `docs/operations/coordination/HERMES_DUAL_AGENT_BATON_PROTOCOL.md`

## Accepted predecessor

Task259 review verdict:

`ACCEPT_CONTRACT_REPAIR__CI_GREEN_VERIFIED__LIVE_SUCCESSOR_REVIEW_REQUIRED`

Reviewed candidate:

`d1531404d3eb8e7349a2058484c2fbc7ec9f1bf6`

Task259 source/test repair is accepted and exact-SHA CI was verified 9/9 success. Baseline `6822af4...` is retired as an executable candidate.

## Active Task260

Execute:

`docs/operations/coordination/tasks/CNX-20260905-260-task259-candidate-deployment-transition-safety-requalification.md`

Task260 is evidence/read-only requalification of the deployment transition. It must prove that supported install-over cannot start the predecessor emittable runtime during the transition and that candidate startup would apply the repaired freshness predicate to the stale recovery row.

## Live hard fences

```text
installer registration/start = 0
scripts/install.ps1 live starts = 0
Gateway/controller/provider lifecycle mutation = 0
live DB/recovery mutation = 0
recovery dispose/replay/redeliver/resend = 0
semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
```

## Baton rule

Luna owns Task260. After publishing the matching report, Luna must hand off to Musethree and invoke/call Musethree when available. Musethree must independently review Task260 before selecting any successor.

If Musethree can determine one safe authorized successor, Musethree may open/execute it under the standing baton protocol. If not, set `WAITING_FOR_CHATGPT` and tell the human operator to notify ChatGPT.
